# /// script
# dependencies = [
#   "watchdog",
#   "gitpython",
# ]
# ///

import argparse
import logging
import os
import subprocess
import sys
import time
from pathlib import Path

import git
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


class CopierSourceWatcher(FileSystemEventHandler):
    def __init__(
        self,
        source_dir: Path,
        dest_dir: Path,
        commit_message: str,
        answers_file: Path,
        debounce_seconds: float = 2.0,
        append_only: bool = False,
    ):
        self.source_dir = source_dir.resolve()
        self.dest_dir = dest_dir.resolve()
        self.commit_message = commit_message
        self.answers_file = answers_file
        self.debounce_seconds = debounce_seconds
        self.last_event_time = 0
        self.is_first_commit = not append_only
        self.append_only = append_only

        # Initialize git repos
        self.source_repo = git.Repo(self.source_dir)
        self.dest_repo = git.Repo(self.dest_dir)

        logger.info(f"Watching {self.source_dir} for changes")
        logger.info(f"Target destination: {self.dest_dir}")
        logger.info(f"Using answers file: {self.answers_file}")

    def on_any_event(self, event):
        # Skip temporary files and .git directory changes
        if (
            event.src_path.endswith(".swp")
            or event.src_path.endswith(".swx")
            or event.src_path.endswith(".tmp")
            or event.src_path.endswith(".bak")
            or event.src_path.endswith("~")
            or "/.#" in event.src_path
            or "/#" in event.src_path
            or ".git" in event.src_path
        ):
            return

        # If the events is a directory and the name didn't change, skip it
        if event.is_directory and event.event_type == "modified":
            return
        current_time = time.time()

        # Debounce - only process if we haven't had an event in a while
        if current_time - self.last_event_time >= self.debounce_seconds:
            logger.info(f"Change detected: {event.src_path}")
            self.process_changes()

        self.last_event_time = current_time

    def process_changes(self):
        # Wait for file operations to complete
        time.sleep(self.debounce_seconds)

        try:
            # 1. Commit changes in source repo
            changes_made = self._commit_source_changes()
            if not changes_made:
                return

            # 2. Get the current revision from source repo
            source_rev = self.source_repo.active_branch.name
            logger.info(f"Source active branch: {source_rev}")

            # 3. Apply changes to destination repo
            self._update_destination_repo(source_rev)

            logger.info("Update completed successfully")

        except Exception as e:
            logger.error(f"Error processing changes: {str(e)}")

    def _commit_source_changes(self) -> bool:
        """Commit changes in the source repository. Returns True if changes were committed."""

        # Check if there are any changes to commit
        if not self.source_repo.is_dirty(untracked_files=True):
            logger.info("No changes detected in source repository. Skipping commit.")
            return False

        logger.info("Committing changes in source repository...")
        # Add all changes
        self.source_repo.git.add(".")

        if self.is_first_commit:
            # First commit with provided message
            self.source_repo.git.commit(m=self.commit_message)
            self.is_first_commit = False
            logger.info(f"Initial commit created with message: '{self.commit_message}'")
        else:
            # Amend existing commit
            self.source_repo.git.commit("--amend", "--no-edit")
            logger.info("Amended previous commit with new changes")
        return True

    def _update_destination_repo(self, source_rev: str):
        logger.info("Updating destination repository...")

        # Clean the destination repo
        self.dest_repo.git.reset("--hard", "HEAD")
        self.dest_repo.git.clean("-df")
        logger.info("Destination repo reset to clean state")

        # Run copier update
        cmd = [
            "uvx",
            "copier",
            "update",
            "-r",
            source_rev,
            "-a",
            str(self.answers_file),
            "-A",
        ]
        # Because of https://github.com/gitpython-developers/gitpython/issues/571
        # we need to do some URL swapping for SSH URLs
        remote_url = self.source_repo.remotes.origin.url
        if remote_url.startswith("git@"):
            # Convert SSH URL to HTTPS
            remote_url = remote_url.replace(":", "/").replace("git@", "https://")

        env = {
            **os.environ,
            "GIT_CONFIG_PARAMETERS": f"'url.{self.source_repo.working_dir}.insteadOf={remote_url}.git'",
        }

        logger.info(
            f"Running: `{' '.join(cmd)}` with GIT_CONFIG_PARAMETERS={env['GIT_CONFIG_PARAMETERS']}"
        )
        try:
            result = subprocess.run(
                cmd,
                cwd=self.dest_dir,
                capture_output=True,
                text=True,
                check=True,
                env=env,
            )
            logger.info("Copier update completed")
            logger.debug(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Copier update failed: {e}")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            raise


def parse_args():
    parser = argparse.ArgumentParser(
        description="""
            Watch a copier source directory and apply changes to a destination repo.

            Run with `uv run copier-watch.py` to ensure the correct environment is used.

            WARNING: This script monkeys with git repositories and can cause data loss.
            Use with caution and ensure you have backups of your repositories.
            Essentially it runs git reset and git clean on the destination repo.
        """
    )
    parser.add_argument(
        "source_dir", type=Path, help="Source directory (copier template)"
    )
    parser.add_argument(
        "dest_dir",
        type=Path,
        help="Destination directory (where copier template is applied)",
    )
    parser.add_argument(
        "--commit-message",
        "-m",
        default="Update copier template",
        help="Commit message for source repo changes",
    )
    parser.add_argument(
        "--answers-file",
        "-a",
        type=Path,
        required=True,
        help="Path to answers file for copier",
    )
    parser.add_argument(
        "--debounce-seconds",
        type=float,
        default=2.0,
        help="Debounce time in seconds to group file changes",
    )
    parser.add_argument(
        "--append-only",
        action="store_true",
        help="Only amend existing commits, never create new ones",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Validate paths
    if not args.source_dir.exists():
        logger.error(f"Source directory does not exist: {args.source_dir}")
        return 1

    if not args.dest_dir.exists():
        logger.error(f"Destination directory does not exist: {args.dest_dir}")
        return 1

    if not (args.answers_file.exists() or (args.dest_dir / args.answers_file).exists()):
        logger.error(
            f"Answers file does not exist: {args.dest_dir / args.answers_file}"
        )
        return 1

    # Check if paths are git repositories
    try:
        git.Repo(args.source_dir)
        git.Repo(args.dest_dir)
    except git.exc.InvalidGitRepositoryError:
        logger.error("Both source and destination must be git repositories")
        return 1

    # Set up the file watcher
    event_handler = CopierSourceWatcher(
        source_dir=args.source_dir,
        dest_dir=args.dest_dir,
        commit_message=args.commit_message,
        answers_file=args.answers_file,
        debounce_seconds=args.debounce_seconds,
        append_only=args.append_only,
    )

    observer = Observer()
    observer.schedule(event_handler, str(args.source_dir), recursive=True)
    observer.start()

    try:
        logger.info("Watcher started. Press Ctrl+C to stop.")
        # Process initial state
        event_handler.process_changes()

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()

    observer.join()
    return 0


if __name__ == "__main__":
    sys.exit(main())

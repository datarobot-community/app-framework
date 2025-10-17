import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import click
import git
import yaml
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

from lib import TemplateConfiguration, _clone_repo, extract_github_organization_repo_name

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("copier_watch")



class CopierSourceWatcher(FileSystemEventHandler):
    def __init__(
        self,
        template_configurations: list[TemplateConfiguration],
        dest_dir: Path,
        commit_message: str,
        debounce_seconds: float = 2.0,
        append_only: bool = False,
    ):
        self.templates = template_configurations
        self.dest_dir = dest_dir.resolve()
        self.commit_message = commit_message
        self.debounce_seconds = debounce_seconds
        self.last_event_time = 0
        self.is_first_commit = not append_only
        self.append_only = append_only

        # Initialize git repos
        self.dest_repo = git.Repo(self.dest_dir)

        self.parent_module_map: dict[Path, list[TemplateConfiguration]] = {}
        template_by_remote = {t.repo_id: t for t in template_configurations}
        for template in template_configurations:
            for submodule in template.git_repo.submodules:
                if (repo_id := extract_github_organization_repo_name(submodule.url)) and (submodule_template := template_by_remote.get(repo_id)):
                    key = submodule_template.template_directory
                    self.parent_module_map.setdefault(key, []).append(template)
                else: # Might be a path
                    p = Path(submodule.url)
                    if p.exists():
                        try:
                            g = git.Repo(p)
                        except git.InvalidGitRepositoryError:
                            continue
                        if g.remotes and (repo_id := extract_github_organization_repo_name(g.remotes[0].url)) and (submodule_template := template_by_remote.get(repo_id)):
                            key = submodule_template.template_directory
                            self.parent_module_map.setdefault(key, []).append(template)
                

        logger.info(f"Watching {[x.template_directory for x in self.templates]} for changes")
        logger.info(f"Target destination: {self.dest_dir}")
        logger.info(f"Using answers file: {[x.answers_file for x in self.templates]}")

    def on_any_event(self, event: FileSystemEvent) -> None:
        # Skip temporary files and .git directory changes
        src_path: str = event.src_path
        if (
            src_path.endswith(".swp")
            or src_path.endswith(".swx")
            or src_path.endswith(".tmp")
            or src_path.endswith(".bak")
            or src_path.endswith("~")
            or "/.#" in src_path
            or "/#" in src_path
            or ".git" in src_path
        ):
            return

        # If the events is a directory and the name didn't change, skip it
        if event.is_directory and event.event_type == "modified":
            return
        current_time = time.time()

        # Debounce - only process if we haven't had an event in a while
        if current_time - self.last_event_time >= self.debounce_seconds:
            logger.info(f"Change detected: {event.src_path}")
            self.process_changes(Path(src_path))

        self.last_event_time = current_time

    def process_changes(self, path: Path) -> None:
        path = path.resolve()
        # Wait for file operations to complete
        time.sleep(self.debounce_seconds)

        changed_template = next((t for t in self.templates if t.template_directory in path.parents or t.template_directory == path), None)

        if not changed_template:
            logger.debug("Path %s did not belong to any known templates.", path)
            return

        try:
            # 1. Commit changes in source repo
            changes_made = self._commit_source_changes(changed_template)
            if not changes_made:
                return

            # 2. Get the current revision from source repo
            source_rev = changed_template.git_repo.active_branch.name
            logger.info(f"Source active branch: {source_rev}")

            # 3. Apply changes to destination repo
            self._update_destination_repo(changed_template, source_rev)

            # 4. Update parent modules of this module (which will trigger another round of updates)
            self._update_git_parent_modules(changed_template)

            logger.info("Update completed successfully")

        except Exception as e:
            logger.error(f"Error processing changes: {str(e)}")

    def _commit_source_changes(self, template: TemplateConfiguration) -> bool:
        """Commit changes in the source repository. Returns True if changes were committed."""

        # Check if there are any changes to commit
        if not template.git_repo.is_dirty(untracked_files=True):
            logger.info("No changes detected in source repository. Skipping commit.")
            return False

        logger.info("Committing changes in source repository...")
        # Add all changes
        template.git_repo.git.add(".")

        self._commit_changes(template)
        return True

    def _commit_changes(self, template: TemplateConfiguration) -> None:
        if template.is_first_commit:
            # First commit with provided message
            template.git_repo.git.commit(m=self.commit_message)
            self.is_first_commit = False
            logger.info(f"Initial commit created for {template.template_directory} with message: '{self.commit_message}'")
        else:
            # Amend existing commit
            template.git_repo.git.commit("--amend", "--no-edit")
            logger.info("Amended previous commit with new changes")
    
    def _update_git_parent_modules(self, changed_submodule: TemplateConfiguration) -> None:
        parents = self.parent_module_map.get(changed_submodule.template_directory, [])
        for template in parents:
            template.git_repo.submodule_update(recursive=True)
            # We're not going to bother to commit changes or recurse as this triggers another round of updates that will propagate and commit


    def _update_destination_repo(self, template: TemplateConfiguration, source_rev: str) -> None:
        # E.g. library components don't directly apply.
        if not template.answers_file:
            return
        
        logger.info("Updating destination repository...")

        # Clean the destination repo
        self.dest_repo.git.reset("--hard", "HEAD")
        self.dest_repo.git.clean("-df")
        logger.info("Destination repo reset to clean state")

        for answer in template.answers_file:
            # Run copier update
            cmd = [
                "uvx",
                "copier",
                "update",
                "-r",
                source_rev,
                "-a",
                str(answer),
                "-A",
            ]
            # Because of https://github.com/gitpython-developers/gitpython/issues/571
            # we need to do some URL swapping for SSH URLs
            remote_url = template.git_repo.remotes.origin.url
            if remote_url.startswith("git@"):
                # Convert SSH URL to HTTPS
                remote_url = remote_url.replace(":", "/").replace("git@", "https://")
            remote_url = remote_url.removesuffix(".git")  # We add it later, don't have double .git.git

            env = {
                **os.environ,
                "GIT_CONFIG_PARAMETERS": f"'url.{template.git_repo.working_dir}.insteadOf={remote_url}.git'",
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

@click.group()
def cli():
    pass

@cli.command("watch-repo", short_help="Watch a single repo.")
@click.argument("source_dir", help="Source directory (copier template)", type=click.Path(file_okay=False, path_type=Path))
@click.argument("dest_dir", help="Destination directory (where copier template is applied)", type=click.Path(file_okay=False, path_type=Path))
@click.option("--commit-message", "-m", default="Update copier template", help="Commit message for source repo changes", type=str)
@click.option("--answers-file", "-a", required=True, type=click.Path(dir_okay=False, path_type=Path), help="Path to answer files for copier")
@click.option("--debounce-seconds", default=2.0, type=float, help="Debounce time in seconds to group file changes.")
@click.option("--append-only", is_flag=True, help="Only amend existing commits, never create new ones")
def watch_repo(
    source_dir: Path,
    dest_dir: Path,
    commit_message: str,
    answers_file: Path,
    debounce_seconds: float,
    append_only: bool
) -> None:
       # Validate paths
    if not source_dir.exists():
        logger.error(f"Source directory does not exist: {source_dir}")
        sys.exit(1)

    if not dest_dir.exists():
        logger.error(f"Destination directory does not exist: {dest_dir}")
        sys.exit(1)

    if not (answers_file.exists() or (dest_dir / answers_file).exists()):
        logger.error(
            f"Answers file does not exist: {dest_dir / answers_file}"
        )
        sys.exit(1)

    # Check if paths are git repositories
    try:
        git.Repo(source_dir)
        git.Repo(dest_dir)
    except git.InvalidGitRepositoryError:
        logger.error("Both source and destination must be git repositories")
        sys.exit(1)

    template = TemplateConfiguration(template_directory=source_dir, answers_file=[answers_file])

    # Set up the file watcher
    event_handler = CopierSourceWatcher(
        template_configurations=[template],
        dest_dir=dest_dir,
        commit_message=commit_message,
        debounce_seconds=debounce_seconds,
        append_only=append_only,
    )

    observer = Observer()
    observer.schedule(event_handler, str(source_dir), recursive=True)
    observer.start()

    try:
        logger.info("Watcher started. Press Ctrl+C to stop.")
        # Process initial state
        event_handler.process_changes(template.template_directory)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()

    observer.join()

@cli.command("watch-all", short_help="Watch all answers.", help="""
This parses the answers in the given --answers-directory to figure out which templates to watch
and then watches the corresponding templates in the direction directory. This has the potential
to mess up your directory as it commits. Make sure important local changes are backed up and
create new git branches. If not
""".strip())
@click.option("--sources-dir", "-s", help="Source directory containing copier templates", type=click.Path(file_okay=False, path_type=Path), default=Path(".."))
@click.option("--destination-dir", "-d", help="Destination directory (where copier template is applied)", type=click.Path(file_okay=False, path_type=Path), default=Path("."))
@click.option("--commit-message", "-m", default="Update copier template", help="Commit message for source repo changes", type=str)
@click.option("--answers-directory", "-a", default=Path(".datarobot/answers"), type=click.Path(file_okay=False, path_type=Path), help="Path to answer files for copier")
@click.option("--debounce-seconds", default=2.0, type=float, help="Debounce time in seconds to group file changes.")
@click.option("--append-only", is_flag=True, help="Only amend existing commits, never create new ones")
@click.option("--submodules", is_flag=True, help="Include watching submodules of watched components")
@click.option("--clone-missing", is_flag=True, help="Clone any missing repos (including, transitively, submodules if --include-submodules set)")
def watch_all(
    sources_dir: Path,
    destination_dir: Path,
    commit_message: str,
    answers_directory: Path,
    debounce_seconds: float,
    append_only: bool,
    submodules: bool,
    clone_missing: bool
) -> None:
    if not sources_dir.exists():
        logger.error(f"Sources dir does not exist {sources_dir}.")
        sys.exit(1)
    if not destination_dir.exists():
        logger.error(f"Destination dir does not exist {destination_dir}")
        sys.exit(1)
    
    if not answers_directory.exists() and not answers_directory.is_absolute():
        answers_directory = destination_dir / answers_directory
    
    if not answers_directory.exists():
        logger.error(f"Answers directory does not exist: {answers_directory}.")
    
    
    # 1. Figure out what repos are needed from the answer files.


    repos: dict[str, list[Path]] = {}

    remote_repos: dict[str, str] = {}
    local_repos: dict[str, Path] = {}
    

    for file in answers_directory.iterdir():
        if file.suffix in [".yml", ".yaml"]:
            with file.open() as f:
                contents: dict[str, Any] = yaml.safe_load(f)
            logger.debug("Looking for source of answer file %s.", file, contents)
            if remote := contents.get("_src_path"):
                if repo := extract_github_organization_repo_name(remote):
                    remote_repos[repo] = remote
                    repos.setdefault(repo, []).append(file)
                else: # This is likely a local reference: check if it's on disk.
                    remote_path = Path(remote)
                    if remote_path.exists():
                        try:
                            remote_repo = git.Repo(remote_path)
                        except git.InvalidGitRepositoryError:
                            logger.warning(f"For answer file {file}, the path {remote} exists, but not as a git repo.")
                            continue
                        if remote_repo.remotes and (repo := extract_github_organization_repo_name(remote_repo.remotes[0].url)):
                            local_repos[repo] = remote_path
                            repos.setdefault(repo, []).append(file)

                
    logger.info(f"Found the following components in answers: {repos}")

    # 2. Figure out what repos we already have pulled.

    base_template_configurations: dict[str, TemplateConfiguration] = {}

    repo_id_to_path: dict[str, Path] = {}

    for directory in sources_dir.iterdir():
        try:
            repo = git.Repo(directory)
        except git.InvalidGitRepositoryError:
            continue
        if repo.remotes and (repo_id := extract_github_organization_repo_name(repo.remotes[0].url)):
            repo_id_to_path[repo_id] = directory
            if answer_file := repos.get(repo_id):
                base_template_configurations[repo_id] = TemplateConfiguration(directory, answer_file)

    
    missing: set[str] = set(repos) - set(base_template_configurations)

    # 3. Clone missing
    if clone_missing:
        for repo in missing:
            _clone_repo(sources_dir, repo)
            repo_directory = sources_dir / ":".split(repo)[1]
            base_template_configurations[repo] = TemplateConfiguration(
                template_directory=repo_directory,
                answers_file=repos[repo]
            )
        
    # 4. Figure out submodules.
    if submodules:
        examined_repos: set[str] = set()
        unexamined_repos: set[str] = set(base_template_configurations) - examined_repos
        while unexamined_repos:
            for repo in unexamined_repos:
                template = base_template_configurations[repo]

                # 4.1. Register and clone submodule
                for submodule in template.submodules:
                    if not submodule.local_path and submodule.repo_id:
                        submodule.clone(sources_dir)

                    if submodule.local_path and submodule.repo_id:
                        base_template_configurations[submodule.repo_id] = TemplateConfiguration(
                            submodule.local_path,
                            repos[submodule.repo_id]
                        )
                
                # 4.2. Repoint submodules at local.
                template.point_modules_at_local()
                
                examined_repos.add(repo)

            unexamined_repos = set(base_template_configurations) - examined_repos

    templates = list(base_template_configurations.values())

    # Set up the file watcher
    event_handler = CopierSourceWatcher(
        template_configurations=templates,
        dest_dir=destination_dir,
        commit_message=commit_message,
        debounce_seconds=debounce_seconds,
        append_only=append_only,
    )

    observer = Observer()
    for template in templates:
        observer.schedule(event_handler, str(template.template_directory), recursive=True)
    observer.start()

    try:
        logger.info("Watcher started. Press Ctrl+C to stop.")
        # Process initial state
        for template in templates:
            event_handler.process_changes(template.template_directory)

        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping watcher...")
        observer.stop()

    observer.join()

        
from contextlib import contextmanager
from functools import cached_property
import logging
import os
import re
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Generator, Self

import git
import toml
import yaml

logger = logging.getLogger("copier_watch")

@dataclass
class Submodule:
    name: str
    local_path: Path | None
    remote_url: str | None
    repo_id: str | None

    @classmethod
    def from_submodule(cls, submodule: git.Submodule) -> Self | None:
        path: Path | None 
        url: str | None = None
        repo_id: str | None = None
        
        if submodule.url and (repo_id := extract_github_organization_repo_name(submodule.url)):
            url = submodule.url
            path = None
        else:
            path = Path(submodule.url)
            try:
                repo = git.Repo(path)
            except git.InvalidGitRepositoryError:
                logger.warning(f"Could not figure out submodule {submodule.url}")
                return None
            if repo.remotes:
                repo_id = extract_github_organization_repo_name(repo.remotes[0].url)
                url = repo.remotes[0].url
            
        return cls(
            name=submodule.name,
            local_path=path,
            remote_url=url,
            repo_id=repo_id
        )
    
    def clone(self, dir: Path) -> Path | None:
        if not self.repo_id:
            return None
        self.local_path = _clone_repo(dir, self.repo_id)
        return self.local_path
    
    

@dataclass
class TemplateConfiguration:
    template_directory: Path
    answers_file: list[Path]
    git_repo: git.Repo = field(init=False)
    is_first_commit: bool = field(init=False, default=True)

    def __post_init__(self):
        self.template_directory = self.template_directory.resolve()
        self.answers_file = [a.resolve() for a in self.answers_file]
        self.git_repo = git.Repo(self.template_directory)

    @cached_property
    def repo_id(self) -> str:
        repo = extract_github_organization_repo_name(self.git_repo.remotes[0].url)
        assert repo
        return repo
    
    @cached_property
    def submodules(self) -> list[Submodule]:
        return [s for s in map(Submodule.from_submodule, self.git_repo.submodules) if s]
    
    def point_answer_at_local(self) -> None:
        for answer in self.answers_file:
            with open(answer) as f:
                answer_contents: dict[str, Any] = yaml.safe_load(f)
            answer_contents["_src_path"] = str(self.template_directory.absolute())
            with open(answer, "w") as f:
                yaml.safe_dump(answer_contents, f)
    
    def point_answer_at_remote(self) -> None:
        if not self.git_repo.remotes:
            return
        
        remote = self.git_repo.remotes[0].url

        for answer in self.answers_file:
            with open(answer) as f:
                answer_contents: dict[str, Any] = yaml.safe_load(f)
            answer_contents["_src_path"] = remote
            with open(answer, "w") as f:
                yaml.safe_dump(answer_contents, f)
    
    def point_modules_at_local(self) -> None:
        with self._modifying_git_module() as submodules:
            for submodule, sub_config in submodules:
                if submodule.local_path:
                    sub_config['url'] = str(os.path.relpath(self.template_directory, submodule.local_path))
        


    def point_modules_at_remote(self) -> None:
        with self._modifying_git_module() as submodules:
            for submodule, sub_config in submodules:
                if submodule.remote_url:
                    sub_config['url'] = submodule.remote_url
                elif submodule.repo_id:
                    sub_config['url'] = f'git@github.com:{submodule.repo_id}'

    def change_modules_branch(self, branch: str) -> None:
        with self._modifying_git_module() as submodules:
            for _, sub_config in submodules:
                sub_config['branch'] = branch

    def resync_submodules(self):
        if (self.template_directory / ".gitmodules").exists():
            self._resync_submodules()

    @contextmanager
    def _modifying_git_module(self) -> Generator[list[tuple[Submodule, dict[str, str]]], None, None]:
        modules_file = self.template_directory / ".gitmodules"

        submodules = []

        if modules_file.exists():
            module_content = toml.loads(modules_file.read_text())
            for submodule in self.submodules:
                key = f'submodule "{submodule.name}"'
                if key not in module_content:
                    logger.warning(f"Module {submodule.repo_id} not found in .gitmodules")
                    continue

                sub_config: dict[str, str] = module_content[key]
                submodules.append((submodule, sub_config))

            yield submodules
                    
            with open(modules_file, "w") as f:
                toml.dump(module_content, f)

            self._resync_submodules()
        else:
            yield []

        

    def _resync_submodules(self) -> None:
        cmd = [
            "git",
            "submodule",
            "sync"
        ]
        try:
            result = subprocess.run(
                        cmd,
                        check=True,
                        cwd=self.template_directory,
                        text=True,
                        capture_output=True
                    )
            logger.info("Synced %s", self.template_directory)
            logger.debug(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Syncs failed: {e}")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            raise

        cmd = [
            "git",
            "submodule",
            "update",
            "--init",
            "--recursive",
            "--remote"
        ]
        try:
            result = subprocess.run(
                        cmd,
                        check=True,
                        cwd=self.template_directory,
                        text=True,
                        capture_output=True
                    )
            logger.info("Synced %s", self.template_directory)
            logger.debug(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Syncs failed: {e}")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            raise


def extract_github_organization_repo_name(url: str) -> str | None:
    """
    Given a github URL in HTTPS, e.g. https://github.com/ORG/REPO(.git)?, or SSH, git@github.com:ORG/REPO.git, extract ORG/REPO.

    Args:
        url (str): A github repository URL

    Returns:
        str: The ORG/REPO if present, else NONE.
    """
    if not url or not isinstance(url, str):
        return None

    url = url.strip()

    # Patterns to match common GitHub URL forms:
    #  - HTTPS: https://github.com/ORG/REPO(.git)?[/]
    #  - SSH scp-like: git@github.com:ORG/REPO(.git)?
    #  - SSH url: ssh://git@github.com/ORG/REPO(.git)?[/]
    patterns = [
        r"^https?://(?:www\.)?github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
        r"^git@github\.com:([^/]+)/([^/]+?)(?:\.git)?$",
        r"^ssh://git@github\.com/([^/]+)/([^/]+?)(?:\.git)?/?$",
    ]

    for pat in patterns:
        if m := re.match(pat, url):
            org, repo = m.group(1), m.group(2)
            repo = repo.rstrip("/").removesuffix(".git")
            org = org.rstrip("/")
            if org and repo:
                return f"{org}/{repo}"

    return None


def _clone_repo(sources_dir: Path, repo: str) -> Path:
    cmd = [
        "git",
        "clone",
        f"git@github.com:{repo}.git"
    ]
    try:
        result = subprocess.run(
                    cmd,
                    check=True,
                    cwd=sources_dir,
                    text=True,
                    capture_output=True
                )
        logger.info("Cloned %s", repo)
        logger.debug(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error(f"Clone failed: {e}")
        logger.error(f"STDOUT: {e.stdout}")
        logger.error(f"STDERR: {e.stderr}")
        raise
    
    return sources_dir / (repo.split('/')[1])
        

import urllib.parse
from pathlib import Path
from typing import Optional

import git


class BranchNotFound(Exception):
    def __init__(self, branch_name):
        super().__init__(f"Branch not found: {branch_name}")
        self.branch_name = branch_name


def branch_exists(repo: git.Repo, branch_name):
    return any(branch.name == branch_name for branch in repo.branches + repo.refs)


def get_repository(repository_path: Path) -> git.Repo:
    return git.Repo(repository_path)


def get_commits_head_and_compare(repo: git.Repo, compare_branch: str) -> tuple[str, str]:
    if not branch_exists(repo, compare_branch):
        raise BranchNotFound(compare_branch)
    compare_commit_head_hash = repo.git.rev_parse(compare_branch)
    current_commit_head_hash = repo.head.commit.hexsha

    return compare_commit_head_hash, current_commit_head_hash


def get_diff_paths(repo_path: Path, compare_branch: str) -> list[str]:
    repo = get_repository(repo_path)
    commit_head, commit_compare = get_commits_head_and_compare(repo, compare_branch)
    diff = repo.git.diff(commit_head, commit_compare, name_only=True)
    return diff.split("\n") if diff else []


def get_diff_per_files(repo_path: Path, compare_branch: str) -> dict[str, str]:
    repo = get_repository(repo_path)
    commit_head, commit_compare = get_commits_head_and_compare(repo, compare_branch)
    diff_paths = get_diff_paths(repo_path, compare_branch)
    diff_dict = {path: repo.git.diff(commit_head, commit_compare, path) for path in diff_paths}
    return diff_dict


def get_head_branch_info(repo):
    head_commit = repo.head.commit
    return {
        "ref": head_commit.name_rev,
        "commit_sha": head_commit.hexsha,
        "commit_author": head_commit.author.name,
        "commit_date": head_commit.committed_datetime.isoformat(),
    }


def get_base_branch_info(repo: git.Repo, base_branch: str):
    target_commit = repo.commit(base_branch)
    return {
        "ref": base_branch,
        "commit_sha": target_commit.hexsha,
        "commit_author": target_commit.author.name,
        "commit_date": target_commit.committed_datetime.isoformat(),
    }


def extract_repository_owner_and_name(repository_url: str) -> tuple[str, str]:
    """Handle 'git@' and 'https' repository url"""
    parsed_url = urllib.parse.urlparse(repository_url)
    path_parts = parsed_url.path.split("/")
    if len(path_parts) < 2:
        return "", ""
    if not path_parts[0] and len(path_parts) >= 3:
        path_parts = path_parts[1:]
    repo_owner = path_parts[0]
    if repo_owner.startswith("git@"):
        repo_owner = repo_owner.split(":")[-1]
    repo_name = path_parts[1]
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    return repo_owner, repo_name


def get_repository_metadata(repository_path: Path, base_branch: Optional[str] = None):
    repo = get_repository(repository_path)

    head_branch_info = get_head_branch_info(repo)

    repository_info = {
        "head_branch": head_branch_info,
        "default_branch": repo.heads[0].name if repo.heads else "",
    }
    if base_branch:
        base_branch_info = get_base_branch_info(repo, base_branch)
        repository_info["base_branch"] = base_branch_info
    repository_url = repo.remotes.origin.url if repo.remotes else None
    if repository_url:
        repository_owner, repository_name = extract_repository_owner_and_name(repository_url)
        repository_info["repository_owner"] = repository_owner
        repository_info["repository_name"] = repository_name
        repository_info["repository_url"] = repository_url
    return repository_info


def get_repository_metadata_with_diff(repository_path: Path, base_branch: str):
    diff_dict = get_diff_per_files(repository_path, base_branch)
    repository_info = get_repository_metadata(repository_path, base_branch)
    repository_info["pull_request"] = diff_dict
    return repository_info

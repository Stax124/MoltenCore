import pytest

from core.github_parser import Repository


@pytest.fixture()
def repo():
    return Repository("https://github.com/Stax124/test-plugin")


def test_repo_name(repo: Repository):
    assert repo.name == "test-plugin"


def test_repo_stars(repo: Repository):
    assert type(repo.stars) == int


def test_repo_forks(repo: Repository):
    assert type(repo.forks) == int


def test_repo_issues(repo: Repository):
    assert type(repo.issues) == int


def test_repo_license(repo: Repository):
    assert repo.license == "MIT License"


def test_repo_owner(repo: Repository):
    assert repo.owner == "Stax124"

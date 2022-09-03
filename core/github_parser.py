import json
from datetime import datetime

import requests


def rewrite_url(url: str) -> str:
    return url.replace("https://github.com/", "https://api.github.com/repos/")


def parse(repo_url: str):
    response = requests.get(repo_url)

    if response.status_code != 200:
        return None

    content = response.content
    data = json.loads(content)
    return data


class Repository:
    def __init__(self, url: str) -> None:
        self.url = rewrite_url(url)
        print(self.url)
        self.data = parse(self.url)

    def refresh_data(self):
        self.data = parse(self.url)

    @property
    def owner(self):
        return self.data["owner"]["login"] if self.data else ""

    @property
    def name(self):
        return self.data["name"] if self.data is not None else ""

    @property
    def stars(self):
        return self.data["stargazers_count"] if self.data else 0

    @property
    def license(self):
        return (
            self.data["license"]["name"]
            if self.data and self.data["license"]
            else "None"
        )

    @property
    def forks(self):
        return self.data["forks"] if self.data else 0

    @property
    def issues(self):
        return self.data["open_issues"] if self.data else 0

    @property
    def watchers(self):
        return self.data["subscribers_count"] if self.data else 0

    @property
    def last_updated(self):
        return (
            datetime.fromisoformat(str(self.data["updated_at"]).replace("Z", ""))
            if self.data
            else None
        )

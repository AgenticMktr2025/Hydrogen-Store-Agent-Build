import reflex as rx
from github import Github


class GitHubService:
    def __init__(self, token: str):
        self.gh = Github(token)

    def create_repository(self, name: str, description: str, private: bool = True):
        pass

    def create_file(self, repo_full_name: str, path: str, content: str, message: str):
        pass

    def create_pull_request(
        self, repo_full_name: str, title: str, body: str, branch: str
    ):
        pass

    def get_repository(self, full_name: str):
        return self.gh.get_repo(full_name)
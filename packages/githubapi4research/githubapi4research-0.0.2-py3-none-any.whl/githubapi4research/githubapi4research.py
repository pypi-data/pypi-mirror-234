from abc import ABC, abstractmethod
import os

class GithubAPI4Research(ABC):
    def __init__(self, api_token, repo_owner, repo_name, to_dir, to_file):
        self.api_token = api_token
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.to_dir = to_dir
        self.to_file = to_file

        print(f"repo owner : {repo_owner}, repo_name : {repo_name}")

        if not os.path.exists(to_dir):
            os.mkdir(to_dir)
    
    @abstractmethod
    def get(self, start_time=None, end_time=None, checkpoint=200, author=None):
        pass

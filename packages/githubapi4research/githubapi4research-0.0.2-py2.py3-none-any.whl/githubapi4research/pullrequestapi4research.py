import os
import json
import requests
import urllib3
from githubapi4research.githubapi4research import GithubAPI4Research

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class PullRequestAPI4Research(GithubAPI4Research):
    def get(self, start_time=None, end_time=None, checkpoint=200):
        json_list = []
        index = 0

        if os.path.exists(f"{self.to_dir}/{self.repo_name}PullRequestIndexTmp.log"):
            with open(f"{self.to_dir}/{self.repo_name}PullRequestIndexTmp.log") as fp:
                index = int(fp.readline())
        
        if os.path.exists(f"{self.to_dir}/{self.to_file}"):
            with open(f"{self.to_dir}/{self.to_file}", "r", encoding='utf-8') as fp:
                json_list = json.load(fp=fp)

        while True:
            try:
                url = "https://api.github.com/repos/{}/{}/pulls?state=all&per_page=100&page={}".format(self.repo_owner, self.repo_name, index)
                print(url)
                response = requests.get(url=url, headers={'Authorization': 'token {}'.format(self.api_token)}, verify=False)

                response.raise_for_status()
                if response.status_code == requests.codes.ok:
                    response_json_list = response.json()
                    if len(response.json()) > 0:
                        json_list = json_list + response_json_list
                        index += 1
                    else:
                        print("Get all PullRequests successfully") 
                        break
                else:
                    print("Stop to get PullRequests due to {}".format(response.text))
                    break
                
            except requests.exceptions.RequestException or requests.exceptions.ConnectionError as e:
                continue

            if index != 0 and index % checkpoint == 0:
                with open(f"{self.to_dir}/{self.repo_name}PullRequestIndexTmp.log", "w", encoding='utf-8') as fp:
                    fp.write(str(index))

                with open(f"{self.to_dir}/{self.to_file}", "w", encoding='utf-8') as fp:
                    json.dump(json_list, fp=fp, indent=4)
        
        if os.path.exists(f"{self.to_dir}/{self.repo_name}PullRequestIndexTmp.log"):
            os.remove(f"{self.to_dir}/{self.repo_name}PullRequestIndexTmp.log")
        
        with open(f"{self.to_dir}/{self.to_file}", "w", encoding='utf-8') as fp:
            json.dump(json_list, fp=fp, indent=4)
        
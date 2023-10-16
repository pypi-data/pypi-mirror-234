import os
import json
import requests
import urllib3
from githubapi4research.githubapi4research import GithubAPI4Research

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CommitCommentsAPI4Research(GithubAPI4Research):
    def get(self, start_time=None, end_time=None, checkpoint=200, author=None):
        json_list = []
        index = 0
        if start_time is None:
            url = "https://api.github.com/repos/{}/{}".format(self.repo_owner, self.repo_name)
            print("get " + url + " start_time")
            response = requests.get(url=url, headers={'Authorization': 'token {}'.format(self.api_token)}, verify=False)

            response.raise_for_status()
            if response.status_code == requests.codes.ok:
                start_time = response.json()['created_at']
                print("get " + url + " start_time successfully")
            else:
                print("get " + url + " start_time failed")
                return

        sinceTime = start_time

        if os.path.exists(f"{self.to_dir}/{self.repo_name}CommitCommentsIndexTmp.log"):
            with open(f"{self.to_dir}/{self.repo_name}CommitCommentsIndexTmp.log") as fp:
                line = fp.readline()
                index = int(line.split('#')[0])
                sinceTime = line.split('#')[1]
        
        if os.path.exists(f"{self.to_dir}/{self.to_file}"):
            with open(f"{self.to_dir}/{self.to_file}", "r", encoding='utf-8') as fp:
                json_list = json.load(fp=fp)

        while True:
            try:
                url = "https://api.github.com/repos/{}/{}/comments?state=all&per_page=100&page={}&sort=created&direction=asc&since={}".format(self.repo_owner, self.repo_name, index, sinceTime)
                print(url)
                response = requests.get(url=url, headers={'Authorization': 'token {}'.format(self.api_token)}, verify=False)

                response.raise_for_status()
                if response.status_code == requests.codes.ok:
                    response_json_list = response.json()
                    if len(response.json()) > 0:
                        json_list = json_list + response_json_list
                        print("Got 100 CommitComments from page {}".format(index)) 
                        index += 1
                    else:
                        print("Get all CommitComments successfully") 
                        break
                else:
                    print("Stop to get CommitComments due to {}".format(response.text))
                    break
                
            except requests.exceptions.RequestException or requests.exceptions.ConnectionError as e:
                continue

            #添加断点sinceTime保存
            if index != 0 and index % checkpoint == 0:
                index = 0
                sinceTime = json_list[-1]['created_at']
                with open(f"{self.to_dir}/{self.repo_name}CommitCommentsIndexTmp.log", "w", encoding='utf-8') as fp:
                    fp.write(str(index) + '#' + sinceTime)
                    print(index, sinceTime+"Save  successfully")

                with open(f"{self.to_dir}/{self.to_file}", "w", encoding='utf-8') as fp:
                    json.dump(json_list, fp=fp, indent=4)
        
        if os.path.exists(f"{self.to_dir}/{self.repo_name}CommitCommentsIndexTmp.log"):
            os.remove(f"{self.to_dir}/{self.repo_name}CommitCommentsIndexTmp.log")
        
        with open(f"{self.to_dir}/{self.to_file}", "w", encoding='utf-8') as fp:
            json.dump(json_list, fp=fp, indent=4)

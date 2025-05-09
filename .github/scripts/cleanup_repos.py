import os
import json
import re
from github import Github
import requests

def check_repo_exists(repo_url):
    """
    检查仓库是否存在
    :param repo_url: 仓库 URL
    :return: 如果仓库存在返回 True，否则返回 False
    """
    try:
        response = requests.head(repo_url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def remove_submodule(submodule_path):
    """
    移除 submodule
    :param submodule_path: submodule 的路径
    """
    if os.path.exists(submodule_path):
        os.system(f"git rm --cached {submodule_path}")
        os.system(f"rm -rf {submodule_path}")
        os.system(f"rm -rf .git/modules/{submodule_path}")
        print(f"Removed submodule: {submodule_path}")

def update_gitmodules(gitmodules_path, repo_name):
    """
    更新 .gitmodules 文件
    :param gitmodules_path: .gitmodules 文件路径
    :param repo_name: 仓库名称
    """
    with open(gitmodules_path, 'r') as f:
        content = f.read()

    pattern = re.compile(rf'\[submodule "{repo_name}"\]\n\tpath = (.*?)\n\turl = (.*?)\n')
    match = pattern.search(content)
    if match:
        submodule_path = match.group(1)
        content = pattern.sub('', content)
        with open(gitmodules_path, 'w') as f:
            f.write(content)
        print(f"Updated .gitmodules: removed entry for {repo_name}")
        return submodule_path
    return None

def update_directory_json(directory_json_path, repo_url):
    """
    更新 directory.json 文件
    :param directory_json_path: directory.json 文件路径
    :param repo_url: 仓库 URL
    """
    with open(directory_json_path, 'r') as f:
        data = json.load(f)

    updated_data = []
    for item in data:
        if item['url'] != repo_url:
            updated_data.append(item)

    with open(directory_json_path, 'w') as f:
        json.dump(updated_data, f, indent=2)
    print(f"Updated directory.json: removed entry for {repo_url}")

def main(location, project_link):
    github_token = os.getenv('GITHUB_TOKEN')
    g = Github(github_token)
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))

    gitmodules_path = '.gitmodules'
    directory_json_path = 'docs/directory.json'

    if not os.path.exists(gitmodules_path) or not os.path.exists(directory_json_path):
        print("Either .gitmodules or directory.json does not exist.")
        return

    with open(gitmodules_path, 'r') as f:
        content = f.read()

    pattern = re.compile(r'\[submodule "(.*?)"\]\n\tpath = (.*?)\n\turl = (.*?)\n')
    matches = pattern.findall(content)

    for repo_name, submodule_path, repo_url in matches:
        if repo_url == project_link and not check_repo_exists(repo_url):
            print(f"Repository {repo_url} is 404. Removing...")
            remove_submodule(submodule_path)
            update_gitmodules(gitmodules_path, repo_name)
            update_directory_json(directory_json_path, repo_url)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Cleanup repositories based on issue details.")
    parser.add_argument("--location", required=False, help="Location in collection")
    parser.add_argument("--project-link", required=False, help="Project link")
    args = parser.parse_args()

    main(args.location, args.project_link)

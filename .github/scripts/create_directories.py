import os
import json
from github import Github

def create_folder_structure(base_path, location):
    """
    创建文件夹结构
    :param base_path: 基础路径，例如 'projects'
    :param location: 位置字符串，例如 'cloud/aws'
    """
    full_path = os.path.join(base_path, location)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Created directory: {full_path}")
    else:
        print(f"Directory already exists: {full_path}")

def get_issue_details(github_token, issue_number):
    """
    获取 GitHub issue 的详细信息
    :param github_token: GitHub 访问令牌
    :param issue_number: issue 编号
    :return: issue 的 body 内容
    """
    g = Github(github_token)
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    issue = repo.get_issue(number=issue_number)
    return issue.body

def parse_issue_body(issue_body):
    """
    解析 issue body 并提取 location 和 project 链接
    :param issue_body: issue 的 body 内容
    :return: location 和 project 链接
    """
    lines = issue_body.split('\n')
    location = None
    project_link = None
    for line in lines:
        if line.startswith("location in collection:"):
            location = line.split(":")[1].strip()
        elif line.startswith("project link:"):
            project_link = line.split(":")[1].strip()
    return location, project_link

def main():
    github_token = os.getenv('GITHUB_TOKEN')
    issue_number = os.getenv('ISSUE_NUMBER')
    issue_body = get_issue_details(github_token, issue_number)
    location, project_link = parse_issue_body(issue_body)

    if location and project_link:
        create_folder_structure('projects', location)
    else:
        print("Location or project link not found in issue body.")

if __name__ == "__main__":
    main()
import os
import sys
import json
from github import Github

def get_issue_details(token, issue_number):
    g = Github(token)
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    issue = repo.get_issue(number=issue_number)
    return issue.body

def parse_issue_body(body):
    lines = body.split('\n')
    location = None
    project_link = None
    for line in lines:
        if line.startswith('location in collection'):
            location = line.split(':')[-1].strip()
        elif line.startswith('project link'):
            project_link = line.split(':')[-1].strip()
    return location, project_link

def update_gitmodules(location, project_link):
    with open('.gitmodules', 'a') as f:
        f.write(f'\n[submodule "{location}"]\n')
        f.write(f'    path = {location}\n')
        f.write(f'    url = {project_link}\n')

def main():
    token = os.getenv('GITHUB_TOKEN')
    issue_number_str = os.getenv('ISSUE_NUMBER')
    try:
        issue_number = int(issue_number_str)  # 将 issue_number 转换为整数类型
    except ValueError:
        print("ISSUE_NUMBER must be an integer.")
        sys.exit(1)
    
    body = get_issue_details(token, issue_number)
    location, project_link = parse_issue_body(body)
    if location and project_link:
        update_gitmodules(location, project_link)
        print("Updated .gitmodules successfully.")
    else:
        print("Failed to parse issue body.")
        sys.exit(1)

if __name__ == "__main__":
    main()
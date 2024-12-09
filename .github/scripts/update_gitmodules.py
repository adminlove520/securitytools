import os
import sys
import requests

def get_issue_details(token, owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        issue_data = response.json()
        return issue_data['body']
    else:
        raise Exception(f"Failed to get issue details: {response.status_code} {response.text}")

def parse_issue_body(body):
    lines = body.split('\n')
    location = None
    project_link = None
    for i in range(len(lines)):
        line = lines[i].strip()
        if line == '### location in collection':
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line:
                    location = next_line
                    break
        elif line == '### project link':
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line:
                    project_link = next_line
                    break
    return location, project_link

def update_gitmodules(location, project_link):
    with open('.gitmodules', 'a') as f:
        f.write(f'\n[submodule "{location}"]\n')
        f.write(f'    path = {location}\n')
        f.write(f'    url = {project_link}\n')

def main():
    token = os.getenv('GITHUB_TOKEN')
    owner = os.getenv('REPO_OWNER')  # 确保环境变量中有仓库所有者信息
    repo = os.getenv('REPO_NAME')    # 确保环境变量中有仓库名称信息
    issue_number_str = os.getenv('ISSUE_NUMBER')
    
    if not all([token, owner, repo, issue_number_str]):
        print("Environment variables GITHUB_TOKEN, REPO_OWNER, REPO_NAME, and ISSUE_NUMBER must be set.")
        sys.exit(1)
    
    try:
        issue_number = int(issue_number_str)
    except ValueError:
        print("ISSUE_NUMBER must be an integer.")
        sys.exit(1)
    
    try:
        body = get_issue_details(token, owner, repo, issue_number)
        location, project_link = parse_issue_body(body)
        if location and project_link:
            update_gitmodules(location, project_link)
            print("Updated .gitmodules successfully.")
        else:
            print("Failed to parse issue body.")
            sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
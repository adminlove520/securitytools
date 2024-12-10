import os
import sys
import requests
from github import Github

def get_issue_details(token, owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        issue_data = response.json()
        return issue_data
    else:
        print(f"Failed to get issue details: {response.status_code} {response.text}")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
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
    if not location or not project_link:
        print("Failed to parse issue body.")
        sys.exit(1)
    return location, project_link

def update_gitmodules(location, project_link):
    gitmodules_path = '.gitmodules'
    try:
        with open(gitmodules_path, 'a') as f:
            f.write(f'\n[submodule "{location}"]\n')
            f.write(f'    path = {location}\n')
            f.write(f'    url = {project_link}\n')
        print(f"Updated .gitmodules with location: {location} and project link: {project_link}")

        # 添加调试信息
        with open(gitmodules_path, 'r') as f:
            content = f.read()
            print(f"Current .gitmodules content:\n{content}")
    except IOError as e:
        print(f"Failed to write to .gitmodules: {e}")

def update_issue_comment(token, owner, repo, issue_number, issue_title, location):
    g = Github(token)
    repo = g.get_repo(f"{owner}/{repo}")
    issue = repo.get_issue(number=issue_number)
    
    comment_body = f"已成功将{issue_title} 添加至SecurityTools, 欢迎您的投稿\n"
    comment_body += f"项目位置: {location}\n"
    comment_body += "<p style='text-align: right;'>---东方隐侠安全团队·SecurityTools</p>"  # 使用 HTML 标签实现右对齐
    
    issue.create_comment(comment_body)
    print("Issue 更新成功")

def main():
    token = os.getenv('GITHUB_TOKEN')
    owner = os.getenv('REPO_OWNER')  # 确保环境变量中有仓库所有者信息
    repo = os.getenv('REPO_NAME')    # 确保环境变量中有仓库名称信息
    
    if not all([token, owner, repo]):
        print("Environment variables GITHUB_TOKEN, REPO_OWNER, and REPO_NAME must be set.")
        sys.exit(1)
    
    issue_number = int(os.getenv('ISSUE_NUMBER'))

    # 打印当前工作目录
    print(f"Current working directory: {os.getcwd()}")

    try:
        issue_details = get_issue_details(token, owner, repo, issue_number)
        body = issue_details['body']
        location, project_link = parse_issue_body(body)
        update_gitmodules(location, project_link)
        
        # 获取 issue title
        issue_title = issue_details['title']

        # 更新 Issue 评论
        update_issue_comment(token, owner, repo, issue_number, issue_title, location)

        # 设置输出变量
        with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
            print(f"location={location}", file=fh)
            print(f"project_link={project_link}", file=fh)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
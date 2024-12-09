import os
import sys
from github import Github

def get_issue_details(token, issue_number):
    g = Github(token)
    repo = g.get_repo(os.getenv('GITHUB_REPOSITORY'))
    issue = repo.get_issue(number=issue_number)
    print(f"Issue body: {issue.body}")  # 调试输出
    return issue.body

def parse_issue_body(body):
    lines = body.split('\n')
    location = None
    project_link = None
    for i in range(len(lines)):
        line = lines[i].strip()
        print(f"Processing line: {line}")  # 调试输出
        if line == '### location in collection':
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                print(f"Next line: {repr(next_line)}")  # 调试输出，使用 repr 查看字符串内容
                if next_line:
                    location = next_line
                    print(f"Parsed location: {location}")  # 调试输出
                    break
            else:
                print("No non-empty line after '### location in collection'")  # 调试输出
        elif line == '### project link':
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                print(f"Next line: {repr(next_line)}")  # 调试输出，使用 repr 查看字符串内容
                if next_line:
                    project_link = next_line
                    print(f"Parsed project_link: {project_link}")  # 调试输出
                    break
            else:
                print("No non-empty line after '### project link'")  # 调试输出
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
        print(f"Converted issue_number: {issue_number}")  # 调试输出
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
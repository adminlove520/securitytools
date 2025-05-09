import os
import json
import re
import argparse
import datetime  # 新增：用于记录时间
from github import Github
import requests  # 注：若无需其他功能可移除 requests 导入

def remove_submodule(submodule_path):
    """
    移除 submodule（Windows 强制删除，修复路径空格问题）
    :param submodule_path: submodule 的路径
    """
    if os.path.exists(submodule_path):
        # 关键修改：用双引号包裹路径，避免空格/特殊字符导致的命令解析错误
        os.system(f'git rm --cached "{submodule_path}"')  # git rm 也需要包裹路径
        os.system(f'rmdir /s /q "{submodule_path}"')  # rd 命令包裹路径
        # 注意：.git/modules 路径中的反斜杠需转义，同时包裹路径
        os.system(f'rmdir /s /q ".git\\modules\\{submodule_path}"')
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

def main():
    parser = argparse.ArgumentParser(description='手动清理指定失败仓库的子模块')
    parser.add_argument('repo_url', type=str, help='需要清理的仓库 URL（手动传入）')
    args = parser.parse_args()
    target_url = args.repo_url

    root_dir = os.path.abspath(os.getcwd())
    gitmodules_path = os.path.join(root_dir, '.gitmodules')
    directory_json_path = os.path.join(root_dir, 'docs', 'directory.json')
    log_dir = os.path.join(root_dir, "logs")  # 日志目录路径
    os.makedirs(log_dir, exist_ok=True)  # 创建日志目录（若不存在）

    if not os.path.exists(gitmodules_path) or not os.path.exists(directory_json_path):
        # 记录错误日志
        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log = f"{log_time} - 仓库URL: {target_url} - 删除原因: .gitmodules 或 directory.json 文件不存在，清理失败\n"
        with open(os.path.join(log_dir, "404_repos.log"), "a", encoding="utf-8") as log_file:
            log_file.write(error_log)
        print("错误：.gitmodules 或 directory.json 文件不存在")
        return

    with open(gitmodules_path, 'r') as f:
        content = f.read()
    pattern = re.compile(r'\[submodule "(.*?)"\]\n\tpath = (.*?)\n\turl = (.*?)\n')
    matches = pattern.findall(content)

    found = False
    for repo_name, submodule_path, repo_url in matches:
        if repo_url == target_url:
            print(f"找到目标仓库 {repo_url}，开始清理...")
            
            # 调整执行顺序：先更新 directory.json 和 .gitmodules，最后删除目录
            update_directory_json(directory_json_path, repo_url)  # 先更新 directory.json
            update_gitmodules(gitmodules_path, repo_name)         # 再更新 .gitmodules
            remove_submodule(submodule_path)                      # 最后删除子模块目录
            
            # 记录成功日志（所有步骤完成后记录）
            log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            success_log = f"{log_time} - 仓库URL: {target_url} - 删除原因: 仓库克隆失败，执行清理\n"
            with open(os.path.join(log_dir, "404_repos.log"), "a", encoding="utf-8") as log_file:
                log_file.write(success_log)
                
            found = True
            break

    if not found:
        # 记录未找到日志
        log_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        not_found_log = f"{log_time} - 仓库URL: {target_url} - 删除原因: 未在 .gitmodules 中找到对应子模块，清理失败\n"
        with open(os.path.join(log_dir, "404_repos.log"), "a", encoding="utf-8") as log_file:
            log_file.write(not_found_log)
        print(f"错误：未在 .gitmodules 中找到 URL 为 {target_url} 的子模块")

if __name__ == "__main__":
    main()

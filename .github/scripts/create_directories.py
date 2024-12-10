import os
import subprocess

def create_folder_structure(base_path, location):
    """
    创建文件夹结构
    :param base_path: 基础路径，例如 'projects'
    :param location: 位置字符串，例如 'cloud/aws/repo-name'
    """
    # 拆分 location 为文件夹路径和子模块名称
    parts = location.rsplit('/', 1)
    if len(parts) == 2:
        folder_path, submodule_name = parts
    else:
        folder_path = ''
        submodule_name = parts[0]

    full_folder_path = os.path.join(base_path, folder_path)
    
    # 创建文件夹路径
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)
        print(f"Created directory: {full_folder_path}")
    else:
        print(f"Directory already exists: {full_folder_path}")

    # 创建子模块路径
    full_submodule_path = os.path.join(full_folder_path, submodule_name)
    if not os.path.exists(full_submodule_path):
        os.makedirs(full_submodule_path)
        print(f"Created submodule directory: {full_submodule_path}")
    else:
        print(f"Submodule directory already exists: {full_submodule_path}")

def add_submodule(base_path, location, project_link):
    """
    添加子模块
    :param base_path: 基础路径，例如 'projects'
    :param location: 位置字符串，例如 'cloud/aws/repo-name'
    :param project_link: 子模块的 URL
    """
    # 拆分 location 为文件夹路径和子模块名称
    parts = location.rsplit('/', 1)
    if len(parts) == 2:
        folder_path, submodule_name = parts
    else:
        folder_path = ''
        submodule_name = parts[0]

    full_folder_path = os.path.join(base_path, folder_path)
    full_submodule_path = os.path.join(full_folder_path, submodule_name)

    # 确保二级文件夹存在
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)
        print(f"Created directory: {full_folder_path}")

    # 切换到二级目录并添加子模块
    if not os.path.exists(os.path.join(full_submodule_path, '.git')):
        try:
            os.chdir(full_folder_path)
            subprocess.run(['git', 'submodule', 'add', project_link, submodule_name], check=True)
            print(f"Added submodule: {submodule_name} at {full_submodule_path}")
        finally:
            os.chdir('..')  # 返回上一级目录
    else:
        print(f"Submodule already exists: {full_submodule_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create directories based on issue details.")
    parser.add_argument("--location", required=True, help="Location in collection")
    parser.add_argument("--project-link", required=True, help="Project link")
    args = parser.parse_args()

    # 移除 main 函数的调用
    # main(args.location, args.project_link)
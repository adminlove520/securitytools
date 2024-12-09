import os
import argparse

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

def main():
    parser = argparse.ArgumentParser(description="Create directories based on issue details.")
    parser.add_argument("--location", required=True, help="Location in collection")
    parser.add_argument("--project-link", required=True, help="Project link")
    args = parser.parse_args()

    location = args.location
    project_link = args.project_link

    create_folder_structure('projects', location)

if __name__ == "__main__":
    main()
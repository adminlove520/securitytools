import os

def add_gitkeep_in_folders(base_path):
    for root, dirs, files in os.walk(base_path):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            gitkeep_path = os.path.join(dir_path, '.gitkeep')
            if not os.path.exists(gitkeep_path):
                with open(gitkeep_path, 'w') as f:
                    f.write("")
                print(f"Added .gitkeep to {dir_path}")

if __name__ == "__main__":
    base_path = "projects"
    add_gitkeep_in_folders(base_path)
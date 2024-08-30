import yaml
import re
import os


def validate_yaml_files():
    yaml_files = [
        '.github/ISSUE_TEMPLATE/add_app.yml',
        '.github/ISSUE_TEMPLATE/edit_app.yml'
    ]

    for file_path in yaml_files:
        with open(file_path, 'r') as file:
            try:
                yaml.safe_load(file)
            except yaml.YAMLError as e:
                print(f"Error in {file_path}: {e}")
                return False
    return True


def validate_markdown_files():
    markdown_files = ['README.md', 'code-of-conduct.md']

    for file_path in markdown_files:
        with open(file_path, 'r') as file:
            content = file.read()
            if not re.search(r'^# ', content, re.MULTILINE):
                print(f"Error in {file_path}: Missing top-level heading")
                return False
    return True


def validate_license():
    with open('LICENSE', 'r') as file:
        content = file.read()
        if 'Creative Commons Attribution-NonCommercial-ShareAlike' not in content:
            print("Error in LICENSE: Invalid license content")
            return False
    return True


def main():
    if not validate_yaml_files():
        exit(1)
    if not validate_markdown_files():
        exit(1)
    if not validate_license():
        exit(1)
    print("All files are valid!")


if __name__ == "__main__":
    main()

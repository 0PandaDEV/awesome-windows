import yaml
import re
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def validate_yaml_files():
    yaml_files = [
        '.github/ISSUE_TEMPLATE/add_app.yml',
        '.github/ISSUE_TEMPLATE/edit_app.yml'
    ]

    all_valid = True
    for file_path in yaml_files:
        with open(file_path, 'r') as file:
            try:
                yaml.safe_load(file)
                logger.info(f"YAML file {file_path} is valid.")
            except yaml.YAMLError as e:
                logger.error(f"Error in {file_path}: {e}")
                logger.info("Please check the YAML syntax and fix any issues.")
                all_valid = False
    return all_valid

def validate_markdown_files():
    markdown_files = ['README.md', 'code-of-conduct.md']
    
    all_valid = True
    for file_path in markdown_files:
        with open(file_path, 'r') as file:
            content = file.read()
            if not re.search(r'^#+ ', content, re.MULTILINE):
                logger.error(f"Error in {file_path}: Missing heading at the start of the file")
                logger.info(f"Please add a heading (e.g., # Title) at the beginning of {file_path}")
                all_valid = False
            else:
                logger.info(f"Markdown file {file_path} has a valid heading.")
    return all_valid

def validate_license():
    with open('LICENSE', 'r') as file:
        content = file.read()
        if 'Creative Commons Attribution-NonCommercial-ShareAlike' not in content:
            logger.error("Error in LICENSE: Invalid license content")
            logger.info("Please ensure the LICENSE file contains the correct Creative Commons Attribution-NonCommercial-ShareAlike license text.")
            return False
        else:
            logger.info("LICENSE file contains valid license content.")
    return True

def main():
    yaml_valid = validate_yaml_files()
    markdown_valid = validate_markdown_files()
    license_valid = validate_license()

    if not (yaml_valid and markdown_valid and license_valid):
        logger.error("Validation failed. Please fix the issues mentioned above.")
        exit(1)
    logger.info("All files are valid!")

if __name__ == "__main__":
    main()

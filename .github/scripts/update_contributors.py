import os
import re
import requests


def get_contributors():
    headers = {'Authorization': f"token {os.environ.get('GITHUB_PAT')}"}
    repo = os.environ.get('GITHUB_REPOSITORY')
    response = requests.get(
        f'https://api.github.com/repos/{repo}/contributors', headers=headers)
    return [contributor for contributor in response.json() if contributor['login'] != 'actions-user']


def has_contributors_changed(contributors):
    with open('README.md', 'r') as file:
        content = file.read()

    for contributor in contributors:
        username = contributor['login']
        if f"https://github.com/{username}" not in content:
            return True
    return False


def update_readme(contributors):
    with open('README.md', 'r') as file:
        content = file.read()

    contributor_section = "## Backers\n\nThanks to all contributors without you this project would not exist.\n\n"

    for contributor in contributors:
        avatar_url = contributor['avatar_url']
        rounded_avatar_url = f"https://images.weserv.nl/?url={
            avatar_url}&fit=cover&mask=circle&maxage=7d"
        username = contributor['login']
        contributor_section += f"<a href='https://github.com/{username}'><img src='{
            rounded_avatar_url}' width='60' height='60' alt='{username}'/></a> "

    contributor_section += "\n\n"
    contributor_section += "Please, consider supporting me as it is a lot of work to maintain this list! Thanks a lot.\n\n"
    contributor_section += "<a href=\"https://buymeacoffee.com/pandadev_\"><img src=\"https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black\"/></a>"

    pattern = r"(#{1,6}\s+Backers[\s\S]*?)(?=\n\[|$)"
    updated_content = re.sub(
        pattern, contributor_section, content, count=1, flags=re.MULTILINE)
    with open('README.md', 'w') as file:
        file.write(updated_content)


if __name__ == "__main__":
    contributors = get_contributors()
    if has_contributors_changed(contributors):
        update_readme(contributors)
        print("Contributors updated")
    else:
        print("No changes in contributors")

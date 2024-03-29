import subprocess
import yaml
import re
from typing import List, Dict, Optional

DEFAULT_CONFIG = {
    'groups': [
        {
            'title': "💥 Breaking changes",
            'regexp': '^.*?(feat|chore|fix)!(?:\(\w+\))?!?: .+$',
            'order': 50
        },
        {
            'title': "🚀 New Features",
            'regexp': '^.*?feat(?:\(\w+\))?!?: .+$',
            'order': 100
        },
        {
            'title': "📦 Dependency updates",
            'regexp': '^.*?chore(?:\(\w+\))?!?: .+$',
            'order': 300
        },
        {
            'title': "⚠️ Security updates",
            'regexp': '^.*?sec(?:\(\w+\))?!?: .+$',
            'order': 150
        },
        {
            'title': "🐛 Bug fixes",
            'regexp': '^.*?(fix|refactor)(?:\(\w+\))?!?: .+$',
            'order': 200
        },
        {
            'title': "🔨 Refactoring",
            'regexp': '^.*?refactor(?:\(\w+\))?!?: .+$',
            'order': 250
        },
        {
            'title': "♻️ Revert changes",
            'regexp': '^.*?revert(?:\(\w+\))?!?: .+$',
            'order': 250
        },
        {
            'title': "📚 Documentation updates",
            'regexp': '^.*?docs(?:\(\w+\))?!?: .+$',
            'order': 400
        },
        {
            'title': "🏗️ Build process updates",
            'regexp': '^.*?(build|ci)(?:\(\w+\))?!?: .+$',
            'order': 400
        },
        {
            'title': "🧰 Other work",
            'order': 9999
        }
    ]
}


def run_command(command: List[str]) -> str:
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()


def run_command_list(command: List[str]) -> List[str]:
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')


def classify_commits(commits: List[str], groups: List[Dict[str, Optional[str]]]) -> Dict[str, List[str]]:
    classified_commits = {group['title']: [] for group in groups}
    classified_commits['🧰 Other work'] = []

    for commit in commits:
        matched = False
        for group in groups:
            regexp = group.get('regexp')
            if regexp and commit and commit.strip() and re.match(regexp, commit):
                classified_commits[group['title']].append(commit)
                matched = True
                break

        if not matched:
            classified_commits['🧰 Other work'].append(commit)

    return classified_commits


def replace_pull_requests(message, repo_url):
    def replace(match):
        pull_number = match.group(1)
        return f'in ({repo_url}/pull/{pull_number})'

    return re.sub(r'\(#(\d+)\)$', replace, message)


def generate_markdown(classified_commits, lower_tag, upper_tag, repo_url):
    markdown = "## Changelog\n"
    pattern = r'^([a-f0-9]+) (.+?) @(.+?) (\(tag: (.+?)\))?$'

    for title, commits in classified_commits.items():
        if commits:
            markdown += "### {}\n".format(title)
            for commit in commits:
                match = re.match(pattern, commit)
                if match:
                    sha, rest, author, _, tags = match.groups()
                    rest = replace_pull_requests(rest, repo_url)

                    # Modification pour gérer plusieurs tags
                    tag_list = tags.split(', ') if tags else []
                    tags_info = " {}".format(' '.join(
                        [f'[🏷 {tag}]({repo_url}/tree/{tag.replace("tag: ", "")})' for tag in
                         tag_list])) if tag_list else ""

                    # Modification pour générer des liens sans " tag: "
                    tags_info = tags_info.replace(" tag: ", "")

                    markdown += "* {}: {} by (@{}){}\n".format(sha, rest, author, tags_info)
            markdown += "\n"

    markdown += "**Full Changelog**: {}/compare/{}...{}".format(repo_url, lower_tag, upper_tag)
    return markdown


def load_user_config(file_path):
    try:
        with open(file_path, 'r') as config_file:
            return yaml.safe_load(config_file)
    except FileNotFoundError:
        return {}

def merge_configs(default_config, user_config):
    merged_config = default_config.copy()
    merged_config.update(user_config)
    return merged_config

def main():
    lower_tag = "base-v1.0.1"
    upper_tag = "base-v1.1.1"
    repo_url = "https://github.com/ixxeL-DevOps/docker-images"

    config_file = ".config-changelog.yml"

    user_config = load_user_config(config_file)
    config = merge_configs(DEFAULT_CONFIG, user_config)

    commits = run_command_list(['git', 'log', f'{lower_tag}..{upper_tag}', '--pretty=format:%H %s @%an %d'])

    classified_commits = classify_commits(commits, config['groups'])

    final_markdown = generate_markdown(classified_commits, lower_tag, upper_tag, repo_url)

    print(final_markdown)

    with open('CHANGELOG.md', 'w') as file:
        file.write(final_markdown)


if __name__ == "__main__":
    main()

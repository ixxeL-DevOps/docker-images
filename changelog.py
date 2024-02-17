#!/usr/bin/env python3
import subprocess
import yaml
import re
from typing import List, Dict, Optional


def run_command(command: List[str]) -> str:
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()


def run_command_list(command: List[str]) -> List[str]:
    result = subprocess.run(command, stdout=subprocess.PIPE, text=True)
    return result.stdout.strip().split('\n')


def classify_commits(commits: List[str], groups: List[Dict[str, Optional[str]]]) -> Dict[str, List[str]]:
    classified_commits = {group['title']: [] for group in groups}

    for commit in commits:
        for group in groups:
            regexp = group['regexp']
            # print("regexp", regexp)
            if commit and commit.strip() and bool(re.match(regexp, commit)):
                print(f"found commit {commit} in group {group['title']}")
                classified_commits[group['title']].append(commit)

    return classified_commits


def get_repo_url():
    # Exécute la commande 'git' pour obtenir l'URL du repo
    command_result = run_command(['git', 'config', '--get', 'remote.origin.url'])
    pattern = '^(https?://[^/]+/[^/]+/[^/]+)\.git$'

    if command_result:
        # Extrayez l'URL du repo à partir de la sortie de la commande git
        repo_url_match = re.match(pattern, command_result[0])
        if repo_url_match:
            return repo_url_match.group(1)

    return None

def replace_pull_requests(message, repo_url):
    # Fonction de rappel pour remplacer dynamiquement le modèle (#<nombre>)
    def replace(match):
        pull_number = match.group(1)
        return f'in {repo_url}/pull/{pull_number}'

    # Recherche et remplace le modèle (#<nombre>) en utilisant la fonction de rappel
    return re.sub(r'\(#(\d+)\)$', replace, message)

# def generate_markdown(classified_commits: Dict[str, List[str]]) -> str:
#     markdown = "## Changelog\n"
#
#     for title, commits in classified_commits.items():
#         if commits:
#             markdown += f"### {title}\n"
#             markdown += "\n".join(commits) + "\n\n"
#
#     return markdown

def generate_markdown(classified_commits):
    markdown = "## Changelog\n"
    pattern = '^([a-f0-9]+) (.+)$'

    for title, commits in classified_commits.items():
        if commits:
            markdown += f"### {title}\n"
            for commit in commits:
                match = re.match(pattern, commit)
                if match:
                    sha, rest = match.groups()
                    print("sha", sha)
                    print("rest", rest)
                    rest = replace_pull_requests(rest, get_repo_url())
                    markdown += f"* {sha}: {rest}\n"
            markdown += "\n"

    return markdown


def main():
    # Tags de borne inférieure et supérieure
    lower_tag = "base-v1.0.1"
    upper_tag = "helm-v0.1.0"

    # Fichier de configuration pour le changelog
    config_file = "config.yaml"

    # Récupérer les commits entre les tags spécifiés
    commits = run_command_list(['git', 'log', f'{lower_tag}..{upper_tag}', '--pretty=format:%H %s'])
    # print(f"Commits between {lower_tag} and {upper_tag}:")
    # for commit in commits:
    #     print(commit)

    with open(config_file, 'r') as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)

    # Classer les commits en fonction des règles de classification définies dans la configuration
    classified_commits = classify_commits(commits, config['groups'])

    # Générer le markdown à partir des commits classés
    final_markdown = generate_markdown(classified_commits)

    # Imprimer le markdown
    print(final_markdown)

    with open('CHANGELOG.md', 'w') as file:
        file.write(final_markdown)


if __name__ == "__main__":
    main()

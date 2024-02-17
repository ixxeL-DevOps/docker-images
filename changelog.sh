#!/bin/bash

# Tags de borne inférieure et supérieure
LOWER_TAG="base-v1.0.1"
UPPER_TAG="builder-v0.1.0"

# Fichier de configuration pour le changelog
CONFIG_FILE=".config.yaml"

# Récupérer les commits entre les tags spécifiés
commits=$(git log ${LOWER_TAG}..${UPPER_TAG} --pretty=format:"%h %s")

# Lire la configuration du changelog
sort_type=$(yq eval '.sort' ${CONFIG_FILE})
use_type=$(yq eval '.use' ${CONFIG_FILE})

# Fonction pour filtrer les commits en fonction des règles
filter_commits() {
    local commits=$1
    local filters=($2)
    local filtered_commits=""

    for commit in ${commits[@]}; do
        include_commit=true
        for filter in ${filters[@]}; do
            if [[ ${commit} =~ ${filter} ]]; then
                include_commit=false
                break
            fi
        done
        if [ ${include_commit} = true ]; then
            filtered_commits+="${commit}\n"
        fi
    done

    echo -e "${filtered_commits}"
}

# Fonction pour trier les commits
sort_commits() {
    local sort_type=$1
    local commits=$2

    if [ ${sort_type} = "asc" ]; then
        echo -e "${commits}" | sort
    elif [ ${sort_type} = "desc" ]; then
        echo -e "${commits}" | sort -r
    else
        echo "Type de tri non reconnu."
        exit 1
    fi
}

# Fonction pour générer le changelog en markdown
generate_changelog() {
    local commits=$1
    local groups=($2)
    local changelog=""

    for group in "${groups[@]}"; do
        title=$(yq eval ".groups[].title" ${CONFIG_FILE})
        regexp=$(yq eval ".groups[].regexp" ${CONFIG_FILE})
        order=$(yq eval ".groups[].order" ${CONFIG_FILE})

        filtered_commits=$(filter_commits "${commits}" "${regexp}")
        sorted_commits=$(sort_commits "${sort_type}" "${filtered_commits}")

        if [ -n "${sorted_commits}" ]; then
            changelog+="## ${title}\n${sorted_commits}\n\n"
        fi
    done

    echo -e "${changelog}"
}

# Générer le changelog
final_changelog=$(generate_changelog "${commits}" groups)

# Ajouter le contenu au modèle Markdown
final_changelog="## Upgrading\n\nThis project uses the semver versioning and ensures that following rules:\n\nThe patch release does not introduce any breaking changes. So if you are upgrading from ${LOWER_TAG} to ${UPPER_TAG} there should be no special instructions to follow.\nThe minor release might introduce minor changes with a workaround. If you are upgrading from ${LOWER_TAG} to ${UPPER_TAG} please make sure to check upgrading details in both ${LOWER_TAG} to v1.4 and ${UPPER_TAG} to v1.5 upgrading instructions.\nThe major release introduces backward incompatible behavior changes. It is recommended to take a backup using disaster recovery guide.\n\n## Changelog\n\n${final_changelog}**Full Changelog**: https://github.com/ixxeL-actions/tbd-from-trunk/compare/${LOWER_TAG}...${UPPER_TAG}\n\n## Helping out\n\nThis release is only possible thanks to **all** the support of some **awesome people**!\n\nWant to be one of them?"

# Imprimer le changelog
echo -e "${final_changelog}" > CHANGELOG.md

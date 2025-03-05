# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: Kaniko must be root to work
# checkov:skip=CKV_DOCKER_8: Kaniko must be root to work
ARG BASE_REGISTRY

FROM summerwind/actions-runner:ubuntu-22.04 AS builder

USER root

COPY ./pki_root_ca.pem /usr/local/share/ca-certificates/root.crt
COPY ./pki_int_ca.pem /usr/local/share/ca-certificates/int.crt

RUN apt-get update && \
    apt-get install -y \
    git \
    curl \
    wget \
    apt-transport-https \
    ca-certificates \
    python3-pip \
    tar \
    gettext 

RUN curl -fsSL "https://cli.github.com/packages/githubcli-archive-keyring.gpg" | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    curl "https://baltocdn.com/helm/signing.asc" | gpg --dearmor | tee /usr/share/keyrings/helm.gpg > /dev/null && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    curl -fsSL "https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key" | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg > /dev/null && \
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list && \
    apt-get update && \
    apt-get install -y \
    helm \
    gh \
    kubectl

RUN wget -qO /usr/local/bin/yq "https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64" && \
    chmod a+x /usr/local/bin/yq && \
    wget -qO /usr/local/bin/argocd "https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64" && \
    chmod a+x /usr/local/bin/argocd && \
    HELMDOC_VERSION=$(curl -sSfL "https://github.com/norwoodj/helm-docs/releases/latest" | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq | tail -1) && \
    HELMDOC_VER_LIGHT=$(echo "$HELMDOC_VERSION" | sed 's/v//g') && \
    curl -sSfL "https://github.com/norwoodj/helm-docs/releases/download/${HELMDOC_VERSION}/helm-docs_${HELMDOC_VER_LIGHT}_Linux_x86_64.tar.gz" | tar -xz && \
    mv ./helm-docs /usr/local/bin && \
    wget -qO /usr/local/bin/hadolint "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64" && \
    VALIDATOR_VERSION=$(curl -sSfL "https://github.com/mpalmer/action-validator/releases" | grep -oE "v[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}" | uniq | sort -rV | head -1) && \
    wget -qO /usr/local/bin/action-validator "https://github.com/mpalmer/action-validator/releases/download/${VALIDATOR_VERSION}/action-validator_linux_amd64"

RUN pip3 install --no-cache-dir --upgrade checkov pre-commit && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    update-ca-certificates

USER runner  

RUN helm plugin install "https://github.com/chartmuseum/helm-push" && \
    helm plugin install "https://github.com/datreeio/helm-datree" && \
    helm plugin install "https://github.com/helm-unittest/helm-unittest" && \
    helm plugin install "https://github.com/melmorabity/helm-kubeconform"

ENV HELM_PLUGINS=/home/runner/.local/share/helm/plugins

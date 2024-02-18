# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: Kaniko must be root to work
# checkov:skip=CKV_DOCKER_8: Kaniko must be root to work
ARG BASE_REGISTRY
ARG KYVERNO_VERSION

FROM ${BASE_REGISTRY}alpine:latest AS builder

ENV KYVERNO_VERSION="v1.11.4"

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN --mount=type=cache,target=/var/cache/apk \
    apk update --no-cache --update && \
    apk add curl tar bash --no-cache --update && \
    curl -sSLO "https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64" && \
    chmod +x ./argocd-linux-amd64 && \
    mv ./argocd-linux-amd64 /usr/local/bin/argocd && \
    curl -sSfL "https://install-cli.jfrog.io" | sh && \
    curl -sSfLO "https://github.com/kyverno/kyverno/releases/download/${KYVERNO_VERSION}/kyverno-cli_${KYVERNO_VERSION}_linux_x86_64.tar.gz" && \
    tar -xzf kyverno-cli_${KYVERNO_VERSION}_linux_x86_64.tar.gz && \
    mv kyverno /usr/local/bin/kyverno && \
    curl -L -o vcluster "https://github.com/loft-sh/vcluster/releases/latest/download/vcluster-linux-amd64" && \
    install -c -m 0755 vcluster /usr/local/bin && rm -f vcluster && \
    curl -s https://fluxcd.io/install.sh | bash

FROM ${BASE_REGISTRY}moby/buildkit:master as buildkit

FROM ${BASE_REGISTRY}ixxel/musl-dns-hack-alpine:latest as dnshack

FROM ${BASE_REGISTRY}ixxel/toolbox:certs-latest AS cd-toolbox

LABEL org.opencontainers.image.title="cd-toolbox"
LABEL org.opencontainers.image.source="https://github.com/ixxeL-docker/docker-images/blob/main/src/cd/Dockerfile"

ENV PATH="/kaniko:$PATH"

COPY --from=buildkit /usr/bin/ /usr/bin/

COPY --from=gcr.io/kaniko-project/executor:latest /kaniko/executor /usr/local/bin/executor

COPY --from=builder /usr/local/bin/jf \
                    /usr/local/bin/argocd \
                    /usr/local/bin/kyverno \
                    /usr/local/bin/vcluster \
                    /usr/local/bin/flux \
                    /usr/local/bin/

RUN --mount=type=cache,target=/var/cache/apk \
    apk update --no-cache \
    && apk upgrade --no-cache \
    && apk add --no-cache --update \
    fuse3 fuse-overlayfs openssh pigz shadow-uidmap xz \
    buildah \
    skopeo \
    gettext \
    bind-tools

RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/community" \
    terraform \
    kustomize \
    cosign \
    vault \
    grype \
    syft \
    kubectl \
    podman && \
    sed -i 's/^#mount_program/mount_program/' /etc/containers/storage.conf

RUN apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/testing" \
    dive \
    trivy

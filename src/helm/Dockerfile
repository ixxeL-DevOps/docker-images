# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: GH actions must be root to work
# checkov:skip=CKV_DOCKER_8: GH actions must be root to work
ARG BASE_REGISTRY

FROM alpine:latest AS builder

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN --mount=type=cache,target=/var/cache/apk \
    apk update --no-cache --update && \
    apk add curl tar --no-cache --update && \
    HELMDOC_VERSION=$(curl -sSfL "https://github.com/norwoodj/helm-docs/releases/latest" | grep -oE 'v[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq | tail -1) && \
    HELMDOC_VER_LIGHT=$(echo "$HELMDOC_VERSION" | sed 's/v//g') && \
    curl -sSfL "https://github.com/norwoodj/helm-docs/releases/download/${HELMDOC_VERSION}/helm-docs_${HELMDOC_VER_LIGHT}_Linux_x86_64.tar.gz" | tar -xz && \
    mv ./helm-docs /usr/local/bin/helm-docs

FROM python:3.11-alpine3.21

ENV TZ="Europe/Paris"

LABEL maintainer="fredspiers@gmail.com"
LABEL org.opencontainers.image.authors="FSPIERS"
LABEL org.opencontainers.image.title="helm-toolbox"
LABEL org.opencontainers.image.source="https://github.com/ixxeL-docker/docker-images/blob/main/src/helm/Dockerfile"
LABEL org.opencontainers.image.base.name="python:3.11-alpine3.18"

COPY --from=builder /usr/local/bin/helm-docs \
                    /usr/local/bin/

RUN --mount=type=cache,target=/var/cache/apk \
    apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add --no-cache --update \
    curl \
    bash \
    jq \
    yq \
    git \
    util-linux \
    tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime

RUN apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/community" \
    helm \
    github-cli

RUN helm plugin install "https://github.com/chartmuseum/helm-push" && \
    helm plugin install "https://github.com/datreeio/helm-datree" && \
    helm plugin install "https://github.com/helm-unittest/helm-unittest" && \
    helm plugin install "https://github.com/melmorabity/helm-kubeconform"

RUN pip3 install --no-cache-dir --upgrade checkov

ENV HELM_PLUGINS=/root/.local/share/helm/plugins

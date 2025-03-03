# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: Buildkit must be root to work
# checkov:skip=CKV_DOCKER_8: Buildkit must be root to work
ARG BASE_REGISTRY

FROM moby/buildkit:master as buildkit

FROM python:3.12-alpine3.21

ENV TZ="Europe/Paris"

LABEL maintainer="fredspiers@gmail.com"
LABEL org.opencontainers.image.authors="FSPIERS"
LABEL org.opencontainers.image.title="builder-toolbox"
LABEL org.opencontainers.image.source="https://github.com/ixxeL-docker/docker-images/blob/main/src/builder/Dockerfile"
LABEL org.opencontainers.image.base.name="python:3.12-alpine3.21"

COPY --from=buildkit /usr/bin/ /usr/bin/

RUN apk update --no-cache && \
    apk upgrade  --no-cache && \
    apk add --no-cache --update \
    fuse3 fuse-overlayfs openssh pigz shadow-uidmap xz \
    git \
    curl \
    bash \
    jq \
    yq \
    moreutils \
    util-linux \
    tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime

RUN apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/community" \
    grype \
    syft \
    cosign \
    helm \
    kubectl \
    github-cli \
    podman && \
    sed -i 's/^#mount_program/mount_program/' /etc/containers/storage.conf

RUN apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/testing" \
    dive

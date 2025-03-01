# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: GH pipelines require root containers
# checkov:skip=CKV_DOCKER_8: GH pipelines require root containers
ARG BASE_REGISTRY

FROM python:3.12-alpine3.21 as base

LABEL maintainer="fredspiers@gmail.com"
LABEL org.opencontainers.image.authors="F.SPIERS"
LABEL org.opencontainers.image.base.name="python:3.12-alpine3.21"

ENV TZ="Europe/Paris"
ENV TEST="toberemoved"

RUN --mount=type=cache,target=/var/cache/apk \
    apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add --no-cache --update \
    git \
    curl \
    bash \
    jq \
    yq \
    moreutils \
    util-linux \
    ca-certificates \
    tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime

RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/community" \
    helm \
    github-cli

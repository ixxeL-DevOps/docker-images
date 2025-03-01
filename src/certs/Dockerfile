# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: GH pipelines require root containers
# checkov:skip=CKV_DOCKER_8: GH pipelines require root containers
ARG BASE_REGISTRY

FROM python:3.11-alpine3.19 as certs

LABEL maintainer="fredspiers@gmail.com"
LABEL org.opencontainers.image.authors="F.SPIERS"
LABEL org.opencontainers.image.base.name="python:3.11-alpine3.19"

ENV TZ="Europe/Paris"

COPY ./pki_root_ca.pem /usr/local/share/ca-certificates/root.crt
COPY ./pki_int_ca.pem /usr/local/share/ca-certificates/int.crt

RUN apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add --no-cache --update \
    git \
    curl \
    bash \
    jq \
    yq \
    wget \
    moreutils \
    util-linux \
    ca-certificates \
    step-cli \
    tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    update-ca-certificates

RUN apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/community" \
    helm \
    github-cli

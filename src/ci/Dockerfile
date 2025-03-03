# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: GH actions must be root to work
# checkov:skip=CKV_DOCKER_8: GH actions must be root to work
ARG BASE_REGISTRY

FROM alpine:3.21 AS builder

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN apk update --no-cache && \
    apk add tar curl --no-cache --update && \
    curl -sSfLO "https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64" && \
    chmod +x hadolint-Linux-x86_64 && \
    mv ./hadolint-Linux-x86_64 /usr/local/bin/hadolint && \
    VALIDATOR_VERSION=$(curl -sSfL "https://github.com/mpalmer/action-validator/releases" | grep -oE "v[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}" | uniq | sort -rV | head -1) && \
    curl -sSfLO "https://github.com/mpalmer/action-validator/releases/download/${VALIDATOR_VERSION}/action-validator_linux_amd64" && \
    chmod +x action-validator_linux_amd64 && \
    mv ./action-validator_linux_amd64 /usr/local/bin/action-validator

FROM ixxel/toolbox:certs-latest AS cd-toolbox

LABEL org.opencontainers.image.title="ci-toolbox"
LABEL org.opencontainers.image.source="https://github.com/ixxeL-docker/docker-images/blob/main/src/ci/Dockerfile"

COPY --from=builder /usr/local/bin/hadolint /usr/local/bin/action-validator /usr/local/bin/

RUN apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add --no-cache --update \
    shellcheck \
    yamllint \
    black \
    make \
    gradle \
    yarn

RUN pip3 install --no-cache-dir --upgrade checkov pre-commit

# checkov:skip=CKV_DOCKER_2: This is not a running container. Its purpose is to be used in CI pipeline jobs
# checkov:skip=CKV_DOCKER_3: Kaniko must be root to work
# checkov:skip=CKV_DOCKER_8: Kaniko must be root to work
ARG BASE_REGISTRY

FROM ${BASE_REGISTRY}alpine:latest AS builder

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN apk update --no-cache \
    && apk add curl --no-cache --update \
    && K9S_VERSION=$(curl -sSfL "https://github.com/derailed/k9s/releases/latest" | grep -Eo "^\\s+v[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}\$" | sed 's/ //g' | sort -rV | uniq | head -1) \
    && curl -sSfL "https://github.com/derailed/k9s/releases/download/${K9S_VERSION}/k9s_Linux_amd64.tar.gz" | tar -xz \
    && mv ./k9s /usr/local/bin/k9s

FROM ${BASE_REGISTRY}ixxel/toolbox:cd-latest as aio

LABEL org.opencontainers.image.title="all-in-one-toolbox"
LABEL org.opencontainers.image.source="https://github.com/ixxeL-docker/docker-images/blob/main/src/aio/Dockerfile"

COPY --from=builder /usr/local/bin/k9s \
                    /usr/local/bin/

RUN --mount=type=cache,target=/var/cache/apk \
    apk update --no-cache && \
    apk upgrade --no-cache && \
    apk add --no-cache --update \
    unzip \
    fzf \
    bat \
    net-tools \
    openssl \
    icu-libs \
    gcompat

RUN apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/main" \
    fish

SHELL ["/bin/ash", "-eo", "pipefail", "-c"]
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache --update --repository="http://dl-cdn.alpinelinux.org/alpine/edge/community" \
    starship \
    && curl -s "https://ohmyposh.dev/install.sh" | bash -s \
    && helm plugin install "https://github.com/chartmuseum/helm-push" \
    && helm plugin install "https://github.com/databus23/helm-diff" \
    # && helm plugin install "https://github.com/datreeio/helm-datree" \
    && fish -c "curl -sL https://git.io/fisher | source && fisher install jorgebucaran/fisher" \
    && fish -c "fisher install jethrokuan/fzf" \
    && fish -c "fisher install evanlucas/fish-kubectl-completions" \
    && fish -c "fisher install danhper/fish-ssh-agent" \
    && mkdir -p /root/.ssh \
    && { \
    echo "#!/usr/bin/fish"; \
    echo "set -x; set temp_dir (mktemp -d); cd $temp_dir"; \
    echo "curl -fsSLO https://github.com/kubernetes-sigs/krew/releases/latest/download/krew-linux_amd64.tar.gz"; \
    echo "tar zxvf krew-linux_amd64.tar.gz"; \
    echo "./krew-linux_amd64 install krew"; \
    echo "set -e temp_dir"; \
    } > install-krew.sh \
    && fish -c "chmod +x ./install-krew.sh" \
    && fish -c "./install-krew.sh" \
    && fish -c "echo 'set -gx PATH $PATH $HOME/.krew/bin' >> ~/.config/fish/config.fish" \
    && fish -c "kubectl krew install ctx" \
    && fish -c "kubectl krew install ns" \
    && fish -c "kubectl krew install neat" \
    && fish -c "kubectl krew install datree" \
    && fish -c "kubectl krew install kyverno" \
    && fish -c "kubectl krew install whoami" \
    && fish -c "kubectl krew install cert-manager" \
    && fish -c "kubectl krew install ktop" \
    && fish -c "kubectl krew install spy" \
    && fish -c "kubectl krew install pod-lens" \
    && fish -c "kubectl krew install view-utilization" \
    && fish -c "kubectl krew install view-allocations" \
    && fish -c "kubectl krew install kc" \
    && fish -c "kubectl krew install gadget" \
    && { \
    echo "function k --wraps kubectl"; \
    echo '  kubectl $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/k.fish \
    && { \
    echo "function vk --wraps vcluster"; \
    echo '  vcluster $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/vk.fish \
    && { \
    echo "function keti --wraps=kubectl-exec-it"; \
    echo '  kubectl exec -it $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/keti.fish \
    && { \
    echo "function kd --wraps=kubectl-describe"; \
    echo '  kubectl describe $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/kd.fish \
    && { \
    echo "function kg --wraps=kubectl-get"; \
    echo '  kubectl get $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/kg.fish \
    && { \
    echo "function kgp --wraps=kubectl-get-pod"; \
    echo '  kubectl get pod $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/kgp.fish \
    && { \
    echo "function kgd --wraps=kubectl-get-deploy"; \
    echo '  kubectl get deploy $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/kgd.fish \
    && { \
    echo "function bat"; \
    echo '  command bat --paging=never $argv'; \
    echo "end"; \
    } > ~/.config/fish/functions/bat.fish

COPY ./config.fish /root/.config/fish/config.fish

COPY ./starship.toml /root/.config/starship.toml

COPY ./oh-my-theme.json /root/.config/oh-my-theme.json

RUN pip3 install --no-cache-dir --upgrade checkov python-gitlab ansible

ENV HELM_PLUGINS=/root/.local/share/helm/plugins
# ENTRYPOINT ["python", "-m", "http.server", "8080"]
ENTRYPOINT ["tail", "-f", "/dev/null"]

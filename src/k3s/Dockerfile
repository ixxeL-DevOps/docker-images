#FROM rancher/k3s:v1.0.0 as base
FROM rancher/k3s:v1.29.2-k3s1 as base

# https://github.com/rancher/k3s/issues/390
# Because of the above issue, we want to add
# some software into our container, and alpine
# is easier to work with than scratch.
#FROM alpine:3.10
FROM alpine:3.19

# Do the same stuff in the k3s-scratch image's
# final stage.
# https://github.com/rancher/k3s/blob/master/package/Dockerfile
COPY --from=base /tmp /tmp
COPY --from=base /run /run
COPY --from=base /etc /etc
COPY --from=base /var /var
COPY --from=base /lib /lib
COPY --from=base /bin /bin

RUN chmod 1777 /tmp
VOLUME /var/lib/kubelet
VOLUME /var/lib/rancher/k3s
VOLUME /var/lib/cni
VOLUME /var/log
ENV PATH="$PATH:/bin/aux"

# Add our patch to enable Kubelet to act as NFS client
# so our pods can use NFS volumes
# RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories \
#     && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
#     && apk update --no-cache \
#     && apk upgrade --no-cache \
#     && apk add --no-cache --update \
#     nfs-utils

# RUN echo "#!/bin/bash" > /entrypoint && \
# echo '\
# rpcbind -f & \n\
# /bin/k3s $@' >> /entrypoint && chmod +x /entrypoint

# ENTRYPOINT ["/entrypoint"]
# CMD ["agent"]

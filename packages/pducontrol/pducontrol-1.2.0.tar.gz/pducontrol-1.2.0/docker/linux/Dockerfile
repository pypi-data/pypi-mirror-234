ARG FROM_IMAGE
FROM ${FROM_IMAGE}
ARG CODENAME

ENV DEBIAN_FRONTEND="noninteractive"

RUN apt-get update && \
    apt-get install --yes --quiet --quiet \
        debhelper \
        devscripts \
        dh-python \
        python3-argcomplete \
        python3-argparse-manpage \
        python3-requests \
        python3-setuptools \
        python3-tabulate \
        python3-xmltodict \
        ronn \
    && \
    apt-get clean && \
    rm --recursive --force /var/lib/apt/lists/* /tmp/* /var/tmp/*

USER root
WORKDIR /root/workspace

ARG BASE_VERSION

FROM docker-regi.intra.yyyyy-it.com/pppppp/centos:${BASE_VERSION}

ARG CONDA_FILE_NAME
LABEL miniconda="${CONDA_FILE_NAME}"
# MINICONDA
RUN cd /tmp \
    && curl -kO https://repo.anaconda.com/miniconda/${CONDA_FILE_NAME} \
    && bash ${CONDA_FILE_NAME} -b -p /opt/conda \
    && rm /tmp/${CONDA_FILE_NAME} \
    && /opt/conda/bin/conda clean --all -y
ENV PATH="/opt/conda/bin:${PATH}"

RUN rpm -ivh http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-7-x86_64.rpm \
    && rpm -ivh http://packages.groonga.org/centos/groonga-release-1.1.0-1.noarch.rpm \
    && yum -y install --nogpgcheck \
        gcc \
        gcc-c++\
        \
        libcouchbase-devel \
        libcouchbase2-bin \
        libcouchbase2-libevent \
        \
        krb5-workstation \
        \
        attr \
        cyrus-sasl-devel \
        cyrus-sasl-gssapi \
        cyrus-sasl-lib \
        fuse \
        libibverbs \
        librdmacm \
        \
        mecab \
        mecab-devel \
        mecab-ipadic \
        \
        glusterfs-client \
        glusterfs-fuse \
        nfs-utils \
        psmisc \
        snappy-devel \
        wget \
        which \
        zip \
        sudo \
        \
        # swig \
    \
    && yum clean all \
    && rm -rf /var/cache/yum

RUN conda create --prefix /opt/python-runtime python=3.10.3
ENV PATH="/opt/python-runtime/bin:${PATH}"

ARG REQUIREMENTS=requirements.txt
COPY ${REQUIREMENTS} requirements.txt
RUN pip install --use-feature=2020-resolver --no-cache-dir --ignore-installed -r requirements.txt

USER pppppp
WORKDIR /opt/YAW-dashboards

COPY --chown=pppppp:pppppp src .

ENV PYTHONPATH="/opt/YAW-dashboards:$PYTHONPATH"
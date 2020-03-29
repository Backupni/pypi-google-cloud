FROM python:3.8.2-alpine3.11

RUN set -ex \
    && apk upgrade --no-cache \
    && python3 -m pip install --no-cache-dir --upgrade --upgrade-strategy=eager \
        setuptools \
        pip \
        wheel \
    && python3 -m pip install --no-cache-dir --upgrade --upgrade-strategy=eager \
        "dumb-pypi==1.4.0"

ENTRYPOINT ["dumb-pypi"]

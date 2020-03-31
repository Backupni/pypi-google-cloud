FROM python:3.8.2-alpine3.11

RUN set -ex \
    && apk upgrade --no-cache \
    && apk add --upgrade --no-cache --virtual .build-deps  \
        build-base \
        grpc-dev \
        linux-headers \
    && apk add --upgrade --no-cache  \
        grpc \
    && python3 -m pip install --no-cache-dir --upgrade --upgrade-strategy=eager \
        setuptools \
        pip \
        wheel \
    && python3 -m pip install --no-cache-dir --upgrade --upgrade-strategy=eager \
        "asgiref==3.2.5" \
        "google-cloud-secret-manager==0.2.0" \
        "google-cloud-storage==1.26.0" \
        "starlette==0.13.2" \
        "uvicorn==0.11.3" \
    && apk del .build-deps

COPY ./app /app

CMD ["uvicorn", "app.proxy:app", "--host", "0.0.0.0", "--port", "8080"]

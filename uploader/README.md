Uploader
========

This service uploads new packages to your storage and invokes Builder.

Implementation
--------------

- Cloud Build process
  - invokes `Builder` on success after uploading

How to use
----------

Invoke 

```
$ gcloud builds submit \
      'dist' \
      --substitutions='_WHL_NAME="my_package-0.1.0-py2.py3-none-any",_PACKAGES_BUCKET="pypi-packages-iobszb",_META_DATA_BUCKET="pypi-metadata-uogykq",_STATIC_BUCKET="packages-internal.example.com",_DOMAIN="packages.example.com"' \
      --config='uploader/cloudbuild.yaml' \
      --project='YOUR_PROJECT_ID'
```

on your CI after package test step.

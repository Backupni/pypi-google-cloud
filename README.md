Private PyPI - Google Cloud
===========================

Private PyPI repository on top of Google Cloud Platform. 

```

  _____   ______ _____ _    _ _______ _______ _______       _____  __   __  _____  _____
 |_____] |_____/   |    \  /  |_____|    |    |______      |_____]   \_/   |_____]   |
 |       |    \_ __|__   \/   |     |    |    |______      |          |    |       __|__


```

Project status: **beta** 

Feel free to open new issues in case of any errors.

Project Goals and Decisions
---------------------------

### Secure

- modular design
- simple components, without tons of unused code and API endpoints (code review should be easy)
- static whenever it possible

### Optimised for Google Cloud

- uses Google Cloud Platform for any related compute, storage or network operations to provide best user experience

### Best choice for Python perfectionists
- respects PEPs (PEP 503)
- uses tokens instead of username & passwords (follow PyPi suggestions)
- supports package hashes (hello, poetry)


Structure: Project Services and Components
------------------------------------------

Just 3 simple components.

### Storage

Storage is storage. This is the main component of the system.

- Cloud Storage bucket for Python wheel packages
- Cloud Storage bucket for [PEP 503](https://www.python.org/dev/peps/pep-0503/) implementation and json's with [package metadata](https://warehouse.readthedocs.io/api-reference/json) `pypi/*/json`
- Cloud Storage bucket for internal metadata for static site generator - package names, file hashes etc.


### Proxy

This component adds basic auth with tokens support and provides access to packages. Simple layer between Storage and end users.

- managed Google Cloud Run
- uses Python image with Starlette Python ASGI framework (it should be fast) ([GitHub repository](https://github.com/backupni/pypi-gcs-proxy-image))
- uses custom Service Account
- uses Google Cloud Secret for auth tokens storage
- (optional) uses custom domain name

### Builder / Uploader

This component uploads new packages to your storage and updates your static repository..

- Cloud Build process
- combines metadata and prepare config for static generator tool
- uses `dumb-pypi` image ([see available image tags](https://hub.docker.com/r/backupni/dumb-pypi/tags), [GitHub repository](https://github.com/backupni/dumb-pypi-image)) as static generator
- uploads generated static files to bucket


Install
-------

Click to banner and follow installation instructions (2 required and 2 optional simple steps inside).

[![Open in Cloud Shell](https://gstatic.com/cloudssh/images/open-btn.svg)](https://ssh.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fbackupni%2Fpypi-google-cloud&cloudshell_print=cloud-shell-readme.txt&cloudshell_open_in_editor=pypi.yaml&cloudshell_working_dir=install&cloudshell_tutorial=install.md)


How to use
----------

Replace in command below:
- `YOUR_DIST_DIRECTORY` to your dist directory (ex, `dist`),
- `YOUR_PACKAGE_WHL_NAME` to your package whl name (ex. `my_package-0.1.0-py2.py3-none-any`),
- `YOUR_PACKAGES_BUCKET` to your packages bucket name,
- `YOUR_STATIC_BUCKET` to your packages bucket name,
- `YOUR_META_DATA_BUCKET` to your packages bucket name,
- `YOUR_DOMAIN` to your domain (ex. `packages.example.com`).


You can edit `cloudbuild.yaml` for your needs. This is just example how you can manage your package uploading.

Invoke on your CI after package test step.

```
gcloud builds submit \
    'YOUR_DIST_DIRECTORY' \
    --substitutions='_WHL_NAME="YOUR_PACKAGE_WHL_NAME",_PACKAGES_BUCKET="YOUR_PACKAGES_BUCKET",_META_DATA_BUCKET="YOUR_META_DATA_BUCKET",_STATIC_BUCKET="YOUR_STATIC_BUCKET",_DOMAIN="YOUR_DOMAIN"' \
    --config='cloudbuild.yaml' \
    --project='YOUR_PROJECT_ID'
```


Uninstall
---------

- (Recommended) Just delete your private PyPi project. 

  ```sh
  gcloud projects delete 'YOUR_PROJECT_ID'
  ```
- (Alternative) If you use shared project run this command:

  ```sh
  gcloud deployment-manager deployments delete \
      'pypi' \
      --project='YOUR_PROJECT_ID'
  ```

  You should also check assigned roles for `YOUR_PROJECT_NUMBER@cloudservices.gserviceaccount.com` and `YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com` service accounts.


License
-------

This source code is licensed under Apache 2.0. Full license text is available in [LICENSE](LICENSE).


Alternatives
------------

If you would like to use cloud agnostic solution, check this repositories:
- `stevearc/pypicloud`
- `private-pypi/private-pypi`

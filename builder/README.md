Builder
=======

This service updates your static repository.

Implementation
--------------

- Cloud Build process
  - combines metadata and prepare config for static generator tool
  - uses `dumb-pypi` image ([see available image tags](https://hub.docker.com/r/backupner/dumb-pypi/tags), [GitHub repository](https://github.com/backupner/dumb-pypi-image)) as static generator
  - uploads generated static files to bucket

(Optional) Test `Builder` service
---------------------------------

### Prepare test

1. Open https://console.cloud.google.com in your browser and log in. Select your project.
2. Open `Navigation menu` and click to `Storage` menu item. Or just click to this link: https://console.cloud.google.com/storage/browser
3. Click to your metadata bucket name (ex. `pypi-metadata-uogykq`) in table.
4. Create test metadata config.

  - Download any python package, for example, `functions-framework`. 

    ```
    $ python3 -m pip download 'functions-framework'
    ```
  - Now we have, for example, `functions_framework-1.2.0-py3-none-any.whl` file, note this name.
  - Let's find out hash of this package.

    ```
    $ python3 -m pip hash -a 'sha256' 'functions_framework-1.2.0-py3-none-any.whl'
    ```

    ```
    functions_framework-1.2.0-py3-none-any.whl:
    --hash=sha256:8abe57b908ea054893c1e9c8ea49c8ac1c405fc2988c05109d255345ea9595d0
    ```
    Note this hash. You may use `sha384` or `sha512` hashing algorithms instead of `sha256`. `PEP 503` recommendation is `sha256`.
  - Let's find out creation date now.

    ```
    $ stat -r 'functions_framework-1.2.0-py3-none-any.whl'
    ```

    Note creation unix timestamp like `1585401713`.

  - Now we have all required information to create test metadata json object.

    ```
    $ print '{"filename": "functions_framework-1.2.0-py3-none-any.whl", "hash": "sha256=8abe57b908ea054893c1e9c8ea49c8ac1c405fc2988c05109d255345ea9595d0", "uploaded_by": "testuser", "upload_timestamp": 1585401713}' > functions_framework-1.2.0-py3-none-any.whl.meta
    ```
  - Click to `Upload files` button and upload `functions_framework-1.2.0-py3-none-any.whl.meta` to metadata bucket.

### Run test

Run build process (replace `pypi-metadata-uogykq`, `packages-internal.example.com`, `packages.example.com` and `YOUR_PROJECT_ID` to your data: 
   
```
$ gcloud builds submit \
      --substitutions='_META_DATA_BUCKET="pypi-metadata-uogykq",_STATIC_BUCKET="packages-internal.example.com",_DOMAIN="packages.example.com"' \
      --config='builder/cloudbuild.yaml' \
      --no-source \
      --project='YOUR_PROJECT_ID'
```


### Check test results

Open your static website bucket (ex. `packages-internal.example.com`) and view changes. 

Objects `index.html`, `simple/index.html`, `simple/package/index.html` and `pypi/packages/json` should be created during this test.

Usually you do not need run `Builder` service manually. You should build and test your Python package on CI, after that use `Uploader` service. 
`Builder` service is primary used as internal dependency for `Uploader` service.

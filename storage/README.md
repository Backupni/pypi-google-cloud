Storage
=======

Storage is storage. This is the main component of the system.

Implementation
--------------

- Cloud Storage bucket
  - contains Python packages `raw/*.whl`
  - contains html `index.html`, `simple/index.html`, `simple/*/index.html` (read PEP 503 to find out more about it: https://www.python.org/dev/peps/pep-0503/)
  - contains json's with package metadata `pypi/*/json` (read more here: https://warehouse.readthedocs.io/api-reference/json)

Setup
-----

### Manual

#### Web Console (GUI)

##### Create new Cloud Storage bucket.

1. Open https://console.cloud.google.com in your browser and log in. Select (or create new) project.
2. Open `Navigation menu` and click to `Storage` menu item. Or just click to this link: https://console.cloud.google.com/storage/browser.
3. Click to `CREATE BUCKET` button.
4. Set bucket name (ex. `packages-internal.example.com`).
5. Click to `CONTINUE` button.
6. Select `Multi-region` location type, select `eu` location.
7. Click to `CONTINUE` button.
8. Choose `Standart` storage class.
9. Click to `CONTINUE` button.
10. Choose `Uniform` access control.
11. Click to `CONTINUE` button.
12. Choose `Google-managed` key encryption.
13. Add label (ex. `service:pypi`).
14. Click to `CREATE` button.

Feel free to adapt this guide for your needs. You may want to change location, for example, to `us` (don't forget to use project search and replace `eu` to `us` in any `cloudbuild.yaml` files).  

##### Command-line interface (CLI)

Use `gsutil mb` command to create bucket. Use `gsutil help mb` command to read more about available options.

### Automatic

Use Cloud Deployment Manager (https://cloud.google.com/deployment-manager/) and/or Terraform. Please, open new PR, contribute your code.

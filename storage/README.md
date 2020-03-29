Storage
=======

Storage is storage. This is the main component of the system.

Implementation
--------------

- Cloud Storage bucket, which contains Python packages `raw/*.whl`
- Cloud Storage bucket, which contains static site - html `index.html`, `simple/index.html`, `simple/*/index.html` (read PEP 503 to find out more about it: https://www.python.org/dev/peps/pep-0503/) and json's with package metadata `pypi/*/json` (read more here: https://warehouse.readthedocs.io/api-reference/json)
- Cloud Storage bucket, which contains internal metadata for static site generator - package names, package file hashes etc.

Setup
-----

### Manual

1. Open https://console.cloud.google.com in your browser and log in. Select (or create new) project.
2. Open `Navigation menu` and click to `Storage` menu item. Or just click to this link: https://console.cloud.google.com/storage/browser.

#### Create new Cloud Storage bucket.

You need create 3 buckets (ex. `pypi-packages-iobszb` for packages store, `packages-internal.example.com` for static website and `pypi-metadata-uogykq` for metadata store), thus repeat the steps below three times.

1. Click to `CREATE BUCKET` button.
2. Set bucket name.
3. Click to `CONTINUE` button.
4. Select `Multi-region` location type, select `eu` location.
5. Click to `CONTINUE` button.
6. Choose `Standart` storage class.
7. Click to `CONTINUE` button.
8. Choose `Uniform` access control.
9. Click to `CONTINUE` button.
10. Choose `Google-managed` key encryption.
11. Add label (ex. `service:pypi`).
12. Click to `CREATE` button.

Use could use `gsutil mb` command instead to create bucket. Use `gsutil help mb` command to read more about available options.

Feel free to adapt this guide for your needs. You may want to change location, for example, to `us` (don't forget to use project search and replace `eu` to `us` in any `cloudbuild.yaml` files).  

### Automatic

Use Cloud Deployment Manager (https://cloud.google.com/deployment-manager/) and/or Terraform. Please, open new PR, contribute your code.

FAQ
---

#### Why do I need Proxy service?

Let's test it without `Proxy` and see what happens.

You can serve your static website directly from Cloud Storage bucket.

Enable index pages for your static website bucket:

`$ gsutil web set -m index.html gs://packages-internal.example.com`

Add `CNAME` record to your DNS zone. (Name `packages-internal`, target `c.storage.googleapis.com`).

In case you need public PyPI, add permissions to `allUsers`:

1. Select your static bucket `packages-internal.example.com`.
2. Click to `ADD MEMBER` button on `PERMISSIONS` tab. 
3. Set `New members` to `allUsers`.
4. Set `Role` to `Storage Object Viewer`.
5. Click to `SAVE` button. 

Now your PyPi is available at http://packages-internal.example.com. 
But in this case your repository site uses plain http, it's not secure.

You may also access your public repository at https://storage.googleapis.com/packages-internal.example.com/ address. 
But this way is not compatible with index page bucket settings.

If you are going to create private PyPi, this method is also not for you, because of you need basic auth support.

That's why we created `Proxy` service.

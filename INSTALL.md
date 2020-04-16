Install pypi-google-cloud
=========================

Installation instructions.


Preparation
-----------

1. Visit [Google Cloud website](https://cloud.google.com/) and click to `Get started for free` button. 
   Sign in to your Google account (sign up for a new account if needed) and follow instructions.
2. Open [Google Cloud Console](https://console.cloud.google.com/projectselector2/home/dashboard) and select or create new (recommended) Cloud project.
3. Open `Navigation menu` and click to `Billing`. Make sure you have activated billing account for this project. ([Read official docs](https://cloud.google.com/billing/docs/how-to/modify-project) if you are stuck.)
4. (Optional but recommended) Create budget. Open your billing account page and click to `Budgets & Alerts` menu button. After that click to `CREATE BUDGET` button and follow instructions.
5. (Optional) Install `Google Cloud SDK` tools, [read more official docs](https://cloud.google.com/sdk/install) (`Installation options` section). You can use Web GUI and click to `Activate Cloud Shell` button in top right menu instead.
6. Clone repository

   ```sh
   git clone git@github.com:backupner/pypi-google-cloud.git && cd 'pypi-google-cloud'
   ```

7. Prepare `Deployment Manager` (DM).

   Grant `Service Account Admin` and `Storage Admin` roles to `Deployment Manager`'s project level service account.
   Grant `Secret Manager Admin`, `Cloud Run Admin` and `Service Account User` roles to `Cloud Build`'s project level service account.

   ```sh
   bash ./install/grant_permissions
   ```

Setup
-----

Replace `YOUR_PROJECT_ID` in code below to your real Cloud project id and run command.
   
```sh
gcloud deployment-manager deployments create \
    'pypi' \
    --config='install/pypi.yaml' \
    --description='PyPi application' \
    --labels='app=pypi' \
    --project='YOUR_PROJECT_ID' \
    --preview
```

### (Optional) Configure custom domain name

Cloud Run generates your service URL like this: `https://pypi-gcs-proxy-xoeq6xeb4q-ew.a.run.app`. You can create subdomain (ex. `packages.example.com`) and use it instead.

Note `beta`, we use beta command here because of GA version of this command is not compatible with managed Cloud Run right now.

Replace `YOUR_DOMAIN_NAME` to your real domain name (ex. `packages.example.com`)

```sh
gcloud beta run domain-mappings create \
    --service='pypi-gcs-proxy' \
    --domain='YOUR_DOMAIN_NAME' \
    --platform='managed' \
    --region='europe-west1' \
    --project='YOUR_PROJECT_ID'
```

Update DNS records.
```
packages CNAME ghs.googlehosted.com.
```

You can use `https://packages.example.com` instead of `https://pypi-gcs-proxy-xoeq6xeb4q-ew.a.run.app` now.

Installation complete. Just add private repository to your `pyproject.toml` and use `poetry` (or `pip`) as usual. Read more about private repositories in [poetry docs](https://python-poetry.org/docs/repositories/#using-a-private-repository) if you need additional help...

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

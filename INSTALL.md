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
6. Prepare `Deployment Manager` (DM).

   Let us explain. As perfectionists we would like to automate granting access permission throw `Deployment Manager`. 
   But it require to extend default permissions for DM project-level service account itself. 

   First, get your project number:

   Replace `YOUR_PROJECT_ID` in code below to your real Cloud project id.

   ```sh
   gcloud projects describe \
       'YOUR_PROJECT_ID' \
       --format='value(project_number)'
   ```

   Now grant `Service Account Admin` and `Storage Admin` roles to your `Deployment Manager` project service account:

   Replace `YOUR_PROJECT_NUMBER` in code below to your real Cloud project number.

   ```sh
   gcloud projects add-iam-policy-binding \
       'YOUR_PROJECT_ID' \
       --member='serviceAccount:YOUR_PROJECT_NUMBER@cloudservices.gserviceaccount.com' \
       --role='roles/iam.serviceAccountAdmin'
   ```

   ```sh
   gcloud projects add-iam-policy-binding \
       'YOUR_PROJECT_ID' \
       --member='serviceAccount:YOUR_PROJECT_NUMBER@cloudservices.gserviceaccount.com' \
       --role='roles/storage.admin'
   ```


Setup
-----

### Clone repository

```sh
git clone git@github.com:backupner/pypi-google-cloud.git
```

### Run installation script

```sh
gcloud deployment-manager deployments create \
    'pypi' \
    --config='install/pypi.yaml' \
    --description='PyPi application' \
    --labels='app=pypi' \
    --project='YOUR_PROJECT_ID' \
    --preview
```

[Sorry, our installation script is incomplete right now that's why you need manually execute several commands below... We will fix it soon]


### Create new secret

Create new secret with generated random token (you MAY generate several tokens and separate them by spaces):

```
$ pwgen 172 1 | gcloud secrets create \
      'pypi-token' \
      --data-file='-' \
      --labels='app=pypi' \
      --replication-policy='automatic' \
      --project='YOUR_PROJECT_ID'
```

You just created new secret with first version of secret value. 

```
$ gcloud secrets versions describe \
      '1' \
      --secret='pypi-token' \
      --project='YOUR_PROJECT_ID'
```

Save `name` value for future use (is should look like `projects/YOUR_PROJECT_ID/secrets/pypi-token/versions/1`). Replace `YOUR_TOKEN_VERSION_NAME` in code below to this value.

#### Grant role

Grant `Secret Manager Secret Accessor` roles:
```
$ gcloud secrets add-iam-policy-binding \
      'pypi-token' \
      --member='serviceAccount:pypi-proxy@YOUR_PROJECT_ID.iam.gserviceaccount.com' \
      --role='roles/secretmanager.secretAccessor' \
      --project='YOUR_PROJECT_ID'
```

### Upload image for `Proxy` service to registry

Run process:

```
$ gcloud builds submit \
      --config='proxy/cloudbuild.yaml' \
      --no-source \
      --project='YOUR_PROJECT_ID'
```

### Run `Proxy` service

Create `Proxy` service:
```
$ gcloud run deploy \
      'pypi-gcs-proxy' \
      --image='eu.gcr.io/YOUR_PROJECT_ID/pypi-gcs-proxy:latest' \
      --args='' \
      --command='' \
      --concurrency='80' \
      --cpu='1' \
      --max-instances='10' \
      --memory='128Mi' \
      --platform='managed' \
      --port='8080' \
      --timeout='5m' \
      --set-env-vars='STATIC_BUCKET_NAME=pypi-YOUR_PROJECT_ID-static,PACKAGES_BUCKET_NAME=pypi-YOUR_PROJECT_ID-packages,TOKEN_NAME=YOUR_TOKEN_VERSION_NAME' \
      --update-labels='app=pypi' \
      --allow-unauthenticated \
      --service-account='pypi-proxy@YOUR_PROJECT_ID.iam.gserviceaccount.com' \
      --region='europe-west1' \
      --project='YOUR_PROJECT_ID'
```

Assign traffic:
```
$ gcloud run services update-traffic \
      'pypi-gcs-proxy' \
      --platform='managed' \
      --region='europe-west1' \
      --to-latest \
      --project='YOUR_PROJECT_ID'
```

#### (Optional) Configure custom domain name

Cloud Run generates your service URL like this: `https://pypi-gcs-proxy-xoeq6xeb4q-ew.a.run.app`. You can create subdomain (ex. `packages.example.com`) and use it instead.

Note `beta`, we use beta command here because of GA version of this command is not compatible with managed Cloud Run right now.

Replace `YOUR_DOMAIN_NAME` to your real domain name (ex. `packages.example.com`)

```
$ gcloud beta run domain-mappings create \
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

Automatic Setup
---------------

Use [Cloud Deployment Manager](https://cloud.google.com/deployment-manager/) (recommended) and/or Terraform. Please, open new PR, contribute your code.

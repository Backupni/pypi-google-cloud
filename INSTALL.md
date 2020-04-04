Install pypi-google-cloud
=========================

Installation instructions.


Preparation
-----------

1. Visit [Google Cloud website](https://cloud.google.com/) and click to `Get started for free` button. 
   Sign in to your Google account (sign up for a new account if needed) and follow instructions.
2. Open [Google Cloud Console](https://console.cloud.google.com/projectselector2/home/dashboard) and select or create new (recommended) Cloud project.
3. Open `Navigation menu` and click to `Billing`. Make sure you have activated billing account for this project. ([Read official docs](https://cloud.google.com/billing/docs/how-to/modify-project) if you are stuck.)
4. Create budget (optional but recommended). Open your billing account page and click to `Budgets & Alerts` menu button. After that click to `CREATE BUDGET` button and follow instructions.
5. (Optional) Install `Google Cloud SDK` tools, [read more official docs](https://cloud.google.com/sdk/install) (`Installation options` section). You can use Web GUI and click to `Activate Cloud Shell` button in top right menu instead.


Setup
-----

Replace `YOUR_PROJECT_ID` in code below to your real Cloud project id.

### Create required service accounts

We need single service account for `Proxy` service with project level permissions (`Service Account Token Creator` role).

```
$ gcloud iam service-accounts create \
      'pypi-proxy' \
      --description='PyPi Proxy service account' \
      --display-name='PyPI proxy' \
      --project='YOUR_PROJECT_ID'
```

#### Grant role

Grant `Service Account Token Creator` role to service account:
```
$ gcloud projects add-iam-policy-binding \
      'YOUR_PROJECT_ID' \
      --member='serviceAccount:pypi-proxy@YOUR_PROJECT_ID.iam.gserviceaccount.com' \
      --role='roles/iam.serviceAccountTokenCreator'
```

### Build images for `Builder` process and `Proxy` service

Build container image for `Builder` process:

```
$ gcloud builds submit \
      'builder/images/dumb-pypi' \
      --config='builder/images/dumb-pypi/cloudbuild.yaml' \
      --project='YOUR_PROJECT_ID'
```

Build container image for `Proxy` service:

```
$ gcloud builds submit \
      'proxy/images/pypi-gcs-proxy' \
      --config='proxy/images/pypi-gcs-proxy/cloudbuild.yaml' \
      --project='YOUR_PROJECT_ID'
```

### Create new `Storage` buckets.

You need create 3 buckets (ex. `pypi-packages-iobszb` for packages store, `pypi-static-ioM6ch` for static website and `pypi-meta-uogykq` for meta data store).

You MUST choose globally unique bucket names. You MAY use results of this command as bucket name unique suffixes:

```
$ pwgen 6 3
```

Replace `YOUR_PACKAGES_BUCKET_NAME`, `YOUR_STATIC_BUCKET_NAME`, and `YOUR_META_DATA_BUCKET_NAME` in code below to your bucket names.

```
$ gsutil mb \
      -b 'on' \
      -c 'Standard' \
      -l 'EU' \
      -p 'YOUR_PROJECT_ID' \
      'gs://YOUR_PACKAGES_BUCKET_NAME'
```
```
$ gsutil mb \
      -b 'on' \
      -c 'Standard' \
      -l 'EU' \
      -p 'YOUR_PROJECT_ID' \
      'gs://YOUR_STATIC_BUCKET_NAME'
```
```
$ gsutil mb \
      -b 'on' \
      -c 'Standard' \
      -l 'EU' \
      -p 'YOUR_PROJECT_ID' \
      'gs://YOUR_META_DATA_BUCKET_NAME'
```
```
$ gsutil label ch -l 'app:pypi' 'gs://YOUR_PACKAGES_BUCKET_NAME'
```
```
$ gsutil label ch -l 'app:pypi' 'gs://YOUR_STATIC_BUCKET_NAME'
```
```
$ gsutil label ch -l 'app:pypi' 'gs://YOUR_META_DATA_BUCKET_NAME'
```

Feel free to adapt this guide for your needs. You may want to change location, for example, to `US` (don't forget to use project search and make related changes in `cloudbuild.yaml` files).  

#### Grant role

Grant `Storage Legacy Bucket Reader` and `Storage Legacy Object Reader` roles to `pypi-proxy` service account for packages and meta data buckets:
```
$ gsutil iam ch \
      'serviceAccount:pypi-proxy@YOUR_PROJECT_ID.iam.gserviceaccount.com:legacyBucketReader,legacyObjectReader' \
      'gs://YOUR_PACKAGES_BUCKET_NAME'
```
```
$ gsutil iam ch \
      'serviceAccount:pypi-proxy@YOUR_PROJECT_ID.iam.gserviceaccount.com:legacyBucketReader,legacyObjectReader' \
      'gs://YOUR_META_DATA_BUCKET_NAME'
```


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
      --set-env-vars='STATIC_BUCKET_NAME=YOUR_STATIC_BUCKET_NAME,PACKAGES_BUCKET_NAME=YOUR_PACKAGES_BUCKET_NAME,TOKEN_NAME=YOUR_TOKEN_VERSION_NAME' \
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

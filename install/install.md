Installation Tutorial
=====================

Select project
--------------

<walkthrough-project-billing-setup></walkthrough-project-billing-setup>


Grant permissions
-----------------

Prepare `Deployment Manager` (DM).

Grant `Service Account Admin` and `Storage Admin` roles to `Deployment Manager`'s project level service account.
Grant `Secret Manager Admin`, `Cloud Run Admin` and `Service Account User` roles to `Cloud Build`'s project level service account.

Run command.

```sh
PROJECT_ID='{{project-id}}' ./grant_permissions
```

Deploy private PyPi application
-------------------------------

Check your `pypi.yaml` properties config and change (you may change `region` property, see [available reions](https://cloud.google.com/compute/docs/regions-zones/#locations) list) if needed. 

After that execute command below:

```sh
gcloud deployment-manager deployments create \
    'pypi' \
    --config='pypi.yaml' \
    --description='PyPi application' \
    --labels='app=pypi' \
    --project='{{project-id}}' \
    --preview
```

(Optional) Configure custom domain name
---------------------------------------

Cloud Run generates your service URL (ex. `https://pypi-gcs-proxy-somethingrandom-ew.a.run.app`). You can create subdomain (ex. `packages.example.com`) and use it instead.

Note `beta`, we use beta command here because of GA version of this command is not compatible with managed Cloud Run right now.

Replace `YOUR_DOMAIN_NAME` to your real domain name (ex. `packages.example.com`)

```sh
gcloud beta run domain-mappings create \
    --service='pypi-gcs-proxy' \
    --domain='YOUR_DOMAIN_NAME' \
    --platform='managed' \
    --region='europe-west1' \
    --project='{{project-id}}'
```

Update DNS records.
```
packages CNAME ghs.googlehosted.com.
```

You can use your domain now.


(Optional, recommended) Create budget
-------------------------------------

Open your billing account page and click to `Budgets & Alerts` menu button. After that click to `CREATE BUDGET` button and follow instructions.


Complete
--------

Installation complete. 

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>


Add private repository to your `pyproject.toml`. Use `poetry` (or `pip`) as usual. Read more about installing packages from private repositories in [poetry docs](https://python-poetry.org/docs/repositories/#using-a-private-repository)...

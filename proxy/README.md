Proxy
=====

This service adds basic auth with tokens support and provides access to packages. Simple layer between Storage and end users.

Implementation
--------------

- managed Google Cloud Run
  - uses Python image with Starlette Python ASGI framework (it should be fast)
  - uses Service Account
  - uses Google Cloud Secret for auth tokens storage
  - (optional) uses custom domain name

Setup
-----

### Manual

#### Build image

Run Cloud Build process:
`$ gcloud builds submit --config proxy/images/pypi-gcs-proxy/cloudbuild.yaml proxy/images/pypi-gcs-proxy --project=YOUR_PROJECT_ID`.

#### Create Service Account. Add permissions

1. Open `Navigation menu`, select `IAM & Admin` -> `Service Accounts`. Or just click to this link: https://console.cloud.google.com/iam-admin/serviceaccounts.
2. Click to `CREATE SERVICE ACCOUNT` button.
3. Set `Service account name` to `pypi-proxy`.
4. Set `Service account description` to `PyPI proxy`.
5. Click to `CREATE` button.
6. Select `Service Account Token Creator` role.
7. Click to `ADD ANOTHER ROLE` button.
8. Select `Secret Manager Secret Accessor` role.
9. Click to `ADD ANOTHER ROLE` button.
10. Select `Storage Admin` role.
11. Click to `CONTINUE` button.
12. Click to `DONE` button.

#### Create Secret

1. Open `Navigation menu`, select `Security` -> `Secret Manager`. Or just click to this link: https://console.cloud.google.com/security/secret-manager.
2. Click to `CREATE SECRET` button.
3. Set `Name` to `pypi-token`.
4. Generate random token.

`$ pwgen 172 1`

5. Set `Secret value` to your token value. You may use multiple tokens, use spaces to separate them.
6. Click to `ADD LABEL` button.
7. Set fields: `Key`: `app`, `Value`: `pypi`.
8. Click to `CREATE SECRET` button.
9. You just created new secret and viewing secret versions table now. Open `Actions` menu and click to `Copy Resource ID` menu button. Save this value for future use (ex. `projects/123/secrets/pypi-token/versions/1`).


#### Run service

1. Open `Navigation menu`, select `Cloud Run`. Or just click to this link: https://console.cloud.google.com/run.
2. Click to `CREATE SERVICE` button.
3. Select `Deployment platform` to `Cloud Run (fully managed)`.
4. Set `Region` to `europe-west1` (select close to storage buckets region).
5. Set `Service name` to `pypi-gcs-proxy`.
6. Set `Authentication` to `Allow unauthenticated invocations`.
7. Click to `NEXT` button.
8. Set `Container image URL` value. You should select `latest` version of your `pypi-gcs-proxy` image here.
9. Click to `SHOW ADVANCED SETTINGS` button. 
10. Now you should find 3 tabs: `CONTAINER`, `VARIABLES & SECRETS` and `CONNECTIONS` with several groups of fields. We need first two of them. Select `CONTAINER` tab.
11. Configure `General` container settings:
    - save default value in `Container port` (`8080`),
    - leave blank `Container command` field,
    - leave blank `Container arguments` field,
    - change `Service account`, select `pypi-proxy` in list of values.
12. Configure `Capacity` container settings:
    - leave default value in `Capacity` field (`80`),
    - leave default value in `Request timeout` (`300`),
    - leave default value in `CPU allocated` field (`1`),
    - change value in `Memory allocated` to `128MiB`.
13. Configure `Autoscaling` container settings:
    - change `Maximum number of instances` to `10`.
14. Click to `VARIABLES & SECRETS` tab.
15. Click to `ADD VARIABLE` button three times.
    - set `STATIC_BUCKET_NAME` to name of your static website bucket (ex. `packages-internal.example.com`),
    - set `PACKAGES_BUCKET_NAME` to name of your packages bucket (ex. `pypi-packages-iobszb`),
    - set `TOKEN_NAME` to your secret token version name (ex. `projects/123/secrets/pypi-token/versions/1`).
16. Leave checked `Serve this revision immediately` checkbox.
17. Click to `DEPLOY` button.


Check logs on errors. You may need activate several APIs. In this case fix error and deploy new revision using `EDIT & DEPLOY NEW REVISION` button.

#### (Optional) Configure custom domain name

Cloud Run generates your service URL like this: `https://pypi-gcs-proxy-xoeq6xeb4q-ew.a.run.app`. You can create subdomain (ex. `packages.example.com`) and use it instead.

1. Open `Navigation menu`, select `Cloud Run`. Or just click to this link: https://console.cloud.google.com/run.
2. Click to  `MANAGE CUSTOM DOMAINS` button.
3. Click to `ADD MAPPING` -> `Add service domain mapping`.
4. Select `pypi-gcs-proxy` service.
5. Select verified domain (or verify new domain) (ex. `example.com`).
6. Specify `packages` subdomain.
7. Click to `CONTINUE` button.
8. Update DNS records.

    `packages CNAME ghs.googlehosted.com.`

9. Click to `DONE` button.

You can use `https://packages.example.com` instead of `https://pypi-gcs-proxy-xoeq6xeb4q-ew.a.run.app` now.

### Automatic

Use Cloud Deployment Manager (https://cloud.google.com/deployment-manager/) and/or Terraform. Please, open new PR, contribute your code.

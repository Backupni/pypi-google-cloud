from typing import Any, Dict, List


REGION = 'europe-west1'

ENV_VARS_TEMPLATE = ','.join([
    'STATIC_BUCKET_NAME={deployment}-{project}-static',
    'PACKAGES_BUCKET_NAME={deployment}-{project}-packages',
    'TOKEN_NAME=projects/{project}/secrets/{deployment}-token/versions/1',
])

DEPLOY_CONTAINER_ARGS_TEMPLATE = [
    'run', 'deploy', '{deployment}-gcs-proxy',
    '--image', '{internal_pypi_gcs_proxy_image}',
    '--args', '',
    '--command', '',
    '--concurrency', '80',
    '--cpu', '1',
    '--max-instances', '10',
    '--memory', '128Mi',
    '--platform', 'managed',
    '--port', '8080',
    '--timeout', '5m',
    '--set-env-vars', '{env_vars}',
    '--update-labels', 'app={deployment}',
    '--allow-unauthenticated',
    '--service-account', '{deployment}-proxy@{project}.iam.gserviceaccount.com',
    '--region', REGION,
    '--project', '{project}',
]

DELETE_SERVICE_ARGS_TEMPLATE = [
    'run', 'services', 'delete',
    '{deployment}-gcs-proxy',
    '--platform', 'managed',
    '--region', REGION,
    '--project', '{project}',
]

INTERNAL_PYPI_GCS_PROXY_IMAGE_TEMPLATE = 'eu.gcr.io/{project}/{deployment}-gcs-proxy:latest'
PYPI_GCS_PROXY_IMAGE = 'backupner/pypi-gcs-proxy:latest'


def generate_config(context: Any) -> Dict[str, List]:
    """We use `Cloud Build` actions here because of related `gcp-types` are not available for `Run` now.

    Todo: create custom type providers (or wait for Google)"""
    deployment = context.env['deployment']
    project = context.env['project']
    internal_pypi_gcs_proxy_image = INTERNAL_PYPI_GCS_PROXY_IMAGE_TEMPLATE.format(deployment=deployment, project=project)
    deploy_container_args = DEPLOY_CONTAINER_ARGS_TEMPLATE
    deploy_container_args[2] = deploy_container_args[2].format(deployment=deployment)
    deploy_container_args[4] = internal_pypi_gcs_proxy_image
    deploy_container_args[24] = ENV_VARS_TEMPLATE.format(deployment=deployment, project=project)
    deploy_container_args[26] = deploy_container_args[26].format(deployment=deployment)
    deploy_container_args[29] = deploy_container_args[29].format(deployment=deployment, project=project)
    deploy_container_args[33] = project
    delete_container_args = DELETE_SERVICE_ARGS_TEMPLATE
    delete_container_args[3] = delete_container_args[3].format(deployment=deployment)
    delete_container_args[9] = project
    resources = [
        {
            'name': 'download-{deployment}-proxy-container-image'.format(deployment=deployment),
            'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
            'metadata': {
                'runtimePolicy': ['CREATE'],
            },
            'properties': {
                'steps': [
                    {
                        'name': 'gcr.io/cloud-builders/docker',
                        'args': ['pull', PYPI_GCS_PROXY_IMAGE],
                    },
                    {
                        'name': 'gcr.io/cloud-builders/docker',
                        'args': ['tag', PYPI_GCS_PROXY_IMAGE, internal_pypi_gcs_proxy_image],
                    },
                    {
                        'name': 'gcr.io/cloud-builders/docker',
                        'args': ['push', internal_pypi_gcs_proxy_image],
                    },
                ],
                'timeout': '120s',
                'options': {
                    'env': [
                        'CLOUDSDK_CORE_DISABLE_PROMPTS=1',
                    ],
                    'sourceProvenanceHash': ['SHA256'],
                },
                'tags': [deployment],
                'images': [
                    internal_pypi_gcs_proxy_image,
                ],
            },
        },
        {
            'name': 'deploy-{deployment}-proxy-run-container'.format(deployment=deployment),
            'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
            'metadata': {
                'dependsOn': [
                    'download-{deployment}-proxy-container-image'.format(deployment=deployment),
                ],
                'runtimePolicy': ['CREATE'],
            },
            'properties': {
                'steps': [
                    {
                        'name': 'gcr.io/cloud-builders/gcloud',
                        'args': deploy_container_args,
                        'env': [
                            'CLOUDSDK_CORE_DISABLE_PROMPTS=1',
                        ],
                    },
                ],
                'timeout': '120s',
                'tags': [deployment],
            },
        },
        {
            'name': 'delete-{deployment}-proxy-run-service'.format(deployment=deployment),
            'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
            'metadata': {
                'runtimePolicy': ['DELETE'],
            },
            'properties': {
                'steps': [
                    {
                        'name': 'gcr.io/cloud-builders/gcloud',
                        'args': delete_container_args,
                        'env': [
                            'CLOUDSDK_CORE_DISABLE_PROMPTS=1',
                        ],
                    },
                ],
                'timeout': '120s',
                'tags': [deployment],
            },
        },
    ]
    return {
        'resources': resources,
    }

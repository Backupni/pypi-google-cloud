from typing import Any, Dict, List


GENERATE_RANDOM_TOKEN_COMMAND = "head -c '500' '/dev/urandom'" \
                                " | tr -dc 'a-zA-Z0-9'" \
                                " | fold -w '33'" \
                                " | head -n '1'"

CREATE_TOKEN_STDIN_COMMAND_TEMPLATE = "gcloud secrets create " \
                                      "'{deployment}-token' " \
                                      "--data-file='-' " \
                                      "--labels='app={deployment}' " \
                                      "--replication-policy='automatic' " \
                                      "--project='{project}'"

CREATE_TOKEN_COMMAND_TEMPLATE = ' | '.join([GENERATE_RANDOM_TOKEN_COMMAND, CREATE_TOKEN_STDIN_COMMAND_TEMPLATE])

DELETE_TOKEN_COMMAND_TEMPLATE = "gcloud secrets delete " \
                                "'{deployment}-token' " \
                                "--project='{project}'"

GRANT_ROLE_COMMAND_TEMPLATE = "gcloud secrets add-iam-policy-binding " \
                              "'{deployment}-token' " \
                              "--member='serviceAccount:{deployment}-proxy@{project}.iam.gserviceaccount.com' " \
                              "--role='roles/secretmanager.secretAccessor' " \
                              "--project='{project}'"


def generate_config(context: Any) -> Dict[str, List]:
    """We use `Cloud Build` actions here because of related `gcp-types` are not available for `Secret manager` now.

    Todo: create custom type providers (or wait for Google)"""
    deployment = context.env['deployment']
    project = context.env['project']
    create_token_command = CREATE_TOKEN_COMMAND_TEMPLATE.format(deployment=deployment, project=project)
    delete_token_command = DELETE_TOKEN_COMMAND_TEMPLATE.format(deployment=deployment, project=project)
    grant_role_command = GRANT_ROLE_COMMAND_TEMPLATE.format(deployment=deployment, project=project)
    resources = [
        {
            'name': 'create-{deployment}-token'.format(deployment=deployment),
            'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
            'metadata': {
                'dependsOn': [
                    '{deployment}-proxy'.format(deployment=deployment),
                    '{deployment}-services-enable-secretmanager'.format(deployment=deployment),
                ],
                'runtimePolicy': ['CREATE'],
            },
            'properties': {
                'steps': [
                    {
                        'name': 'gcr.io/cloud-builders/gcloud',
                        'entrypoint': 'bash',
                        'args': [
                            '-c',
                            create_token_command,
                        ],
                    },
                    {
                        'name': 'gcr.io/cloud-builders/gcloud',
                        'entrypoint': 'bash',
                        'args': [
                            '-c',
                            grant_role_command,
                        ],
                    },
                ],
                'timeout': '120s',
                'options': {
                    'env': [
                        'CLOUDSDK_CORE_DISABLE_PROMPTS=1',
                    ],
                },
                'tags': [deployment],
            },
        },
        {
            'name': 'delete-{deployment}-token'.format(deployment=deployment),
            'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
            'metadata': {
                'dependsOn': [
                    '{deployment}-services-enable-secretmanager'.format(deployment=deployment),
                ],
                'runtimePolicy': ['DELETE'],
            },
            'properties': {
                'steps': [
                    {
                        'name': 'gcr.io/cloud-builders/gcloud',
                        'entrypoint': 'bash',
                        'args': [
                            '-c',
                            delete_token_command,
                        ],
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

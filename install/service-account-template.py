from typing import Any, Dict, List


def generate_config(context: Any) -> Dict[str, List]:
    resources = [
        {
            'name': 'pypi-proxy',
            'type': 'gcp-types/iam-v1:projects.serviceAccounts',
            'properties': {
                'accountId': 'pypi-proxy',
                'serviceAccount': {
                    'displayName': 'PyPI proxy',
                    'description': 'PyPi Proxy service account',
                },
            },
            'accessControl': {
                'gcpIamPolicy': {
                    'bindings': [
                        {
                            'role': 'roles/iam.serviceAccountTokenCreator',
                            'members': [
                                'serviceAccount:pypi-proxy@{project}.iam.gserviceaccount.com'.format(project=context.env['project']),
                            ],
                        },
                    ],
                },
            },
        },
    ]
    return {
        'resources': resources,
    }

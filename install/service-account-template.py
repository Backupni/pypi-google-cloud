def generate_config(context):
    deployment = context.env['deployment']
    project = context.env['project']
    resources = [
        {
            'name': '{deployment}-proxy'.format(deployment=deployment),
            'type': 'gcp-types/iam-v1:projects.serviceAccounts',
            'properties': {
                'accountId': '{deployment}-proxy'.format(deployment=deployment),
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
                                'serviceAccount:{deployment}-proxy@{project}.iam.gserviceaccount.com'.format(deployment=deployment, project=project),
                            ],
                        },
                    ],
                },
            },
            'metadata': {
                'dependsOn': [
                    '{deployment}-services-enable-iam'.format(deployment=deployment),
                ],
            },
        },
    ]
    return {
        'resources': resources,
    }

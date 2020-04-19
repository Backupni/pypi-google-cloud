def generate_config(context):
    deployment = context.env['deployment']
    project = context.env['project']
    name_prefix = '{deployment}-{project}-'.format(deployment=deployment, project=project)
    resources = [
        {
            'name': '{name_prefix}proxy'.format(name_prefix=name_prefix),
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
                    '{name_prefix}services-enable-iam'.format(name_prefix=name_prefix),
                ],
            },
        },
    ]
    return {
        'resources': resources,
    }

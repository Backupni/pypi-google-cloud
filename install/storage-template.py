def generate_config(context):
    deployment = context.env['deployment']
    project = context.env['project']
    name_prefix = '{deployment}-{project}-'.format(deployment=deployment, project=project)
    resources = [
        {
            'name': '{name_prefix}packages'.format(name_prefix=name_prefix),
            'type': 'gcp-types/storage-v1:buckets',
            'properties': {
                'location': 'EU',
                'storageClass': 'STANDARD',
                'iamConfiguration': {
                    'uniformBucketLevelAccess': {
                        'enabled': True,
                    },
                },
                'labels': {
                    'app': deployment,
                },
            },
        },
        {
            'name': '{name_prefix}static'.format(name_prefix=name_prefix),
            'type': 'gcp-types/storage-v1:buckets',
            'properties': {
                'location': 'EU',
                'storageClass': 'STANDARD',
                'iamConfiguration': {
                    'uniformBucketLevelAccess': {
                        'enabled': True,
                    },
                },
                'labels': {
                    'app': deployment,
                },
            },
        },
        {
            'name': '{name_prefix}meta'.format(name_prefix=name_prefix),
            'type': 'gcp-types/storage-v1:buckets',
            'properties': {
                'location': 'EU',
                'storageClass': 'STANDARD',
                'iamConfiguration': {
                    'uniformBucketLevelAccess': {
                        'enabled': True,
                    },
                },
                'labels': {
                    'app': deployment,
                },
            },
        },
        {
            'name': '{name_prefix}packages-iam-policy'.format(name_prefix=name_prefix),
            'action': 'gcp-types/storage-v1:storage.buckets.setIamPolicy',
            'properties': {
                'bucket': '{name_prefix}packages'.format(name_prefix=name_prefix),
                'project': project,
                'bindings': [
                    {
                        'role': 'roles/storage.legacyBucketOwner',
                        'members': [
                            'projectEditor:{project}'.format(project=project),
                            'projectOwner:{project}'.format(project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyBucketReader',
                        'members': [
                            'projectViewer:{project}'.format(project=project),
                            'serviceAccount:{deployment}-proxy@{project}.iam.gserviceaccount.com'.format(deployment=deployment, project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyObjectOwner',
                        'members': [
                            'projectEditor:{project}'.format(project=project),
                            'projectOwner:{project}'.format(project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyObjectReader',
                        'members': [
                            'projectViewer:{project}'.format(project=project),
                            'serviceAccount:{deployment}-proxy@{project}.iam.gserviceaccount.com'.format(deployment=deployment, project=project),
                        ],
                    },
                ],
            },
            'metadata': {
                'dependsOn': [
                    '{name_prefix}proxy'.format(name_prefix=name_prefix),
                    '{name_prefix}packages'.format(name_prefix=name_prefix),
                ],
            },
        },
        {
            'name': '{name_prefix}static-iam-policy'.format(name_prefix=name_prefix),
            'action': 'gcp-types/storage-v1:storage.buckets.setIamPolicy',
            'properties': {
                'bucket': '{name_prefix}static'.format(name_prefix=name_prefix),
                'project': project,
                'bindings': [
                    {
                        'role': 'roles/storage.legacyBucketOwner',
                        'members': [
                            'projectEditor:{project}'.format(project=project),
                            'projectOwner:{project}'.format(project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyBucketReader',
                        'members': [
                            'projectViewer:{project}'.format(project=project),
                            'serviceAccount:{deployment}-proxy@{project}.iam.gserviceaccount.com'.format(deployment=deployment, project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyObjectOwner',
                        'members': [
                            'projectEditor:{project}'.format(project=project),
                            'projectOwner:{project}'.format(project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyObjectReader',
                        'members': [
                            'projectViewer:{project}'.format(project=project),
                            'serviceAccount:{deployment}-proxy@{project}.iam.gserviceaccount.com'.format(deployment=deployment, project=project),
                        ],
                    },
                ],
            },
            'metadata': {
                'dependsOn': [
                    '{name_prefix}proxy'.format(name_prefix=name_prefix),
                    '{name_prefix}static'.format(name_prefix=name_prefix),
                ],
            },
        },
        {
            'name': '{name_prefix}meta-iam-policy'.format(name_prefix=name_prefix),
            'action': 'gcp-types/storage-v1:storage.buckets.setIamPolicy',
            'properties': {
                'bucket': '{name_prefix}meta'.format(name_prefix=name_prefix),
                'project': project,
                'bindings': [
                    {
                        'role': 'roles/storage.legacyBucketOwner',
                        'members': [
                            'projectEditor:{project}'.format(project=project),
                            'projectOwner:{project}'.format(project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyBucketReader',
                        'members': [
                            'projectViewer:{project}'.format(project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyObjectOwner',
                        'members': [
                            'projectEditor:{project}'.format(project=project),
                            'projectOwner:{project}'.format(project=project),
                        ],
                    },
                    {
                        'role': 'roles/storage.legacyObjectReader',
                        'members': [
                            'projectViewer:{project}'.format(project=project),
                        ],
                    },
                ],
            },
            'metadata': {
                'dependsOn': [
                    '{name_prefix}proxy'.format(name_prefix=name_prefix),
                    '{name_prefix}meta'.format(name_prefix=name_prefix),
                ],
            },
        },
    ]
    return {
        'resources': resources,
    }

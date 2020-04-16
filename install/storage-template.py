from typing import Any, Dict, List


def generate_config(context: Any) -> Dict[str, List]:
    deployment = context.env['deployment']
    project = context.env['project']
    bucket_name_prefix = '{deployment}-{project}-'.format(deployment=deployment, project=project)
    resources = [
        {
            'name': '{bucket_name_prefix}packages'.format(bucket_name_prefix=bucket_name_prefix),
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
            'name': '{bucket_name_prefix}static'.format(bucket_name_prefix=bucket_name_prefix),
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
            'name': '{bucket_name_prefix}meta'.format(bucket_name_prefix=bucket_name_prefix),
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
            'name': '{bucket_name_prefix}packages-iam-policy'.format(bucket_name_prefix=bucket_name_prefix),
            'action': 'gcp-types/storage-v1:storage.buckets.setIamPolicy',
            'properties': {
                'bucket': '{bucket_name_prefix}packages'.format(bucket_name_prefix=bucket_name_prefix),
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
                    '{bucket_name_prefix}packages'.format(bucket_name_prefix=bucket_name_prefix),
                ],
            },
        },
        {
            'name': '{bucket_name_prefix}static-iam-policy'.format(bucket_name_prefix=bucket_name_prefix),
            'action': 'gcp-types/storage-v1:storage.buckets.setIamPolicy',
            'properties': {
                'bucket': '{bucket_name_prefix}static'.format(bucket_name_prefix=bucket_name_prefix),
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
                    '{bucket_name_prefix}static'.format(bucket_name_prefix=bucket_name_prefix),
                ],
            },
        },
        {
            'name': '{bucket_name_prefix}meta-iam-policy'.format(bucket_name_prefix=bucket_name_prefix),
            'action': 'gcp-types/storage-v1:storage.buckets.setIamPolicy',
            'properties': {
                'bucket': '{bucket_name_prefix}meta'.format(bucket_name_prefix=bucket_name_prefix),
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
                    '{bucket_name_prefix}meta'.format(bucket_name_prefix=bucket_name_prefix),
                ],
            },
        },
    ]
    return {
        'resources': resources,
    }

def generate_config(context):
    deployment = context.env['deployment']
    project = context.env['project']
    name_prefix = '{deployment}-{project}-'.format(deployment=deployment, project=project)
    resources = [
        {
            'name': '{name_prefix}services-enable-iam'.format(name_prefix=name_prefix),
            'type': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
            'properties': {
                'consumerId': 'project:{project}'.format(project=project),
                'serviceName': 'iam.googleapis.com',
            },
        },
        {
            'name': '{name_prefix}services-enable-secretmanager'.format(name_prefix=name_prefix),
            'type': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
            'properties': {
                'consumerId': 'project:{project}'.format(project=project),
                'serviceName': 'secretmanager.googleapis.com',
            },
        },
        {
            'name': '{name_prefix}services-enable-run'.format(name_prefix=name_prefix),
            'type': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
            'properties': {
                'consumerId': 'project:{project}'.format(project=project),
                'serviceName': 'run.googleapis.com',
            },
        },
    ]
    return {
        'resources': resources,
    }

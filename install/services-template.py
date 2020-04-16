from typing import Any, Dict, List


def generate_config(context: Any) -> Dict[str, List]:
    deployment = context.env['deployment']
    project = context.env['project']
    resources = [
        {
            'name': '{deployment}-services-enable-iam'.format(deployment=deployment),
            'type': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
            'properties': {
                'consumerId': 'project:{project}'.format(project=project),
                'serviceName': 'iam.googleapis.com',
            },
        },
        {
            'name': '{deployment}-services-enable-secretmanager'.format(deployment=deployment),
            'type': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
            'properties': {
                'consumerId': 'project:{project}'.format(project=project),
                'serviceName': 'secretmanager.googleapis.com',
            },
        },
        {
            'name': '{deployment}-services-enable-run'.format(deployment=deployment),
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

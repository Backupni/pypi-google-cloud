from typing import Any, Dict, List


def generate_config(context: Any) -> Dict[str, List]:
    """Creates private PyPi."""

    resources = [
        {
            'name': 'pypi-run',
            'type': 'run-template.py',
        },
        {
            'name': 'pypi-secret',
            'type': 'secret-template.py',
        },
        {
            'name': 'pypi-service-account',
            'type': 'service-account-template.py',
        },
        {
            'name': 'pypi-services',
            'type': 'services-template.py',
        },
        {
            'name': 'pypi-storage',
            'type': 'storage-template.py',
        },
    ]
    return {
        'resources': resources,
    }

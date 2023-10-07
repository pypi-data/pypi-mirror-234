# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['object_storage',
 'object_storage.clients',
 'object_storage.managers',
 'object_storage.providers']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=23.1.0,<24.0.0',
 'aiohttp>=3.8.4,<4.0.0',
 'azure-storage-blob==12.16.0',
 'httpx>=0.25.0,<0.26.0']

setup_kwargs = {
    'name': 'pilot-platform-object-storage',
    'version': '1.5.4',
    'description': 'Python library for interacting with multiple object storage APIs.',
    'long_description': '# Pilot Platform Storage Manager\n\n[![Run Tests](https://github.com/PilotDataPlatform/object-storage/actions/workflows/run-tests.yml/badge.svg?branch=develop)](https://github.com/PilotDataPlatform/object-storage/actions/workflows/run-tests.yml)\n[![Python](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://www.python.org/)\n[![PyPI](https://img.shields.io/pypi/v/pilot-platform-object-storage.svg)](https://pypi.org/project/pilot-platform-object-storage/)\n\nProvides a simple and flexible Python library for efficient and reliable object storage solutions. Enables direct interaction with multiple object storage APIs, starting with Azure Blob API and with plans to add more in the future\n\n## Getting Started\n\n### Manager\n```python\nimport asyncio\nfrom object_storage.factories import get_manager\n\nconnection_string = \'DefaultEndpointsProtocol=https;AccountName=pilot;AccountKey=any;EndpointSuffix=core.windows.net\'\nazr_manager = get_manager(\'azure\', connection_string)\n\naccount_sas = asyncio.run(azr_manager.get_container_sas(\'test\'))\nprint(blob_sas)\n> \'https://pilot.blob.core.windows.net/test/file.txt?sp=rw&st=2023-04-28T15:15:14Z&se=2023-04-28T23:15:14Z&spr=https&sv=2021-12-02&sr=b&sig=account_signature\'\n\n\nblob_sas = asyncio.run(azr_manager.get_blob_sas(\'test\', \'small.txt\'))\n\nprint(blob_sas)\n> \'https://pilot.blob.core.windows.net/test/file.txt?sp=rw&st=2023-04-28T15:15:14Z&se=2023-04-28T23:15:14Z&spr=https&sv=2021-12-02&sr=b&sig=blob_signature\'\n\n\nblobs_list = asyncio.run(azr_manager.list_objects(\'test\'))\nprint(blobs_list)\n> [<class \'azure.storage.blob._models.BlobProperties\'>, ...]\n\n\nblobs_list = asyncio.run(azr_manager.create_container(\'test\'))\n```\n\n### File Client\n```python\nimport asyncio\nfrom object_storage.factories import get_file_client\n\nblob_sas_url = \'https://pilot.blob.core.windows.net/test/file.txt?sp=rw&st=2023-04-28T15:15:14Z&se=2023-04-28T23:15:14Z&spr=https&sv=2021-12-02&sr=b&sig=account_signature\'\nazr_file_client = get_file_client(\'azure\', blob_sas_url)\nasyncio.run(azr_file_client.upload_file(\'./small.txt\'))\n```\n\n### Container Client\n```python\nimport asyncio\nfrom object_storage.factories import get_container_client\n\ncontainer_sas_url = \'https://pilot.blob.core.windows.net/test?sp=rw&st=2023-04-28T15:15:14Z&se=2023-04-28T23:15:14Z&spr=https&sv=2021-12-02&sr=b&sig=account_signature\'\nazr_container_client = get_container_client(\'azure\', container_sas_url)\nasyncio.run(azr_container_client.upload_file(\'small.txt\', \'./small.txt\'))\n\n```\n\n## Installation & Quick Start\nThe latest version of the object-storage package is available on [PyPi](https://pypi.org/project/pilot-platform-object-storage/) and can be installed into another service via Pip.\n\nPip install from PyPi:\n```\npip install pilot-platform-object-storage\n```\n\nIn `pyproject.toml`:\n```\npilot-platform-object-storage = "^<VERSION>"\n```\n\nPip install from a local `.whl` file:\n```\npip install pilot_platform_object_storage-<VERSION>-py3-none-any.whl\n```\n\n## Documentation\n\nAPI Reference and User Guide available at [pilotdataplatform.github.io/object-storage](https://pilotdataplatform.github.io/object-storage/)\n\n## Contribution\n\nYou can contribute the project in following ways:\n\n* Report a bug.\n* Suggest a feature.\n* Open a pull request for fixing issues or adding functionality. Please consider using [pre-commit](https://pre-commit.com) in this case.\n* For general guidelines on how to contribute to the project, please take a look at the [contribution guide](CONTRIBUTING.md).\n',
    'author': 'Indoc Systems',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

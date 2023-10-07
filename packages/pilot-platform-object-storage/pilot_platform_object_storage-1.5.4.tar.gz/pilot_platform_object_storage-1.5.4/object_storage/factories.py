# Copyright (C) 2023 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from typing import Optional
from typing import Union

from object_storage.clients import AzureBlobClient
from object_storage.clients import AzureContainerClient
from object_storage.managers import AzureBlobStorageManager
from object_storage.providers.enum import Provider


def get_file_client(provider: Union[Provider, str], sas_url: Optional[str] = None) -> Optional[AzureBlobClient]:
    """Returns an instance of an file client for the given provider and sas url."""

    provider = Provider(provider)
    if provider == Provider.AZURE:
        if sas_url is None:
            raise ValueError('sas_url is mandatory to AzureBlobClient')
        client = AzureBlobClient(blob_sas_url=sas_url)
    return client


def get_container_client(
    provider: Union[Provider, str], sas_url: Optional[str] = None
) -> Optional[AzureContainerClient]:
    """Returns an instance of an container client for the given provider and sas url."""

    provider = Provider(provider)
    if provider == Provider.AZURE:
        if sas_url is None:
            raise ValueError('sas_url is mandatory to AzureContainerClient')
        client = AzureContainerClient(container_sas_url=sas_url)
    return client


def get_manager(
    provider: Union[Provider, str], connection_string: Optional[str] = None
) -> Optional[AzureBlobStorageManager]:
    """Returns an instance of an manager client for the given provider and connection string."""

    provider = Provider(provider)
    if provider == Provider.AZURE:
        if connection_string is None:
            raise ValueError('connection_string is mandatory to AzureBlobClient')
        client = AzureBlobStorageManager(connection_string=connection_string)
    return client


__all__ = ['get_file_client', 'get_container_client', 'get_manager']

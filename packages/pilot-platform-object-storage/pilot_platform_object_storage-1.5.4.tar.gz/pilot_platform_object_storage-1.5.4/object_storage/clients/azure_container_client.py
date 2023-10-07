# Copyright (C) 2023 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import logging
from io import BytesIO
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from azure.storage.blob import BlobBlock
from azure.storage.blob import BlobProperties
from azure.storage.blob.aio import ContainerClient

from object_storage.clients.base_container_client import BaseContainerClient
from object_storage.providers.azure import AzureClient

logger = logging.getLogger('pilot.object-storage')


class AzureContainerClient(BaseContainerClient, AzureClient):
    """A client for interacting with Azure Blob Storage.

    Inherits from:
        - BaseObjectStorageClient: to provide a generic interface for object storage clients

    :param container_sas_url:
        SAS URL to an Azure Blob Storage Container.
    """

    def __init__(
        self,
        container_sas_url: str,
    ):
        self.container_sas_url = container_sas_url

    async def is_exists(self) -> bool:
        """Checks if container in the context exists."""

        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                return await container_client.exists()
        except Exception as exc:
            raise self._handle_exception(exc)

    async def is_file_exists(self, key: str) -> bool:
        """Checks if container in the context exists."""

        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                blob_client = container_client.get_blob_client(key)
                return await blob_client.exists()
        except Exception as exc:
            raise self._handle_exception(exc)

    async def delete(self) -> Dict[str, Any]:
        """Deletes the specific container in the context from the Storage."""

        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                return await container_client.delete_container()
        except Exception as exc:
            raise self._handle_exception(exc)

    async def upload_file(
        self,
        key: str,
        file_path: str,
        chunk_size: int = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> Dict[str, Any]:
        """Uploads a file to a blob in the specified container."""
        try:
            async with ContainerClient.from_container_url(
                container_url=self.container_sas_url, max_block_size=chunk_size
            ) as container_client:
                blob_client = container_client.get_blob_client(key)
                return await self._upload(blob_client, file_path, key, progress_callback, chunk_size=chunk_size)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def upload_file_from_bytes(
        self,
        key: str,
        buffer: BytesIO,
        chunk_size: int = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> Dict[str, Any]:
        """Uploads a file to a blob in the specified container."""
        try:
            async with ContainerClient.from_container_url(
                container_url=self.container_sas_url, max_block_size=chunk_size
            ) as container_client:
                blob_client = container_client.get_blob_client(key)
                return await self._upload_from_byte(blob_client, key, buffer, chunk_size, progress_callback)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def resume_upload(
        self,
        key: str,
        file_path: str,
        chunk_size: int = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> None:
        """Uploads a file to an Azure Blob Storage container, resuming an interrupted upload if there is an uncommitted
        block list."""
        try:
            async with ContainerClient.from_container_url(
                container_url=self.container_sas_url, max_block_size=chunk_size
            ) as container_client:
                blob_client = container_client.get_blob_client(key)
                await self._resume_upload(blob_client, key, file_path, chunk_size, progress_callback)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def download_file_to_bytes(
        self,
        key: str,
        chunk_size: Optional[int] = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> bytes:
        """Download a file from the specified container."""
        try:
            async with ContainerClient.from_container_url(
                container_url=self.container_sas_url, max_chunk_get_size=chunk_size
            ) as container_client:
                blob_client = container_client.get_blob_client(key)
                return await self._download_bytes(blob_client, key, progress_callback=progress_callback)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def download_file(
        self,
        key: str,
        file_path: str,
        chunk_size: Optional[int] = 4 * 1024 * 1024,
        progress_callback: Optional[Callable[[str, int, int], Awaitable[Any]]] = None,
    ) -> None:
        """Download a file from the specified container."""

        await self._create_parent_dir(file_path)
        try:
            async with ContainerClient.from_container_url(
                container_url=self.container_sas_url, max_chunk_get_size=chunk_size
            ) as container_client:
                blob_client = container_client.get_blob_client(key)
                await self._download(
                    blob_client, key, file_path, get_chunk_size=chunk_size, progress_callback=progress_callback
                )
        except Exception as exc:
            raise self._handle_exception(exc)

    async def copy_file_from_url(
        self,
        key: str,
        source_url: str,
    ) -> str:
        """Copies a file from a URL to a blob in the specified container."""
        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                blob_client = container_client.get_blob_client(key)
                return await self._copy_from_url(blob_client, source_url)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def delete_file(self, key: str) -> None:
        """Deleted a file with all its snapshots."""
        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                blob_client = container_client.get_blob_client(key)
                return await self._delete(blob_client)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def delete_versions(self, key: str, permanent_delete: bool = False) -> None:
        """Deleted the versions in the file."""
        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                version_ids = await self._get_blob_versions(container_client, key)
                await self._delete_versions(container_client, key, version_ids, permanent_delete)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def delete_file_with_versions(self, key: str, permanent_delete: bool = False) -> None:
        """Deleted a file with all its snapshots. Also delete the version of the file for soft deletion.

        Also allowed the permanent delete of the deleted blob
        """
        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                if not permanent_delete:
                    blob_client = container_client.get_blob_client(blob=key)
                    await self._delete(blob_client)
                version_ids = await self._get_blob_versions(container_client, key)
                await self._delete_versions(container_client, key, version_ids, permanent_delete)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def batch_delete_files_with_versions(self, keys: List[str], permanent_delete: bool = False) -> None:
        """Deleted a list of files with all its snapshots. Also delete the version of the files for soft deletion.

        Also allowed the permanent delete of the deleted blob
        """
        try:
            for key in keys:
                await self.delete_file_with_versions(key, permanent_delete)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def get_file_url(
        self,
        key: str,
    ) -> str:
        """Returns the URL that can be used to access the specified file."""
        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                blob_client = container_client.get_blob_client(key)
                return blob_client.url
        except Exception as exc:
            raise self._handle_exception(exc)

    async def get_file_properties(
        self,
        key: str,
    ) -> BlobProperties:
        """Retrieves the properties of a blob in the specified container."""
        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                blob_client = container_client.get_blob_client(blob=key)
                return await blob_client.get_blob_properties()
        except Exception as exc:
            raise self._handle_exception(exc)

    async def commit_file(self, key: str) -> None:
        """Commits the uncommitted blocks of a blob, making them a part of the blob's content."""

        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                blob_client = container_client.get_blob_client(blob=key)
                await self._commit_blob(blob_client)
        except Exception as exc:
            raise self._handle_exception(exc)

    async def get_file_chunks(self, key: str) -> Tuple[List[BlobBlock], List[BlobBlock]]:
        """Returns a list of committeed and uncommitted the info of blob chunks."""

        try:
            async with ContainerClient.from_container_url(container_url=self.container_sas_url) as container_client:
                blob_client = container_client.get_blob_client(blob=key)
                return await self._get_blob_chunks(blob_client)
        except Exception as exc:
            raise self._handle_exception(exc)

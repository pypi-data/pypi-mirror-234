# Copyright (C) 2023 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List


class BaseObjectStorageManager(ABC):
    """Abstract base class for object storage managers."""

    @abstractmethod
    async def create_container(self, container_name: str) -> Dict[str, Any]:
        """Creates a container in the object storage service."""

        raise NotImplementedError()

    @abstractmethod
    async def delete_container(self, container_name: str) -> Dict[str, Any]:
        """Deletes container from the object storage service."""

        raise NotImplementedError()

    @abstractmethod
    async def list_objects(self, container_name: str) -> List[str]:
        """Lists all objects in the specified container."""

        raise NotImplementedError()

    @abstractmethod
    async def is_container_exists(self, container_name: str) -> bool:
        """Checks if container with `container_name` exists in the Storage."""

        raise NotImplementedError()

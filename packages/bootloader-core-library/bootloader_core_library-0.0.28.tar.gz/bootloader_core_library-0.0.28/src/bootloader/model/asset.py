# Copyright (C) 2023 Bootloader.  All rights reserved.
#
# This software is the confidential and proprietary information of
# Bootloader or one of its subsidiaries.  You shall not disclose this
# confidential information and shall use it only in accordance with the
# terms of the license agreement or other applicable agreement you
# entered into with Bootloader.
#
# BOOTLOADER MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR
# A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.  BOOTLOADER SHALL NOT BE
# LIABLE FOR ANY LOSSES OR DAMAGES SUFFERED BY LICENSEE AS A RESULT OF
# USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.

from __future__ import annotations

import json
import logging
import os
from abc import abstractmethod
from os import PathLike
from typing import Type, Any
from uuid import UUID

from majormode.perseus.constant.obj import ObjectStatus
from majormode.perseus.model import obj
from majormode.perseus.model.date import ISO8601DateTime
from majormode.perseus.model.version import Version
from majormode.perseus.utils import cast


class Asset:
    """
    Represent an asset used by a game engine (Unreal Engine, Unity, etc.).
    """
    def __eq__(self, other: Asset) -> bool:
        """
        Check whether this asset is the same as another asset.

        Two assets are different if their identifiers, their data's size, and/or
        checksum are different.  Otherwise, they are equivalent if they have the
        same name, the same class, and the same package name.


        :param other: Another asset.


        :return: ``True`` if the two assets are the same; ``False`` otherwise.
        """
        if other is None:
            return False

        # Compare the identifier of the assets when defined.
        #
        # :note: Two assets with the same identifiers are not necessarily the
        #    same. The content of the asset may have changed.
        if self._asset_id is not None and other.asset_id is not None \
           and self._asset_id != other.asset_id:
            return False

        # Compare the respective assets' size and checksum when defined.
        if self._data_size is not None and other.data_size is not None \
           and self._data_checksum is not None and other.data_checksum is not None \
           and (self._data_size != other.data_size
                or self.data_checksum != other.data_checksum):
            return False

        # Compare the metadata of the assets.
        #
        # :todo: The class of an asset CANNOT change; however the package name
        #     of the asset, and even the name of the asset, CAN change.  In such
        #     case, the following test is buggy.
        return self._asset_class_path == other.asset_class_path \
            and self._asset_name == other.asset_name \
            and self._package_name == other.package_name

    def __init__(
            self,
            asset_name: str,
            asset_class_path: str,
            package_name: str,
            dependencies: list[str] or None,
            asset_id: UUID or None = None,
            data_size: int or None = None,
            data_checksum: str or None = None,
            object_status: ObjectStatus = None,
            references: list[str] or None = None,
            tags: list[str] or None = None,
            update_time: ISO8601DateTime or None = None,
            version_code: int or None = None):
        """
        Build a new {@link UAsset}.


        :param asset_name: The name of the asset without the package.

        :param asset_class_path: The path name of the asset’s class.

        :param package_name: The name of the package in which the asset is
            found.

        :param dependencies: The list of names of the packages that the asset
            depends on.

        :param asset_id: The identification of the asset, when already
            registered to the back-end platform.

        :param data_size: The size in bytes of the asset's binary data.

        :param data_checksum: The SHA256 message digest of the asset's binary
            data of the asset file.

        :param object_status: The current status of the asset.

        :param references: The list of pacakge names of the asset that depend
            on this asset.

        :param tags: The list of tags associated with the asset.

        :param update_time: The time of the most recent modification of some
            mutable attributes of the asset, such as its status, its list of
            tags, and its picture.

        :param version_code: A positive integer used as an internal version
            number.  This number helps determine whether one version is more
            recent than another, with higher numbers indicating more recent
            versions.
        """
        self._asset_class_path = asset_class_path
        self._asset_id = asset_id
        self._asset_name = asset_name
        self._dependencies = dependencies
        self._data_checksum = data_checksum
        self._data_size = data_size
        self._object_status = object_status
        self._package_name = package_name
        self._references = references
        self._tags = tags
        self._update_time = update_time
        self._version_code = version_code

    def __str__(self):
        """
        Return the string representation of this asset.


        :return: Return a stringified JSON expression of this asset.
        """
        return json.dumps(obj.stringify(self.to_json(), trimmable=True))


    @property
    @abstractmethod
    def asset_class_name(self) -> str or None:
        """
        Return the humanly readable name of the asset's class.


        :return: The humanly readable name of the asset's class, or ``None``
            if the asset's class doesn't correspond to a game engine core
            class.
        """

    @property
    def asset_class_path(self) -> str:
        """
        Return the path name of the asset's class.


        :return: The path name of the asset's class.
        """
        return self._asset_class_path

    @property
    def asset_id(self) -> UUID:
        if self._asset_id is None:
            raise ValueError(f"No identification defined for the asset {self._package_name}")

        return self._asset_id

    @asset_id.setter
    def asset_id(self, asset_id: UUID):
        if asset_id is None:
            raise ValueError("Cannot set the asset's identifier with a null value")

        if self._asset_id is None:
            self._asset_id = asset_id
        elif self._asset_id == asset_id:
            raise ValueError(f"The asset {self._asset_name} has already an identifier ({self._asset_id})")

    @property
    def asset_name(self) -> str:
        """
        Return the name of the asset.


        :return: The name of the asset without the package.
        """
        return self._asset_name

    @asset_name.setter
    def asset_name(self, asset_name):
        """
        Change the name of the asset.


        :param asset_name: The new name of the asset without the package.
        """
        if asset_name is None:
            raise ValueError("Cannot set the asset's name with a null value")

        if self._asset_name is None:
            self._asset_name = asset_name
        elif self._asset_name != asset_name:
            raise ValueError(f"The asset {self._asset_name} has already a name ({self._asset_name})")

    @property
    def data_checksum(self) -> str:
        """
        Return the SHA256 message digest of the asset's binary data.


        :return: The SHA256 message digest of the asset's binary data.
        """
        return self._data_checksum

    @data_checksum.setter
    def data_checksum(self, data_checksum: str):
        """
        Set the SHA256 message digest of the asset's binary data when its
        content has changed.


        :param data_checksum: The SHA256 message digest of the asset's binary
            data.
        """
        if data_checksum is None:
            raise ValueError("Cannot set the asset's data checksum with a null value")

        if self._data_checksum is None:
            self._data_checksum = data_checksum
        elif self._data_checksum != data_checksum:
            raise ValueError(f"The asset {self._asset_name} has already a data checksum ({self._data_checksum})")

    @property
    def data_size(self) -> int:
        """
        Return the size of the asset's binary data.


        :return: The size in bytes of the asset's binary data.
        """
        return self._data_size

    @data_size.setter
    def data_size(self, data_size: int):
        """
        Set the size of the asset's binary data when its content has changed.


        :param data_size: The size in bytes of the asset's binary data.
        """
        if data_size is None:
            raise ValueError("Cannot set the asset's data size with a null value")

        if self._data_size is None:
            self._data_size = data_size
        elif self._data_size != data_size:
            raise ValueError(f"The asset {self._asset_name} has already a data size ({self._data_size})")

    @property
    def dependencies(self) -> list[str]:
        """
        Return the list of names of the packages that the asset depends on.


        :return: The list of names of the packages that the asset depends on.
        """
        return self._dependencies or []

    @property
    @abstractmethod
    def file_name(self) -> str:
        """
        Return the asset's file name.


        :return: The asset's file name.
        """

    @property
    @abstractmethod
    def file_path_name(self) -> PathLike:
        """
        Return the asset's file path name.


        :note: The file path is relative to the project's root folder.


        :return: The asset's file path name.
        """

    @property
    def fully_qualified_name(self):
        """
        Return the Fully Qualified Name (FQN) of the asset composed of the
        package and the name of the asset.


        :return: The Fully Qualified Name (FQN) of the asset.
        """
        return os.path.join(self._package_name, self.asset_name)

    @classmethod
    def from_json(cls, payload: Any):
        if isinstance(payload, str):
            payload = json.loads(payload)

        return cls(
            payload['asset_name'],
            payload['asset_class_path'],
            payload['package_name'],
            payload['dependencies'],
            asset_id=cast.string_to_uuid(payload.get('asset_id')),
            data_size=payload.get('data_size'),
            data_checksum=payload.get('data_checksum'),
            object_status=cast.string_to_enum(payload.get('object_status'), ObjectStatus),
            references=payload.get('reference'),
            tags=payload.get('tags'),
            update_time=cast.string_to_timestamp(payload.get('update_time')),
            version_code=Version.from_string(payload.get('version_code'))
        )

    @classmethod
    def from_object(cls, o: Any):
        if o is None:
            return None

        return cls(
            o.asset_name,
            o.asset_class_path,
            o.package_name,
            getattr(o, 'dependencies', None),
            asset_id=getattr(o, 'asset_id', None),
            data_size=getattr(o, 'data_size', None),
            data_checksum=getattr(o, 'data_checksum', None),
            object_status=getattr(o, 'object_status', None),
            references=getattr(o, 'reference', None),
            tags=getattr(o, 'tags', None),
            update_time=getattr(o, 'update_time', None),
            version_code=getattr(o, 'version_code', None)
        )

    @abstractmethod
    def is_game_engine_core_class(self):
        """
        Indicate whether this asset is of a core class of the game engine.

        Developers can create their own asset classes that may be specific to
        their game.

        :return: ``True`` if this asset is of a game engine's core class;
            ``False`` if this asset has a custom class.
        """

    @abstractmethod
    def is_storable(self) -> bool:
        """
        Indicate whether this asset needs to be stored in the inventory.


        :return: ``true`` if the asset needs to be stored in the inventory;
            ``false`` otherwise.
        """

    @property
    def object_status(self) -> ObjectStatus or None:
        """
        Return The current status of the asset.


        :return: The current status of the asset.
        """
        return self._object_status

    @property
    def package_name(self) -> str:
        """
        Return the name of the package in which the asset is found.


        :return: The name of the package in which the asset is found.
        """
        return self._package_name

    @package_name.setter
    def package_name(self, package_name: str):
        """
        Change the package name of the asset.


        :param package_name: The new name of the asset's package.
        """
        if package_name is None:
            raise ValueError("Cannot set the asset's package name with a null value")

        if self._package_name is None:
            self._package_name = package_name
        elif self._package_name != package_name:
            raise ValueError(f"The asset {self._asset_name} has already a package name ({self._package_name})")


    @property
    def references(self) -> list[str] or None:
        """
        Return the list of names of the packages of the assets that reference
        this asset.


        :return: The list of names of the packages of the assets that
            reference this asset.
        """
        return self._references

    @property
    def tags(self) -> list[str] or None:
        """
        Return the list of tags associated to the asset.


        :return: The list of tags associated with the asset.
        """
        return self._tags

    def to_json(self) -> Any:
        """
        Serialize the asset's information to a JSON expression.


        :return: A JSON expression representing the asset's information.
        """
        return {
            'asset_id': self._asset_id,
            'asset_name': self._asset_name,
            'asset_class_path': self._asset_class_path,
            'dependencies': self._dependencies,
            'data_size': self._data_size,
            'data_checksum': self._data_checksum,
            'object_status': self._object_status,
            'package_name': self._package_name,
            'references': self._references,
            'tags': self._tags,
            'update_time': self._update_time,
            'version_code': self._version_code,
        }

    @property
    def update_time(self) -> ISO8601DateTime or None:
        """
        Return the time of the most recent modification of some mutable
        attributes of the asset.

        The mutable attributes of the asset are its status, the list of
        its tags, and its picture.


        :return: The time of the most recent modification of some mutable
            attributes of the asset.
        """
        return self._update_time

    @property
    def version_code(self) -> int or None:
        """
        Return a positive integer used as an internal version number.

        This number helps determine whether one version is more recent than
        another, with higher numbers indicating more recent versions.


        :return: A positive integer used as an internal version number.
        """
        return self._version_code

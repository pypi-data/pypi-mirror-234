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

import logging
from os import PathLike
from pathlib import Path

from majormode.perseus.utils import cast

from bootloader.constant.ue_asset import ASSET_CLASS_NAME_MAPPING
from bootloader.constant.ue_asset import UnrealEngineAssetClass
from bootloader.model.asset import Asset


class UnrealEngineAsset(Asset):
    # The default extension (suffix) of an Unreal Editor asset file.
    UNREAL_ENGINE_ASSET_FILE_EXTENSION = '.uasset'

    # The path prefix of Unreal Engine core classes.
    UNREAL_ENGINE_CORE_CLASS_PATH_PREFIX = '/Script/Engine/'

    # The class of an Unreal Engine asset world.
    UNREAL_ENGINE_WORLD_ASSET_CLASS = '/Script/Engine/World'

    @property
    def file_name(self) -> str:
        """
        Return the asset's file name.


        :return: The asset's file name.
        """
        return f'{self._asset_name}.{self.UNREAL_ENGINE_ASSET_FILE_EXTENSION}'

    @property
    def file_path_name(self) -> PathLike:
        """
        Return the asset's file name.


        :return: The asset's file name.
        """
        pathname = self._package_name.replace('Game', 'Content')
        return Path(f'{pathname}.{self.UNREAL_ENGINE_ASSET_FILE_EXTENSION}')

    def is_storable(self) -> bool:
        """
        Indicate whether this asset needs to be stored in the inventory.


        :return: ``true`` is the asset needs to be stored in the inventory;
            ``false`` otherwise.
        """
        return self._asset_class_path == '/Script/Engine/World'

    @property
    def asset_class(self) -> UnrealEngineAssetClass:
        """
        Return the asset's class.

        For example, the class of a ``/Script/Engine/SkeletalMesh`` asset is
        ``UnityEngineAssetClass.SkeletalMesh``.


        :return: The class of the asset, or ``None`` if the class is not defined
            (i.e., a user-defined class).
        """
        class_name = self._asset_class_path.split('/')[-1]
        try:
            asset_class = cast.string_to_enum(class_name, UnrealEngineAssetClass)
            return asset_class
        except ValueError as error:
            logging.exception(error)

    @property
    def asset_class_name(self) -> str:
        """
        Return the humanly readable name of the asset's class.

        For example, the humanly readable name of the class
        `/Script/Engine/SkeletalMesh` is `Skeletal Mesh`.


        :return: The humanly readable name of the asset's class, or ``None``
            if the asset's class doesn't correspond to an Unreal Engine
            standard class.
        """
        asset_class_name = ASSET_CLASS_NAME_MAPPING.get(self.asset_class)
        if asset_class_name is None and self.is_game_engine_core_class():
            logging.warning(
                f"The Unreal Engine class {self.asset_class} might not be properly "
                f"declared in the enumeration 'UnrealEngineAssetClass'"
            )
        return asset_class_name

    def is_game_engine_core_class(self):
        """
        Indicate whether this asset is of a Unreal Engine's core class.

        Unreal Engine classes are prefixed with ``/Script/Engine/``.


        :return: ``True`` if this asset is of a Unreal Engine core class;
            ``False`` if this asset has a custom class.
        """
        return self.asset_class_path.startswith(self.UNREAL_ENGINE_CORE_CLASS_PATH_PREFIX)

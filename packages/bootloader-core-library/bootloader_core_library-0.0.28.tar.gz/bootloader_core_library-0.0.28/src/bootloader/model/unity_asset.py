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

import logging
from os import PathLike
from pathlib import Path

from majormode.perseus.utils import cast

from bootloader.constant.unity_asset import ASSET_CLASS_NAME_MAPPING, UnityAssetClass
from bootloader.model.asset import Asset


class UnityAsset(Asset):
    # The path prefix of Unity core classes.
    UNITY_CORE_CLASS_PATH_PREFIX = 'UnityEngine.'

    @property
    def asset_class(self) -> UnityAssetClass:
        """
        Return the asset's class.

        For example, the class of a ``UnityEngine.Material`` asset is
        ``UnityAssetClass.Material``.


        :return: The class of the asset, or `None` if the class is not defined
            (i.e., a user-defined class).
        """
        class_name = self._asset_class_path.split('.')[-1]
        try:
            asset_class = cast.string_to_enum(class_name, UnityAssetClass)
            return asset_class
        except ValueError as error:
            logging.exception(error)

    @property
    def asset_class_name(self) -> str or None:
        asset_class_name = ASSET_CLASS_NAME_MAPPING.get(self.asset_class)
        if asset_class_name is None and self.is_game_engine_core_class():
            logging.warning(
                f"The Unity class {self.asset_class} might not be properly "
                f"declared in the enumeration 'UnityAssetClass'"
            )
        return asset_class_name

    @property
    def file_name(self) -> str:
        """
        Return the asset's file name.


        :return: The asset's file name.
        """
        return self._asset_name

    @property
    def file_path_name(self) -> PathLike:
        """
        Return the asset's file name.


        :return: The asset's file name.
        """
        return Path(self._package_name, self.file_name)

    def is_game_engine_core_class(self):
        """
        Indicate whether this asset is a Unity's core class.


        :return: ``True`` if this asset is a Unity's core class; ``False`` if
            this asset has a custom class.
        """
        return self.asset_class_path.startswith(self.UNITY_CORE_CLASS_PATH_PREFIX)

    def is_storable(self) -> bool:
        """
        Indicate whether this asset needs to be stored in the inventory.


        :return: ``true`` is the asset needs to be stored in the inventory;
            ``false`` otherwise.
        """
        return True

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

from os import PathLike
from pathlib import Path

from bootloader.model.asset import Asset


class UnityAsset(Asset):
    # The path prefix of Unity core classes.
    UNREAL_ENGINE_STANDARD_CLASS_PATH_PREFIX = 'Packages/com.unity.'

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

    def is_storable(self) -> bool:
        """
        Indicate whether this asset needs to be stored in the inventory.


        :return: ``true`` is the asset needs to be stored in the inventory;
            ``false`` otherwise.
        """
        return True

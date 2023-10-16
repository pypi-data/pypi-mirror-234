#
#  This file is part of IOCBIO Gel.
#
#  SPDX-FileCopyrightText: 2022-2023 IOCBIO Gel Authors
#  SPDX-License-Identifier: GPL-3.0-or-later
#


import hashlib
import os
from typing import Optional

import numpy as np

from iocbio.gel.domain.gel_image import GelImage


class ProcessingCache:
    """
    Cache processed image matrices to speed up UX.
    """

    PROCESSING_PATH = "processing"

    @staticmethod
    def background_key(gel_image: GelImage) -> Optional[str]:
        return "{}/{}/{}/{}/{}".format(
            gel_image.hash,
            gel_image.region,
            gel_image.rotation,
            gel_image.background_subtraction,
            gel_image.background_is_dark,
        )

    @staticmethod
    def region_key(gel_image: GelImage) -> Optional[str]:
        return "{}/{}/{}".format(gel_image.hash, gel_image.region, gel_image.rotation)

    def __init__(self, cache_path: str):
        self.cache_path = os.path.join(cache_path, self.PROCESSING_PATH)
        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path)

    def get(self, key: str):
        """
        Loads step numpy matrix from a cache file.
        """
        if key is None:
            return None

        file = self._get_file_path(key)
        if not os.path.exists(file):
            return None

        with open(file, "rb") as f:
            return np.load(f, allow_pickle=True)

    def set(self, key: str, data):
        """
        Saves step numpy matrix to a cache file.
        """
        if key is None:
            return

        file = self._get_file_path(key)
        if os.path.exists(file):
            os.remove(file)

        with open(file, "wb") as f:
            np.save(f, data)

    def _get_file_path(self, param: str) -> Optional[str]:
        file_name = hashlib.sha256(param.encode("utf-8")).hexdigest()
        return os.path.join(self.cache_path, file_name + ".npy")

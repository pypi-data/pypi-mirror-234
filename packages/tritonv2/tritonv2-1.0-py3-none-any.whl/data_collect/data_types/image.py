# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
image data type for data collect
"""
import PIL.Image
import numpy as np
from typing import Union

from .blob import Blob


class Image(Blob):
    def __init__(self,
                 data: Union[np.ndarray, PIL.Image.Image],
                 designation: str = '',
                 metadata=None
                 ) -> None:
        """
        :param data: image data
        :param designation: designation
        :param metadata: metadata
        """
        super().__init__(data, designation, metadata)

    def covert_to_rgb(self):
        """
        covert to rgb
        """
        self.data = np.asarray(self.data)
        # pillow image mode P covert to RGB 需要特别处理
        if PIL.Image.fromarray(self.data).mode == 'P':
            self.data = PIL.Image.fromarray(self.data).convert('RGB')
            return
        if PIL.Image.fromarray(self.data).mode != 'RGB':
            self.data = self.data[..., ::-1]

    def covert_cv_image(self):
        """
        covert cv image
        """
        valid_data_types = {
            "b": "bool",
            "i": "signed integer",
            "u": "unsigned integer",
            "f": "floating",
        }

        if self.data.dtype.kind not in valid_data_types:
            raise TypeError(
                f"Invalid array data type: '{self.data.dtype}'. "
                f"Must be one of {list(valid_data_types.values())}"
            )
        # only support 2D, 3D, 4D array
        if self.data.ndim not in [2, 3, 4]:
            raise ValueError(
                "`image` must be a 2D or 3D or 4D array but got a {}D array".format(self.data.ndim)
            )

        if (self.data.ndim == 3) and (self.data.shape[2] not in [1, 3, 4]):
            raise ValueError(
                "Invalid channel length: {}. Must be one of [1, 3, 4]".format(
                    self.data.shape[2]
                )
            )

        # squeeze a 3D grayscale image since `Image.fromarray` doesn't accept it.
        if self.data.ndim == 3 and self.data.shape[2] == 1:
            self.data = self.data[:, :, 0]

        if self.data.ndim == 4:
            # 4d to 3d
            self.data = self.data.squeeze()
        else:
            self._normalize_to_uint8()

        self.covert_to_rgb()

    def _normalize_to_uint8(self):
        # Based on: https://github.com/matplotlib/matplotlib/blob/06567e021f21be046b6d6dcf00380c1cb9adaf3c/lib
        # /matplotlib/image.py#L684
        is_int = np.issubdtype(self.data.dtype, np.integer)
        low = 0
        high = 255 if is_int else 1
        if self.data.min() < low or self.data.max() > high:
            self.data = np.clip(self.data, low, high)

        # float or bool
        if not is_int:
            self.data = self.data * 255

        self.data = self.data.astype(np.uint8)

    def is_bytes(self):
        """
        is bytes
        """
        return isinstance(self.data, bytes)
    
    def is_p_mode(self):
        """
        is p mode
        """
        return PIL.Image.fromarray(self.data).mode == 'P'

    def is_pillow_image(self):
        """
        is pillow image
        """
        return isinstance(self.data, PIL.Image.Image)

    def is_numpy_array(self):
        """
        is numpy array
        """
        return isinstance(self.data, np.ndarray)

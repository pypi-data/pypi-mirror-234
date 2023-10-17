# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
blob data type for data collect
"""
import typing
import numpy as np
from typing import Union


class Blob:
    def __init__(self,
                 data: Union[np.ndarray, bytes, typing.IO],
                 designation: str = '',
                 metadata=None) -> None:
        if metadata is None:
            metadata = {}
        self.data = data
        self.designation = designation
        self.metadata = metadata

# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
utils for data collect
"""
import json
import os
import numpy as np
from datetime import date, datetime, timedelta
from .constants import MODEL_NAME


def get_model_name() -> str:
    """
    get model name
    :return: str
    """
    return os.environ.get(MODEL_NAME)


class NpEncoder(json.JSONEncoder):
    """
    Numpy encoder for covert numpy type to python type
    """
    def default(self, obj): # pylint: disable=E0202
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.floating, np.complexfloating)):
            return float(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.string_):
            return str(obj)
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, timedelta):
            return str(obj)
        return super(NpEncoder, self).default(obj)

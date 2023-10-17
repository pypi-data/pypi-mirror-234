# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
correlation id utils for data collect
"""

import uuid


def generate_correlation_id() -> str:
    """
    generate correlation id
    """
    return str(uuid.uuid4().hex)

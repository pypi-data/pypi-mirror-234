# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton client package
"""
from pyrate_limiter import Limiter, RequestRate

from .constants import LimiterConfig
from .utils import gen_unique_id


class TritonClient(object):
    """
    TritonClient is a wrapper class for TritonClient
    """

    def __init__(self, limiter_config: LimiterConfig = None):
        """
        Constructor
        """
        self._client = None
        # generate a unique identifier for the limiter with per client
        self._identifier = gen_unique_id()

        self._limiter = None
        self._limiter_delay = None
        self._limiter_max_delay = None

        if limiter_config is not None and isinstance(limiter_config, LimiterConfig):
            self._limiter = Limiter(RequestRate(limiter_config.limit, limiter_config.interval))
            self._limiter_delay = limiter_config.delay
            self._limiter_max_delay = limiter_config.max_delay

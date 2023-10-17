# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
grpc interceptor
"""
from grpc_interceptor import ClientInterceptor
from pyrate_limiter import Limiter
import grpc


class rate_limit_interceptor(ClientInterceptor):
    """rate_limit_interceptor for grpc client"""

    def __init__(self, identifier=None, limiter: Limiter = None, limiter_delay=None, limiter_max_delay=None):
        self._identifier = identifier
        self._limiter = limiter
        self._limiter_delay = limiter_delay
        self._limiter_max_delay = limiter_max_delay

    def intercept(self, method, request_or_iterator, call_details):
        """
        intercept method
        """
        if self._limiter is not None:
            with self._limiter.ratelimit(
                    self._identifier,
                    delay=self._limiter_delay,
                    max_delay=self._limiter_max_delay):
                return method(request_or_iterator, call_details)
        return method(request_or_iterator, call_details)


class async_rate_limit_interceptor(grpc.aio.UnaryUnaryClientInterceptor):
    def __init__(
            self, identifier=None, limiter: Limiter = None, limiter_delay=None, limiter_max_delay=None):
        self._identifier = identifier
        self._limiter = limiter
        self._limiter_delay = limiter_delay
        self._limiter_max_delay = limiter_max_delay

    async def intercept_unary_unary(self, continuation, client_call_details, request):
        if self._limiter is not None:
            async with self._limiter.ratelimit(
                    self._identifier,
                    delay=self._limiter_delay,
                    max_delay=self._limiter_max_delay):
                return await continuation(client_call_details, request)
        return await continuation(client_call_details, request)

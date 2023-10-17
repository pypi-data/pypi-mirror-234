# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton client constants
"""
from __future__ import annotations
from typing import List
from pydantic import BaseModel

GRPC_SERVICE = "inference.GRPCInferenceService"

BENCHMARK_TASK = "benchmark"
TESTING_TASK = "testing"

class LimiterConfig(BaseModel):
    # ratelimit limit, the max request number per interval
    limit: int
    # ratelimit interval, with units as RequestRateDuration
    interval: int
    # ratelimit delay, if delay is True, the request will be delayed until the ratelimit is passed
    delay: bool = True
    # ratelimit max_delay, if delay is True, the request will be delayed until the ratelimit is passed,
    # but the max delay is max_delay
    max_delay: int = 60


class RequestRateDuration:
    SECOND = 1
    MINUTE = 60
    HOUR = 3600
    DAY = 3600 * 24
    MONTH = 3600 * 24 * 30


class NameItem(BaseModel):
    service: str


class RetryPolicy(BaseModel):
    maxAttempts: int
    initialBackoff: str
    maxBackoff: str
    backoffMultiplier: int
    retryableStatusCodes: List[str]


class MethodConfigItem(BaseModel):
    name: List[NameItem]
    retryPolicy: RetryPolicy


class ServiceConfig(BaseModel):
    methodConfig: List[MethodConfigItem]

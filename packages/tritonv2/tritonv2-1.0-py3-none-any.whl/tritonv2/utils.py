# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
triton client utils
"""
import uuid
import boto3
import shutil
import os
import numpy as np


def gen_unique_id():
    """
    Generate unique id
    """
    return str(uuid.uuid4().hex)


def list_stack_ndarray(arrays) -> np.ndarray:
    """
    Convert list of ndarrays to single ndarray with ndims+=1
    """
    lengths = list(
        map(lambda x, a=arrays: a[x].shape[0], [x for x in range(len(arrays))])
    )
    max_len = max(lengths)
    arrays = list(map(lambda a, ml=max_len: np.pad(
        a, (0, ml - a.shape[0])), arrays))
    for arr in arrays:
        assert arr.shape == arrays[0].shape, "arrays must have the same shape"
    return np.stack(arrays, axis=0)


def parse_model(model_metadata, model_config):
    """
    Check the configuration of a model to make sure it meets the
    requirements for an image classification network (as expected by
    this client)
    """
    input_metadata = model_metadata['inputs']
    output_metadata = model_metadata['outputs']

    max_batch_size = None
    if "max_batch_size" in model_config:
        max_batch_size = model_config['max_batch_size']

    return input_metadata, output_metadata, max_batch_size


class BlobStoreFactory:
    """
    BlobStoreFactory
    """

    def create(self, kind, bucket, endpoint_url, aws_access_key_id='', aws_secret_access_key='', region='bj'):
        if kind == "s3":
            return S3BlobStore(bucket, endpoint_url, aws_access_key_id, aws_secret_access_key, region)
        if kind == "local":
            return LocalBlobStore(endpoint_url)


class LocalBlobStore:
    """
    LocalBlobStore
    """

    def __init__(self, prefix_path) -> None:
        self._prefix = prefix_path+"/"

    def exist(self, path):
        """
        file exist
        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            path = self._prefix+path
            return os.path.exists(path)
        except Exception as e:
            print(f"File {path} not exist: {e}")
            return False

    def read_file(self, path):
        """
        read file
        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            path = self._prefix+path
            with open(path, "r") as f:
                data = f.read()
            return data
        except Exception as e:
            print(f"File {path} read error: {e}")
            return None

    def write_file(self, path, data):
        """
        write file
        Args:
            path (_type_): _description_
            data (_type_): _description_
        """
        if isinstance(data, bytes):
            data = data.decode("utf-8")

        with open(self._prefix+path, "w") as f:
            f.write(data)

    def copy(self, source_key, destination_key):
        """
        copy file
        Args:
            source_key (_type_): _description_
            destination_key (_type_): _description_
        """
        shutil.copy(self._prefix+source_key, self._prefix+destination_key)


class S3BlobStore:
    """
    S3BlobStore
    """

    def __init__(self, bucket, endpoint_url, aws_access_key_id, aws_secret_access_key, region):
        self._bucket = bucket
        self._client = boto3.client(
            "s3", aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key, endpoint_url=f"http://{endpoint_url}", region_name=region)

    def exist(self, path):
        """_summary_
        file exist
        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """
        try:
            self._client.head_object(Bucket=self._bucket, Key=path)
            return True
        except Exception as e:
            print(f"File {path} not exist: {e}")
            return False

    def read_file(self, path):
        """
        read file
        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = self._client.get_object(Bucket=self._bucket, Key=path)
        data = response["Body"].read()
        return data.decode("utf-8")

    def write_file(self, path, data):
        """
        write file
        Args:
            path (_type_): _description_
            data (_type_): _description_
        """
        self._client.put_object(Body=data, Bucket=self._bucket, Key=path)

    def copy(self, source_key, destination_key):
        """
        copy file
        Args:
            source_key (_type_): _description_
            destination_key (_type_): _description_
        """
        copy_source = {"Bucket": self._bucket, "Key": source_key}
        self._client.copy_object(
            CopySource=copy_source, Bucket=self._bucket, Key=destination_key)

# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
DataCollectClient Library
"""
import datetime
import json
import mimetypes
import os
import time
from pathlib import Path
from typing import Union, Sequence, Dict, List, Any, Mapping
from pydantic import BaseModel

from .constants import (
    DEFAULT_CAPTURE_LOG_DIR, DEFAULT_CAPTURE_BLOB_DIR,
    CAPTURE_LOG_DIR, CAPTURE_BLOB_DIR,
    ENABLE_CAPTURE_INPUT, ENABLE_CAPTURE_PREDICTION, ENABLE_CAPTURE_GROUND_TRUTH, DEFAULT_CAPTURE_INPUT_DESIGNATION,
    TIME_DIRECTORY_FORMAT, DEFAULT_CAPTURE_PREDICTION_DESIGNATION, CAPTURE_LOG_ROTATION, CAPTURE_LOG_RETENTION,
    DEFAULT_CAPTURE_LOG_ROTATION, DEFAULT_CAPTURE_LOG_RETENTION, CV2_IMWRITE_VALID_CONTENT_TYPE,
)
from .logger import LineLogger, BlobLogger, ImageLogger
from .utils import get_model_name, NpEncoder
from .data_types.blob import Blob as WindmillBlob
from .data_types.image import Image as WindmillImage
from .data_types.text import Text as WindmillText


class DataCollectConfig(BaseModel):
    """Config model"""
    model_name: str = ''
    logger_name: str = ''
    log_path: str = ''
    blob_path: str = ''
    input_enable: bool = True
    prediction_enable: bool = True
    ground_truth_enable: bool = True
    max_workers: int = 1

    class Config:
    """Config model config"""
        protected_namespaces = ()


class DataCollectClient:
    """
    DataCollectClient
    """

    def __init__(self, config):
        """
        init logger
        :path log_dir_path:
        """
        self._load_env_setting_and_config(config)
        self._init_base_logger()

    def blob_logger(self):
        """
        get blob logger
        :return:
        """
        return self._blob_logger

    def image_logger(self):
        """
        get image logger
        :return:
        """
        return self._image_logger

    def _init_base_logger(self):
        """
        init base logger
        :return:
        """
        log_file_dir = f"{self.log_path}/{DEFAULT_CAPTURE_PREDICTION_DESIGNATION}"
        log_file_dir = Path(log_file_dir)
        log_file_dir.mkdir(parents=True, exist_ok=True)

        self._logger = LineLogger({
            'file_path': f'{log_file_dir}/result.jsonl',
            'rotation': self.log_rotation,
            'retention': self.log_retention,
            'max_workers': self.max_workers,
        })

        self._blob_logger = BlobLogger({'max_workers': self.max_workers})
        self._image_logger = ImageLogger({'max_workers': self.max_workers})

    def _is_data_capture_enable(self):
        """
        check is need print log
        :return:
        """
        return self.input_enable or \
            self.prediction_enable or \
            self.ground_truth_enable

    def gen_image_save_path(self, correlation_id: str, designation: str = '', metadata=None) -> str:
        """
        generate image tmp save dir as yyyy-MM-dd/hh
        :return:
        """
        # generate time directory
        if metadata is None:
            metadata = {}
        if len(designation) == 0:
            designation = DEFAULT_CAPTURE_INPUT_DESIGNATION
        time_tuple = time.localtime(int(time.time()))
        dir_name = os.path.join(f"{self.blob_path}/{designation}",
                                time.strftime(TIME_DIRECTORY_FORMAT, time_tuple))
        dir_name = Path(dir_name)
        dir_name.mkdir(parents=True, exist_ok=True)
        file_name = correlation_id
        if metadata.get('sub_name'):
            file_name = f'{file_name}_{metadata.get("sub_name")}'
        file_path = f"{dir_name}/{file_name}"
        # validate content type and set file extension
        content_type = metadata.get('content_type', 'image/jpeg')
        if content_type is not None and content_type not in CV2_IMWRITE_VALID_CONTENT_TYPE:
            content_type = 'image/jpeg'  # default content type .jpeg
        ext = mimetypes.guess_extension(content_type)
        file_path += ext
        return file_path

    def _gen_default_message(self, correlation_id: str) -> {}:
        """
        generate default message
        :param correlation_id:
        :return:
        """
        message = {
            'correlation_id': correlation_id,
            'model_name': self.model_name,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return message

    def log(self,
            correlation_id: str,
            logline: Dict[str, Any] = None,
            designation: str = '',
            text: Sequence = None,
            time_series: Sequence = None,
            blob_paths: Union[Dict, List, str] = None,
            image: WindmillImage = None,
            blob: Union[WindmillText, WindmillBlob] = None,
            prediction: Union[Dict, List, str] = None,
            ground_truth: Union[Dict, List] = None,
            config: DataCollectConfig = None,
            ):
        """
        data capture main log function
        :param correlation_id: 请求id，用于关联请求和响应
        :param logline: 日志行，字典类型，key为字符串，value为字符串、数字、列表、字典
        :param designation: 用于区分不同的数据类型，如input、prediction、ground_truth
        :param blob: 二进制文件 类型定义在data_types/blob.py
        :blob_paths: 二进制文件路径，用于记录二进制文件路径，类型为dict、list、str
        :param image: 图片 data_types/image.py
        :param text: 文本，本期未支持，预留记录nlp模型的输出
        :param time_series: 时间序列，本期未支持
        :param prediction: 模型预测结果
        :param ground_truth: ground truth 本期未支持
        :param config: DataCollectConfig 支持在log时重新执行DataCollectConfig
        :return:
        """
        if prediction is not None:
            assert isinstance(prediction, (dict, list, str)
                              ), "prediction must be a dict, list, or str"

        if config is not None:
            self._load_env_setting_and_config(config)
            self._init_base_logger()

        message = None

        if logline is not None:
            message = self._gen_default_message(correlation_id)
            if not isinstance(logline, Mapping):
                raise ValueError("data must be passed a dictionary")

            if any(not isinstance(key, str) for key in logline.keys()):
                raise ValueError("Key values passed to data must be strings.")

            for k, v in logline.items():
                if isinstance(v, (list, dict)):
                    message[k] = json.dumps(v, cls=NpEncoder)
                if isinstance(v, (int, float, str)):
                    message[k] = v

        if prediction is not None and self.prediction_enable:
            if message is None:
                message = self._gen_default_message(correlation_id)
            message['prediction'] = prediction if isinstance(prediction, str) else json.dumps(prediction,
                                                                                              cls=NpEncoder)
        if ground_truth is not None and self.ground_truth_enable:
            if message is None:
                message = self._gen_default_message(correlation_id)
            message['ground_truth'] = ground_truth if isinstance(ground_truth, str) else json.dumps(ground_truth,
                                                                                                    cls=NpEncoder)
        if image is not None and self.input_enable:
            self._log_image(correlation_id, image, designation)

        if blob is not None and self._is_data_capture_enable():
            self._log_blob(correlation_id, blob, designation)

        if blob_paths is not None and self._is_data_capture_enable():
            message['blob_paths'] = blob_paths

        if self._is_data_capture_enable() and message is not None:
            self._logger.log(message)

    def _load_env_setting_and_config(self, config: DataCollectConfig):
        """
        load env setting and config
        :param config:
        :return:
        """
        # config优先级高于env
        self.model_name = config.model_name if len(
            config.model_name) > 0 else get_model_name()

        self.log_path = os.environ.get(CAPTURE_LOG_DIR).rstrip("/") if os.environ.get(
            CAPTURE_LOG_DIR) is not None else DEFAULT_CAPTURE_LOG_DIR
        if len(config.log_path) > 0:
            self.log_path = config.log_path.rstrip("/")

        self.blob_path = os.environ.get(CAPTURE_BLOB_DIR).rstrip("/") if os.environ.get(
            CAPTURE_BLOB_DIR) is not None else DEFAULT_CAPTURE_BLOB_DIR
        if len(config.blob_path) > 0:
            self.blob_path = config.blob_path.rstrip("/")

        self.input_enable = os.environ.get(ENABLE_CAPTURE_INPUT) == "True"
        if config.input_enable is not None:
            self.input_enable = config.input_enable

        self.prediction_enable = os.environ.get(
            ENABLE_CAPTURE_PREDICTION) == "True"
        if config.prediction_enable is not None:
            self.prediction_enable = config.prediction_enable

        self.ground_truth_enable = os.environ.get(
            ENABLE_CAPTURE_GROUND_TRUTH) == "True"
        if config.ground_truth_enable is not None:
            self.ground_truth_enable = config.ground_truth_enable

        self.log_rotation = os.environ.get(CAPTURE_LOG_ROTATION) if os.environ.get(
            CAPTURE_LOG_ROTATION) is not None else DEFAULT_CAPTURE_LOG_ROTATION

        self.log_retention = int(os.environ.get(CAPTURE_LOG_RETENTION)) if os.environ.get(
            CAPTURE_LOG_RETENTION) is not None else DEFAULT_CAPTURE_LOG_RETENTION

        self.max_workers = config.max_workers

    def _log_image(self,
                   correlation_id: str,
                   image: WindmillImage,
                   designation: str = ''):
        """
            Log an image as an file. The following image objects are supported:

            - `numpy.ndarray`_
            - `PIL.Image.Image`_

            .. _numpy.ndarray:
                https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html

            .. _PIL.Image.Image:
                https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image

            Numpy array support
                - data type (( ) represents a valid value range):

                    - bool
                    - integer (0 ~ 255)
                    - unsigned integer (0 ~ 255)
                    - float (0.0 ~ 1.0)

                    .. warning::

                        - Out-of-range integer values will be **clipped** to [0, 255].
                        - Out-of-range float values will be **clipped** to [0, 1].

                - shape (H: height, W: width):

                    - H x W (Grayscale)
                    - H x W x 1 (Grayscale)
                    - H x W x 3 (an RGB channel order is assumed)
                    - H x W x 4 (an RGBA channel order is assumed)

        :param correlation_id: Correlation ID of the image.
        :param image: Image to log.
        :param designation: Designation of the image.
        """
        if image.designation is None:
            image.designation = self.gen_image_save_path(
                correlation_id, designation, image.metadata)
        self._image_logger.log(image)

    def _log_blob(self, correlation_id: str, blob: WindmillBlob, designation: str = ''):
        if blob.designation is None:
            blob.designation = self.gen_blob_save_path(
                correlation_id, designation, blob.metadata)
        self._blob_logger.log(blob)

    def gen_blob_save_path(self, correlation_id: str, designation: str = '', metadata=None) -> str:
        """
        generate blob save path
        :param correlation_id:
        :return:
        """
        time_tuple = time.localtime(int(time.time()))
        if len(designation) == 0:
            designation = DEFAULT_CAPTURE_INPUT_DESIGNATION
        dir_name = os.path.join(f"{self.blob_path}/{designation}",
                                time.strftime(TIME_DIRECTORY_FORMAT, time_tuple))
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        content_type = metadata.get("content_type", "application/octet-stream") \
            if metadata is not None else "application/octet-stream"
        ext = mimetypes.guess_extension(content_type)
        extension = ext if ext is not None else "bin"
        file_name = correlation_id
        if metadata.get('sub_name'):
            file_name = f"{file_name}_{metadata.get('sub_name')}"
        return f"{dir_name}/{file_name}{extension}"

    def close(self):
        self._logger.close()
        self._image_logger.close()
        self._blob_logger.close()

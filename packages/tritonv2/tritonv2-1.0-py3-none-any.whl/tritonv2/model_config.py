# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved

import os
from typing import Dict
from tritonclient.grpc import model_config_pb2
from google.protobuf import text_format, json_format


class ModelConfig:
    """
    ModelConfig For Triton Model
    """

    def __init__(self, model_config):
        self._model_config = model_config

    def is_ensemble(self) -> bool:
        """
        return if model is ensemble
        Returns:
            bool: _description_
        """
        return getattr(self._model_config, "platform") == "ensemble"

    def as_dict(self) -> Dict:
        """
        return model config as dict
        Returns:
            Dict: _description_
        """
        return json_format.MessageToDict(self._model_config)

    def get_ensemble_steps(self):
        """
        get ensemble steps
        """
        if not self.is_ensemble():
            raise ValueError("Model config is not an ensemble")

        model_config_dict = self.as_dict()
        if "ensembleScheduling" not in model_config_dict or \
                "step" not in model_config_dict["ensembleScheduling"] or \
                len(model_config_dict["ensembleScheduling"]["step"]) < 1:
            raise ValueError("Model ensembleScheduling is not valid")

        scheduling_step = {}
        try:
            for step in model_config_dict["ensembleScheduling"]["step"]:
                if step["modelVersion"] == "-1":
                    raise ValueError("Model version can not be -1")
                scheduling_step[step["modelName"]] = step["modelVersion"]
        except Exception as e:
            raise ValueError("Model ensembleScheduling is not valid")

        return scheduling_step

    def set_scheduling_model_version(self, model_name, model_version):
        """
        set scheduling model version
        """
        if not self.is_ensemble():
            raise ValueError("Model config is not an ensemble")

        model_config_dict = self.as_dict()
        try:
            for step in model_config_dict["ensembleScheduling"]["step"]:
                if step["modelName"] == model_name:
                    step["modelVersion"] = model_version
        except Exception as e:
            raise ValueError("Set model version failed {}".format(e))

        self._model_config = ModelConfig.create_from_dict(
            model_config_dict)._model_config

    def write_to_file(self, model_path, variant_model_source_version, bs):
        """
        write model config to file
        """
        model_config_path = os.path.join(model_path, "config.pbtxt")
        if not bs.exist(model_config_path):
            raise FileNotFoundError(
                "Model config path: {} not found".format(model_config_path))
        model_source_config_path = os.path.join(
            model_path, "{}/config.pbtxt".format(variant_model_source_version))
        try:
            bs.copy(model_config_path, model_source_config_path)
            model_config_bytes = text_format.MessageToBytes(self._model_config)
            bs.write_file(model_config_path, model_config_bytes)
        except Exception as e:
            raise ValueError("Model config write to file error:{}".format(e))

    @staticmethod
    def create_from_dict(model_config_dict):
        """
        create model config from dict
        """
        return ModelConfig(json_format.ParseDict(model_config_dict, model_config_pb2.ModelConfig()))

    @staticmethod
    def create_from_text(model_config_text):
        """
        create model config from text
        """
        return ModelConfig(text_format.Parse(model_config_text, model_config_pb2.ModelConfig()))

    @staticmethod
    def create_from_file(model_path, bs):
        """
        create model config from file
        """
        model_config_path = os.path.join(model_path, "config.pbtxt")
        if not bs.exist(model_config_path):
            raise FileNotFoundError(
                "Model config path: {} not found".format(model_config_path))
        raw_str = bs.read_file(model_config_path)
        return ModelConfig.create_from_text(raw_str)

# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
Model For Triton
"""
import os
import json
import base64
from typing import Any, Optional, List

from .module import CustomModule
from .client_factory import TritonClientFactory
from .constants import BENCHMARK_TASK, TESTING_TASK

try:
    from tritonclient.http import _get_inference_request
except ImportError:
    from tritonclient.http._utils import _get_inference_request


class Model(object):
    """
    Model Class
    Args:
        object (_type_): _description_
    """

    def __init__(self,
                 custom_module_class: Optional[CustomModule],
                 input_file_path: str,
                 server_url: str,
                 kind: str,
                 model_name: str = 'ensemble',
                 model_version: str = '1',
                 **kwargs) -> None:
        """
        Args:
            custom_module_class (Optional[CustomModule]): derived class of CustomModule
            input_file_path (str): input file path
            server_url (str): inference server url
            kind (str, optional): One of benchmark, testing
            model_name (str, optional): Defaults to 'ensemble'.
            model_version (str, optional): Defaults to '1'.
            output_file_path (str, optional): Defaults to './request.json'.
        """
        self.input_file_path = str(input_file_path)
        self.model_name = str(model_name)
        self.server_url = str(server_url)
        self.model_version = str(model_version)

        assert kind in [BENCHMARK_TASK,
                        TESTING_TASK], "kind must be one of benchmark or testing"
        self.kind = kind
        if self.kind == BENCHMARK_TASK:
            self.output_file_path = './request.json'
        elif self.kind == TESTING_TASK:
            self.output_file_path = './result/'
            if not os.path.exists(self.output_file_path):
                os.makedirs(self.output_file_path)

        self.client = TritonClientFactory.create_http_client(
            server_url=self.server_url)
        self.input_metadata, self.output_metadata, self.batch_size = self.client.get_inputs_and_outputs_detail(
            model_name=self.model_name, model_version=self.model_version)

        self.input_file_path_list = self.get_input_file_path_list()

        self.custom_module_instance = custom_module_class(
            input_metadata=self.input_metadata,
            output_metadata=self.output_metadata,
            **kwargs)

    def get_input_file_path_list(self) -> List[str]:
        """
        Scan input file path
        Returns:
            List[str]: path list
        """
        file_extensions = {'.jpeg', '.png', '.jpg'}
        file_paths = []

        if os.path.isdir(self.input_file_path):
            for root, _, files in os.walk(self.input_file_path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in file_extensions):
                        file_paths.append(os.path.join(root, file))
        elif os.path.isfile(self.input_file_path):
            _, ext = os.path.splitext(self.input_file_path)
            if ext.lower() in file_extensions:
                file_paths.append(self.input_file_path)
        else:
            return file_paths

        return file_paths

    def save_benchmark_request(self, model_inputs, model_outputs):
        """
        Save perf analysis input data json file
        Args:
            model_inputs (_type_): triton model inputs
            model_outputs (_type_): triton model outputs

        Returns:
            _type_: _description_
        """
        request_body_list = []
        for k, v in enumerate(model_inputs):
            request_body, json_size = _get_inference_request(inputs=v,
                                                             outputs=model_outputs[k],
                                                             request_id=str(k),
                                                             sequence_id=None,
                                                             sequence_start=None,
                                                             sequence_end=None,
                                                             priority=None,
                                                             timeout=None,
                                                             custom_parameters=None)
            if json_size is not None:
                return self._save_binary_benchmark_request(model_inputs)

            request_body_list.append(request_body)

        result = {'data': []}

        for k, body in enumerate(request_body_list):
            infer_req = json.loads(body)
            single_input = {}
            for i in range(len(infer_req['inputs'])):
                shape = infer_req['inputs'][i]['shape']
                if self.batch_size > 0:
                    shape.pop(0)
                single_input[infer_req['inputs'][i]['name']] = {
                    'shape': shape,
                    'content': infer_req['inputs'][i]['data']
                }

            result['data'].append(single_input)

        perf_req = json.dumps(result)
        with open(self.output_file_path, 'w') as f:
            f.write(perf_req)

    def save_testing_result(self, model_inputs, model_outputs):
        """
        Save inference result json file
        Args:
            model_inputs (_type_): _description_
            model_outputs (_type_): _description_
        """
        for k, model_input in enumerate(model_inputs):
            model_output = model_outputs[k]
            response = self.client.model_infer(
                model_name=self.model_name,
                model_version=self.model_version,
                inputs=model_input, outputs=model_output)
            response_str = self.custom_module_instance.postprocess(response)
            result_file_path = os.path.join(self.output_file_path, os.path.basename(
                self.input_file_path_list[k]) + '.json')
            with open(result_file_path, 'w') as f:
                f.write(response_str)

    def _save_binary_benchmark_request(self, model_inputs):
        """
        Save binary perf analysis input data json file
        Args:
            model_inputs (_type_): _description_
        """
        result = {'data': []}

        for k, v in enumerate(model_inputs):
            single_input = {}
            for i in v:
                shape = i.shape()
                if self.batch_size > 0:
                    shape.pop(0)
                single_input[i.name()] = {
                    'content': {'b64': base64.b64encode(i._get_binary_data()).decode('utf-8')},
                    'shape': shape,
                }
            result['data'].append(single_input)

        perf_req = json.dumps(result)
        with open(self.output_file_path, 'w') as f:
            f.write(perf_req)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        model_inputs = []
        model_outputs = []

        for input_path in self.input_file_path_list:
            model_input = self.custom_module_instance.prepare_input(input_path)
            model_inputs.append(model_input)
            model_output = self.custom_module_instance.prepare_output()
            model_outputs.append(model_output)

        if self.kind == BENCHMARK_TASK:
            self.save_benchmark_request(model_inputs, model_outputs)
        elif self.kind == TESTING_TASK:
            self.save_testing_result(model_inputs, model_outputs)

# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
"""
CustomModule For Triton
"""
from abc import ABCMeta, abstractmethod

class CustomModule(metaclass=ABCMeta):
    """_summary_

    Args:
        metaclass (_type_, optional): _description_. Defaults to ABCMeta.
    """
    def __init__(self, input_metadata, output_metadata, **kwargs):
        self.input_metadata = input_metadata
        self.output_metadata = output_metadata
    
    @abstractmethod
    def prepare_input(self, input_file_path):
        """
        Prepare input data for inference
        """
        pass
    
    @abstractmethod
    def prepare_output(self):
        """
        Prepare output data for inference
        """
        pass
    
    @abstractmethod
    def postprocess(self):
        """
        Postprocess output data to json str
        """
        pass
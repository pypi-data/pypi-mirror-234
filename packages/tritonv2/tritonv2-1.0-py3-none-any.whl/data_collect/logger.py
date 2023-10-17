# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
data collect support logger
"""
import json
import sys
import cv2
import spdlog
from typing import Dict
from concurrent import futures

from .utils import NpEncoder
from .data_types.image import Image as WindmillImage
from .data_types.blob import Blob as WindmillBlob


class Logger:
    """ Perform disk IO for images or blob or text in a background thread."""

    def __init__(self, config: Dict = {}):
        self._queue_size = config.get('queue_size', 4096) #参数不能设置的太大，会导致buffer存的数据量过大，无法刷到文件里
        from .queue import queue_manager
        queue_name = queue_manager.add_queue(name=self.__class__.__name__,
                                             maxsize=self._queue_size,
                                             create_new=True)
        self._queue = queue_manager.get_queue(queue_name)
        self._thread = None

    def _set_thread(self):
        """ Set the background thread for the load and save iterators and launch it. """
        if self._thread is not None and self._thread.is_alive():
            return
        from data_collect.thread import MultiThread
        self._thread = MultiThread(self._process,
                                   self._queue,
                                   name=self.__class__.__name__,
                                   thread_count=1)
        self._thread.start()

    def log(self, **kwargs):
        """ Log 

        Parameters
        ----------
        designation: str
            The symbol of the log record
        """
        raise NotImplementedError

    def _process(self, queue):
        """ IO process to be run in a thread. get data from queue and save to disk.

        Parameters
        ----------
        queue: queue.Queue()
        """
        raise NotImplementedError

    def close(self):
        """ Closes down and joins the internal threads 
        to ensure that all data is saved to disk.
        """
        if self._thread is not None:
            self._thread.join()
        del self._thread
        self._thread = None


class ImageLogger(Logger):
    """
    图片日志类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)

    def _save(self, image: WindmillImage):
        """
        保存图片
        :param designation:
        :param image:
        :return:
        """
        try:
            if image.is_bytes():
                with open(image.designation, "wb") as f:
                    f.write(image.data)
            else:
                if "PIL" in sys.modules and image.is_pillow_image():
                    image.covert_to_rgb()
                elif "numpy" in sys.modules and image.is_numpy_array():
                    image.covert_cv_image()
                cv2.imwrite(image.designation, image.data)
        except Exception as e:
            print(f"save image error: {e}")
        del image

    def _process(self, queue):
        """ Saves images from the save queue to the given params inside a thread.

        Parameters
        ----------
        queue: queue.Queue()
            The ImageIO Queue
        """
        executor = futures.ThreadPoolExecutor(thread_name_prefix=self.__class__.__name__)
        while True:
            item = queue.get()
            if item == "EOF":
                break
            executor.submit(self._save, *item)
        executor.shutdown()

    def log(self, image: WindmillImage):
        """
        put params to queue
        """
        self._set_thread()
        self._queue.put([image])

    def close(self):
        """ Signal to the Save Threads that they should be closed and cleanly shutdown
        the saver """
        self._queue.put("EOF")
        super().close()


class BlobLogger(Logger):
    """
    二进制文件类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)

    def _save(self, blob: WindmillBlob):
        try:
            with open(blob.designation, "wb") as f:
                f.write(blob.data)
        except Exception as e:
            print(f"save blob error: {e}")
        
        del blob
        
    def _process(self, queue):
        """ Saves blob from the save queue to the given params inside a thread.

        Parameters
        ----------
        queue: queue.Queue()
        """
        executor = futures.ThreadPoolExecutor(thread_name_prefix=self.__class__.__name__)
        while True:
            item = queue.get()
            if item == "EOF":
                break
            executor.submit(self._save, *item)
        executor.shutdown()

    def log(self, blob: WindmillBlob):
        """main save function

        Args:
            designation (str): _description_
            blob (WindmillBlob, optional): _description_. Defaults to None.
        """
        self._set_thread()
        self._queue.put([blob])

    def close(self):
        """ Signal to the Save Threads that they should be closed and cleanly shutdown
        the saver """
        self._queue.put("EOF")
        super().close()



class LineLogger(Logger):
    """
    文本日志类
    """

    def __init__(self, config: Dict = None):
        super().__init__(config)
        self._file_path = config.get('file_path')
        self._rotation = config.get('rotation')
        self._retention = config.get('retention')
        self._logger = self._spd_logger()

    def _spd_logger(self):
        """
        获取spdlog
        性能测试见:https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/pKzJfZczuc/I1E7bZqZ7Q/RxrbRhabyZlRhK
        """
        spdlog.set_async_mode(self._queue_size)
        # rotating_file_sink_mt 线程安全 rotating_file_sink_st 单线程模式
        sink = spdlog.rotating_file_sink_mt(
            self._file_path,
            self.rotation_to_bytes(),
            self._retention,
        )
        _logger = spdlog.SinkLogger(
            name="spd_log",  # placeholder
            sinks=[sink],
            async_mode=True,
        )
        _logger.set_level(spdlog.LogLevel.INFO)
        _logger.set_pattern("%v", spdlog.PatternTimeType.local)
        # 设置info的时候flush机制是生效的
        _logger.flush_on(spdlog.LogLevel.INFO)
        return _logger

    def rotation_to_bytes(self) -> int:
        """
        convert rotation
        :return:
        """
        if self._rotation.endswith('KB'):
            return int(self._rotation[:-2]) * 1024
        if self._rotation.endswith('MB'):
            return int(self._rotation[:-2]) * 1024 * 1024
        if self._rotation.endswith('GB'):
            return int(self._rotation[:-2]) * 1024 * 1024 * 1024
        return int(self._rotation)

    def log(self, message):
        """main save function

        Args:
            correlation_id (str): _description_
            message (_type_, optional): _description_. Defaults to None.
        """
        if isinstance(message, dict):
            message = json.dumps(message, cls=NpEncoder)
        self._logger.info(f"{message}")

    def _process(self, queue):
        """
        _process
        spdlog自带异步队列，不需要实现
        """
        pass
    
    def close(self):
        """
        close
        退出时调用drop_all，drop所有logger
        """
        spdlog.drop_all()
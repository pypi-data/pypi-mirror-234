# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
data collect useful queue
"""
import threading
from queue import Queue
from time import sleep
from typing import Dict


class EventQueue(Queue):
    """ Standard Queue object with a separate global shutdown parameter indicating that the main
    process, and by extension this queue, should be shut down.
    reference: https://github.com/deepfakes/faceswap/lib/queue_manager.py#L17
    remove the logger
    Parameters
    ----------
    shutdown_event: :class:`threading.Event`
        The global shutdown event common to all managed queues
    maxsize: int, Optional
        Upperbound limit on the number of items that can be placed in the queue. Default: `0`
    """
    def __init__(self, shutdown_event: threading.Event, maxsize: int = 0) -> None:
        super().__init__(maxsize=maxsize)
        self._shutdown = shutdown_event

    @property
    def shutdown(self) -> threading.Event:
        """ :class:`threading.Event`: The global shutdown event """
        return self._shutdown

class _QueueManager():
    """ Manage :class:`EventQueue` objects for availability across processes.
    reference:https://github.com/deepfakes/faceswap/lib/queue_manager.py#L38
    remove the logger
        Notes
        -----
        Don't import this class directly, instead import via :func:`queue_manager` """
    def __init__(self) -> None:
        """ Initialize the :class:`_QueueManager` """
        self.shutdown = threading.Event()
        self.queues: Dict[str, EventQueue] = {}

    def add_queue(self, name: str, maxsize: int = 0, create_new: bool = False) -> str:
        """ Add a :class:`EventQueue` to the manager.

        Parameters
        ----------
        name: str
            The name of the queue to create
        maxsize: int, optional
            The maximum queue size. Set to `0` for unlimited. Default: `0`
        create_new: bool, optional
            If a queue of the given name exists, and this value is ``False``, then an error is
            raised preventing the creation of duplicate queues. If this value is ``True`` and
            the given name exists then an integer is appended to the end of the queue name and
            incremented until the given name is unique. Default: ``False``

        Returns
        -------
        str
            The final generated name for the queue
        """
        if not create_new and name in self.queues:
            raise ValueError(f"Queue '{name}' already exists.")
        if create_new and name in self.queues:
            i = 0
            while name in self.queues:
                name = f"{name}{i}"

        self.queues[name] = EventQueue(self.shutdown, maxsize=maxsize)
        return name

    def del_queue(self, name: str) -> None:
        """ Remove a queue from the manager

        Parameters
        ----------
        name: str
            The name of the queue to be deleted. Must exist within the queue manager.
        """
        del self.queues[name]

    def get_queue(self, name: str, maxsize: int = 0) -> EventQueue:
        """ Return a :class:`EventQueue` from the manager. If it doesn't exist, create it.

        Parameters
        ----------
        name: str
            The name of the queue to obtain
        maxsize: int, Optional
            The maximum queue size. Set to `0` for unlimited. Only used if the requested queue
            does not already exist. Default: `0`
         """
        queue = self.queues.get(name)
        if not queue:
            self.add_queue(name, maxsize)
            queue = self.queues[name]
        return queue

    def terminate_queues(self) -> None:
        """ Terminates all managed queues.

        Sets the global shutdown event, clears and send EOF to all queues.  To be called if there
        is an error """
        self.shutdown.set()
        self._flush_queues()
        for q_name, queue in self.queues.items():
            queue.put("EOF")

    def _flush_queues(self):
        """ Empty out the contents of every managed queue. """
        for q_name in self.queues:
            self.flush_queue(q_name)

    def flush_queue(self, name: str) -> None:
        """ Flush the contents from a managed queue.

        Parameters
        ----------
        name: str
            The name of the managed :class:`EventQueue` to flush
        """
        queue = self.queues[name]
        while not queue.empty():
            queue.get(True, 1)

    def debug_monitor(self, update_interval: int = 2) -> None:
        """ A debug tool for monitoring managed :class:`EventQueues`.

        Prints queue sizes to the console for all managed queues.

        Parameters
        ----------
        update_interval: int, Optional
            The number of seconds between printing information to the console. Default: 2
        """
        thread = threading.Thread(target=self._debug_queue_sizes,
                                  args=(update_interval, ))
        thread.daemon = True
        thread.start()

    def _debug_queue_sizes(self, update_interval) -> None:
        """ Print the queue size for each managed queue to console.

        Parameters
        ----------
        update_interval: int
            The number of seconds between printing information to the console
        """
        while True:
            for name in sorted(self.queues.keys()):
                print(f"{name}: {self.queues[name].qsize()}")
            sleep(update_interval)

queue_manager = _QueueManager()
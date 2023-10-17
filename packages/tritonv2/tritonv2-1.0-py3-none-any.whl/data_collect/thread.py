# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
"""
data collect useful thread
"""
import sys
import threading
from types import TracebackType
from typing import Callable, Tuple, Dict, Any, Optional, Type, Union, List, Set

_ErrorType = Optional[Union[Tuple[Type[BaseException], BaseException, TracebackType],
Tuple[Any, Any, Any]]]

_THREAD_NAMES: Set[str] = set()


def _get_name(name: str) -> str:
    """ Obtain a unique name for a thread

    Parameters
    ----------
    name: str
        The requested name

    Returns
    -------
    str
        The request name with "_#" appended (# being an integer) making the name unique
    """
    idx = 0
    real_name = name
    while True:
        if real_name in _THREAD_NAMES:
            real_name = f"{name}_{idx}"
            idx += 1
            continue
        _THREAD_NAMES.add(real_name)
        return real_name


class FSThread(threading.Thread):
    """
    Subclass of thread that passes errors back to parent
    reference: https://github.com/deepfakes/faceswap/lib/multithreading.py#L48
    remove the logger
    Parameters
    ----------
    target: callable object, Optional
        The callable object to be invoked by the run() method. If ``None`` nothing is called.
        Default: ``None``
    name: str, optional
        The thread name. if ``None`` a unique name is constructed of the form "Thread-N" where N
        is a small decimal number. Default: ``None``
    args: tuple
        The argument tuple for the target invocation. Default: ().
    kwargs: dict
        keyword arguments for the target invocation. Default: {}.
    """
    _target: Callable
    _args: Tuple
    _kwargs: Dict[str, Any]
    _name: str

    def __init__(self,
                 target: Optional[Callable] = None,
                 name: Optional[str] = None,
                 args: Tuple = (),
                 kwargs: Optional[Dict[str, Any]] = None,
                 *,
                 daemon: Optional[bool] = None) -> None:
        super().__init__(target=target, name=name, args=args, kwargs=kwargs, daemon=daemon)
        self.err: _ErrorType = None

    def check_and_raise_error(self) -> None:
        """ Checks for errors in thread and raises them in caller.

        Raises
        ------
        Error
            Re-raised error from within the thread
        """
        if not self.err:
            return
        raise self.err[1].with_traceback(self.err[2])

    def run(self) -> None:
        """ Runs the target, raising any errors from within the thread in the caller. """
        try:
            if self._target is not None:
                self._target(*self._args, **self._kwargs)
        except Exception as err:  # pylint: disable=broad-except
            self.err = sys.exc_info()
        finally:
            # Avoid a recycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs


class MultiThread():
    """ Threading for IO heavy ops. Catches errors in thread and rethrows to parent.
    reference: https://github.com/deepfakes/faceswap/lib/multithreading.py#L106
    remove the logger
    Parameters
    ----------
    target: callable object
        The callable object to be invoked by the run() method.
    args: tuple
        The argument tuple for the target invocation. Default: ().
    thread_count: int, optional
        The number of threads to use. Default: 1
    name: str, optional
        The thread name. if ``None`` a unique name is constructed of the form {target.__name__}_N
        where N is an incrementing integer. Default: ``None``
    kwargs: dict
        keyword arguments for the target invocation. Default: {}.
    """

    def __init__(self,
                 target: Callable,
                 *args,
                 thread_count: int = 1,
                 name: Optional[str] = None,
                 **kwargs) -> None:
        self._name = _get_name(name if name else target.__name__)
        self.daemon = True
        self._thread_count = thread_count
        self._threads: List[FSThread] = []
        self._target = target
        self._args = args
        self._kwargs = kwargs

    @property
    def has_error(self) -> bool:
        """ bool: ``True`` if a thread has errored, otherwise ``False`` """
        return any(thread.err for thread in self._threads)

    @property
    def errors(self) -> List[_ErrorType]:
        """ list: List of thread error values """
        return [thread.err for thread in self._threads if thread.err]

    @property
    def name(self) -> str:
        """ :str: The name of the thread """
        return self._name

    def check_and_raise_error(self) -> None:
        """ Checks for errors in thread and raises them in caller.

        Raises
        ------
        Error
            Re-raised error from within the thread
        """
        if not self.has_error:
            return
        error = self.errors[0]
        assert error is not None
        raise error[1].with_traceback(error[2])

    def is_alive(self) -> bool:
        """ Check if any threads are still alive

        Returns
        -------
        bool
            ``True`` if any threads are alive. ``False`` if no threads are alive
        """
        return any(thread.is_alive() for thread in self._threads)

    def start(self) -> None:
        """ Start all the threads for the given method, args and kwargs """
        for idx in range(self._thread_count):
            name = self._name if self._thread_count == 1 else f"{self._name}_{idx}"
            thread = FSThread(name=name,
                              target=self._target,
                              args=self._args,
                              kwargs=self._kwargs)
            thread.daemon = self.daemon
            thread.start()
            self._threads.append(thread)

    def completed(self) -> bool:
        """ Check if all threads have completed

        Returns
        -------
        ``True`` if all threads have completed otherwise ``False``
        """
        ret_val = all(not thread.is_alive() for thread in self._threads)
        return ret_val

    def join(self) -> None:
        """ Join the running threads, catching and re-raising any errors

        Clear the list of threads for class instance re-use
        """
        for thread in self._threads:
            thread.join()
            if thread.err:
                raise thread.err[1].with_traceback(thread.err[2])
        del self._threads
        self._threads = []

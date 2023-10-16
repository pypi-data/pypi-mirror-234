# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "20/04/2020"


import os
from flufl.lock import Lock

from tomwer.core.utils.Singleton import singleton

_FILE_LOCKERS = {}


def get_lock_file_path(process_file_path):
    process_file_path = os.path.abspath(process_file_path)
    parts = process_file_path.split(os.sep)
    if len(parts) == 0:
        # file without any name ???!!!
        raise RuntimeError
    elif len(parts) == 1:
        file_path = ""
    else:
        file_path = os.path.join(*parts[:-1])
    lock_name = "." + parts[-1] + ".flufllock"
    return os.path.join(file_path, lock_name)


@singleton
class FileLockerManager:
    """Insure that for each file we will provide at most one locker"""

    def __init__(self):
        self.__lockers = {}

    def clear_locker(self, file_):
        if file_ in self.__lockers:
            del self.__lockers[file_]

    @staticmethod
    def get_lock(file_name):
        def get_lock_file_path(file_path):
            file_path = os.path.abspath(file_path)
            parts = file_path.split(os.sep)
            if len(parts) == 0:
                # file without any name ???!!!
                raise RuntimeError
            elif len(parts) == 1:
                file_path = ""
            else:
                file_path = os.sep.join(parts[:-1])
            lock_name = "." + parts[-1] + ".flufllock"
            return os.path.join(file_path, lock_name)

        lock_file_path = get_lock_file_path(file_name)
        # if not os.path.exists(lock_file_path):
        #     from pathlib import Path
        #     Path(lock_file_path).touch()
        if lock_file_path not in _FILE_LOCKERS:
            _FILE_LOCKERS[lock_file_path] = Lock(lock_file_path, default_timeout=3)
        return _FILE_LOCKERS[lock_file_path]

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# multitasking: Non-blocking Python methods using decorators
# https://github.com/ranaroussi/multitasking
#
# Copyright 2016-2018 Ran Aroussi
#
# Licensed under the GNU Lesser General Public License, v3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/lgpl-3.0.en.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__version__ = "0.0.7a"

from sys import exit as sysexit
from os import _exit as osexit

from threading import Thread, Semaphore
from multiprocessing import Process, cpu_count

config = {
    "CPU_CORES": cpu_count(),
    "ENGINE": "thread",
    "MAX_THREADS": cpu_count(),
    "KILL_RECEIVED": False,
    "TASKS": [],
    "POOLS": {},
    "POOL_NAME": "Main"
}


def set_max_threads(threads=None):
    if threads is not None:
        config["MAX_THREADS"] = threads
    else:
        config["MAX_THREADS"] = cpu_count()


def set_engine(kind=""):
    if "process" in kind.lower():
        config["ENGINE"] = "process"
    else:
        config["ENGINE"] = "thread"


def getPool(name=None):
    if name is None:
        name = config["POOL_NAME"]

    engine = "thread"
    if config["POOLS"][config["POOL_NAME"]]["engine"] == Thread:
        engine = "process"

    return {
        "engine": engine,
        "name": name,
        "threads": config["POOLS"][config["POOL_NAME"]]["threads"]
    }


def createPool(name="main", threads=None, engine=None):

    config["POOL_NAME"] = name

    try:
        threads = int(threads)
    except:
        threads = config["MAX_THREADS"]
    if threads < 2:
        threads = 0

    engine = engine if engine is not None else "thread"

    config["MAX_THREADS"] = threads
    config["ENGINE"] = engine

    config["POOLS"][config["POOL_NAME"]] = {
        "pool": Semaphore(threads) if threads > 0 else None,
        "engine": Process if "process" in engine.lower() else Thread,
        "name": name,
        "threads": threads
    }


def task(callee):

    # create default pool if nont exists
    if not config["POOLS"]:
        createPool()

    def _run_via_pool(*args, **kwargs):
        with config["POOLS"][config["POOL_NAME"]]['pool']:
            return callee(*args, **kwargs)

    def async_method(*args, **kwargs):
        # no threads
        if config["POOLS"][config["POOL_NAME"]]['threads'] == 0:
            return callee(*args, **kwargs)

        # has threads
        if not config["KILL_RECEIVED"]:
            try:
                single = config["POOLS"][config["POOL_NAME"]]['engine'](
                    target=_run_via_pool, args=args, kwargs=kwargs, daemon=False)
            except:
                single = config["POOLS"][config["POOL_NAME"]]['engine'](
                    target=_run_via_pool, args=args, kwargs=kwargs)
            config["TASKS"].append(single)
            single.start()
            return single

    return async_method


def wait_for_tasks():
    config["KILL_RECEIVED"] = True

    if config["POOLS"][config["POOL_NAME"]]['threads'] == 0:
        return True

    try:
        running = len([t.join(1)
                       for t in config["TASKS"] if t is not None and t.isAlive()])
        while running > 0:
            running = len([t.join(1)
                           for t in config["TASKS"] if t is not None and t.isAlive()])
    except:
        pass
    return True


def killall():
    config["KILL_RECEIVED"] = True

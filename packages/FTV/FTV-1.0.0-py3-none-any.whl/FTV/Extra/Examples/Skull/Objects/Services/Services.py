from __future__ import annotations

import multiprocessing as mp
import os
import threading
import time
from typing import TYPE_CHECKING

from PyQt5.QtCore import QTimer

if TYPE_CHECKING:
    from multiprocessing.queues import Queue


class PeriodicTimer:
    def __init__(self, period, target, *args, **kwargs):
        super().__init__()
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.period = period
        self.i = 0
        self.t0 = time.time()
        self.print = None

    def sleep(self):
        self.i += 1
        end_time = self.t0 + self.period * self.i
        delta = end_time - time.time()

        if delta > 0:
            time.sleep(delta)

    def run(self):
        # frequencies = []
        # n = 20
        self.frequency = None

        while True:
            # start_time = time.time()
            res = self.target(*self.args, **self.kwargs)

            if res is False:
                break

            self.sleep()
            # end_time = time.time_ns()

            # if end_time - start_time != 0:
            #     frequencies.append(10**9/(end_time - start_time))
            #
            # if len(frequencies) == n:
            #     self.frequency = (round(sum(frequencies)/n, 1))
            #     self.print(f"{self.frequency} [Hz]")
            #     frequencies = []

    def setPrint(self, _print):
        self.print = _print

    def start(self):
        self.run()


class Service:
    def __init__(self):
        self.name = self.__class__.__name__
        if self.name.endswith("Service"):
            self.name = self.name.removesuffix("Service")

        self.executor: mp.Process = None
        self.daemon = False
        self.del_t = 0  # default
        self.timer: QTimer = None
        self.is_thread = False

        # TODO lahav rename below block to avoid dependency between services
        self.sensors_shared: mp.Queue = None

        # TODO lahav rename below block to avoid dependency between services
        self.sensors_lock: threading.Lock = None

    def _run(self, shared_1):
        self.print(f"Service is running [{os.getpid()}]")

        self.sensors_shared, self.sensors_lock = shared_1

        self.setup()
        self._startLoop()

        self.print(f"Service finished")

    @staticmethod
    def sleep(duration, get_now=time.perf_counter):
        now = get_now()
        end = now + duration
        while now < end:
            now = get_now()

    def getFrequency(self):
        return self.timer.frequency

    def setAsThread(self):
        self.is_thread = True

    def setAsProcess(self):
        self.is_thread = False

    def isThread(self):
        return self.is_thread

    def isProcess(self):
        return not self.is_thread

    def _timer_loop(self):
        res = self.loop()
        if res is False:
            self.print("stopping timer")
            self.timer.stop()

    def _startLoop(self):
        if self.del_t != 0:
            self.timer = PeriodicTimer(self.del_t, self.loop)
            self.timer.setPrint(self.print)
            self.timer.start()

        else:
            while True:
                res = self.loop()

                if res is False:
                    break

                if self.del_t != 0:
                    time.sleep(self.del_t)

    def setup(self):
        pass

    def loop(self):
        pass

    def start(self, *args):
        if self.is_thread:
            Executor = threading.Thread
        else:
            Executor = mp.Process

        self.executor = Executor(target=self._run, args=args, name=self.name, daemon=self.daemon)
        self.executor.start()

    def join(self):
        self.executor.join()

    def print(self, *args, **kwargs):
        args = tuple([f"\033[0;32m{self.name}:\033[0m"] + list(args))
        # print(*args, **kwargs)

    def setDel_t(self, del_t):
        self.del_t = del_t

    def setDaemon(self, daemon):
        self.daemon = daemon


class ServicesManager:
    def __init__(self, *services):
        services = list(services)
        self.main_service = services.pop(0)
        self.services = services
        self.processes = []
        self.shared_count = 1

        mpManager = mp.Manager()
        self.shared_list = [(mp.Queue(), mpManager.Lock()) for _ in range(self.shared_count)]
        self.shared_list = [
            (mp.Queue(), mpManager.Lock())
            # (mpManager.list(), mpManager.Lock())
        ]

    def start(self):
        print()
        mp.freeze_support()

        for service in self.services:
            service.start(*self.shared_list)
            time.sleep(service.del_t / (len(self.services) + 1))

        self.main_service.start(*self.shared_list)

        for services in self.services:
            services.join()

    def addServices(self, *services):
        self.services += list(services)


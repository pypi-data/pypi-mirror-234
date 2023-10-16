from __future__ import annotations

from sys import exit

import asyncio
import json
import os
from pathlib import Path
from signal import Signals, signal, SIGINT, SIGTERM
from typing import List, Generic, Any, Coroutine, Type, cast

import loguru

from web import settings
from web.kernel.messaging.dispatcher import IDispatcher
from web.kernel.proc.manager import ProcManager
from web.kernel.transport import Transport, TransportIsolate
from web.kernel.types import ConfAble, GenConfig, AppNameAble, Environment, EnvAble, cheat, ISocket, SigAble, \
    IScheduler, ChanAble, SocketConf, TaskEvent, SharedState, SignalType, call_signals


class WebApp(Generic[GenConfig], ConfAble[GenConfig], SigAble, ChanAble):
    """
    Main application class.
    """
    _transports: List[Transport]
    name: str
    _environment: Environment
    manager: ProcManager
    scheduler: IScheduler | None
    dispatcher: IDispatcher
    shared_state: SharedState | None

    def __init__(self, name: str,
                 config: GenConfig,
                 transports: List[Transport],
                 environment: Environment):
        self.scheduler = None
        self.shared_state = None
        self._environment = environment
        self._transports = transports
        self.manager = ProcManager()
        self.dispatcher = IDispatcher()
        cheat(self.manager, EnvAble, self._environment, nested=False)
        self.channel = self.dispatcher.set_channel(self, ext_name="MasterChannel", master=True)
        self.name = name
        self.conf = config

    def with_scheduler(self, scheduler: IScheduler = None) -> WebApp:
        """
        add background task scheduler to app.
        """
        if settings.SCHEDULER_ENABLE:
            if not self.shared_state:
                self.shared_state = SharedState(self.channel)
            from web.kernel.proc.scheduler import Scheduler
            self.scheduler = Scheduler() if not scheduler else scheduler
            if not self.scheduler.manager:
                self.scheduler.manager = self.manager
            if not self.scheduler.dispatcher:
                self.scheduler.dispatcher = self.dispatcher
            return self
        else:
            raise RuntimeError("apscheduler is not installed on your system. scheduler not enable")

    def with_shared_state(self) -> WebApp:
        """
        add shared state to app.
        :return:
        """
        self.shared_state = SharedState(self.channel)
        return self

    def _create_transport_isolates(self, workers: int | None = None) -> List[TransportIsolate]:
        isolates = []

        usual_transports = [t for t in self._transports if not t.ignore_balance and t.workers < 1]

        for transport in self._transports:
            if transport.workers < 1 and not transport.ignore_balance:
                transport.workers = 1
            elif transport.ignore_balance and transport.workers < 1:
                if workers:
                    transport.workers = workers
                else:
                    transport.workers = 1

        if workers:
            if (transports := sum(list(t.workers for t in self._transports if not t.ignore_balance))) > workers:
                raise Exception(f"Too many transports ({transports}) for this cpu ({workers})")
        else:
            workers = sum(t.workers for t in self._transports if not t.ignore_balance)

        if workers > (sum_workers := sum(t.workers for t in self._transports if not t.ignore_balance)):
            priority_sum = sum([t.priority for t in usual_transports])
            ost_workers = workers - sum_workers
            if priority_sum:
                for transport in self._transports:
                    w = round(ost_workers * (transport.priority / priority_sum))
                    transport.workers += w
            else:
                from itertools import cycle
                t_c = cycle(usual_transports)
                while ost_workers > 0:
                    t = next(t_c)
                    t.workers += 1
                    ost_workers -= 1

        count = 0
        for transport in self._transports:
            conf = cast(SocketConf, transport.conf.socket)
            sock = ISocket(conf.host, conf.port)
            for _ in range(transport.workers):
                isolate = TransportIsolate(f"{self.name}::{transport.__class__.__name__}-{count}",
                                           transport, sock)
                self.dispatcher.set_channel(isolate)
                isolates.append(isolate)
                count += 1

        self._worker_num = len(isolates)
        return isolates

    async def run(self, multiprocessing: bool = False,
                  fast: bool = False,
                  ) -> None:
        """
        Run app.
        :param multiprocessing: if True, run every transport in separate processes; else run all in one process.
        :param fast:
        :return:
        """
        if not multiprocessing and fast:
            raise Exception("multiprocessing must be True if fast is True")

        cheat(self, AppNameAble, self.name)
        tasks: list[Coroutine[Any, Any, Any]] = []

        cheat(self, EnvAble, self._environment)

        cheat(self, ConfAble, self.conf)

        await self._environment.init()
        await call_signals(self, SignalType.BEFORE_APP_RUN, app=self)
        await self._environment.shutdown()

        if multiprocessing:
            self.manager.add_isolate_list(self._create_transport_isolates(workers=os.cpu_count() if fast else None))
            # tasks.extend(self.manager.perform())
        else:  # TODO fix (hz chto)
            for transport in self._transports:
                socket = ISocket(transport.conf.socket.host, transport.conf.socket.port)
                tasks.extend(transport.perform(socket))
        await self.manager.run()

        if self.scheduler:
            self.channel.add_event_listener(TaskEvent.message_type, self.scheduler.add_task)
            # tasks.extend(self.scheduler.perform())
            await self.scheduler.run()

        tasks.extend(self.dispatcher.perform())
        tasks.append(self.channel.listen_consume())

        async def sig_handler():
            loguru.logger.info(
                f"{self.name} Received shutdown signal , exit")
            await call_signals(self, SignalType.AFTER_APP_STOP, app=self)
            if self.scheduler:
                self.scheduler.stop()
            self.manager.stop()
            exit(0)

        loop = asyncio.get_event_loop()
        loop.add_signal_handler(SIGINT, lambda: asyncio.create_task(sig_handler()))
        loop.add_signal_handler(SIGTERM, lambda: asyncio.create_task(sig_handler()))

        await self._environment.init()
        await asyncio.wait(tasks)
        await self._environment.shutdown()


#
# async def __return_metrics(self, event: MetricRequestEvent):
#     event = await self._metrics_store.on_metric_request(event)
#     await self._dispatcher.send_to_consume(event.sender, event)

def load_config(conf_path: Path, config_model: Type[GenConfig]) -> GenConfig:
    """
    Load environment config to user in
    :param conf_path:
    :param config_model: BaseModel to cast json file to pydantic
    :return: None
    """
    with open(conf_path, "r") as _json_file:
        conf = config_model(**json.loads(_json_file.read()))
        return conf

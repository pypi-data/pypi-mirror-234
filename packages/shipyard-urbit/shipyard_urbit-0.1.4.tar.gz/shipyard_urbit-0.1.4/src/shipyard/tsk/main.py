from functools import wraps
from multiprocessing import current_process
from multiprocessing.connection import Client, Listener
from aioprocessing.connection import AioClient
from aiohttp import web
import threading
import logging
import time
from shipyard.models import Task, TaskLog
from .app import app

async def aiohttp_run():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8080)
    await site.start()
    # wait for finish signal
    await runner.cleanup()


class TaskRunner(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name="TaskRunner")
        self.stop_event = threading.Event()
        self.logger = logging.getLogger(
            f"{self.__class__.__module__}.{self.__class__.__qualname__}"
        )

    def stop(self):
        self.stop_event.set()
        # One more task to break the listener loop
        TaskRunner.run_task(NullTask())

    def is_stopped(self):
        return self.stop_event.is_set()

    def __enter__(self):
        self.logger.info("Initializing")
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.logger.info("Completing tasks...")
        self.join()
        self.logger.info("Terminated")

    def run(self):
        with Listener(("127.0.0.1", 57778)) as listener:
            while not self.is_stopped():
                conn = listener.accept()
                thr = threading.Thread(target=self.handle_connection, args=[conn])
                thr.start()

    def handle_connection(self, conn):
        task = conn.recv()
        if isinstance(task, Task):
            result = self.execute_task(task)
            conn.send(result)
        else:
            conn.send(Exception("uh"))
        conn.close()

    def execute_task(self, task: Task):
        if task.loggable:
            log = TaskLog.fromTask(task)
            self.logger.info(log)
        return task.run()

    @classmethod
    def run_task(cls, task: Task):
        with Client(("127.0.0.1", 57778)) as conn:
            conn.send(task)

    @classmethod
    def run_task_sync(cls, task: Task):
        with Client(("127.0.0.1", 57778)) as conn:
            conn.send(task)
            r = conn.recv()
            return r

    @classmethod
    async def run_task_async(cls, task: Task):
        with AioClient(("127.0.0.1", 57778)) as conn:
            await conn.coro_send(task)
            return await conn.coro_recv()

    @classmethod
    def async_task_client(cls):
        return AioClient(("127.0.0.1", 57778))

    @classmethod
    def sync_task_client(cls):
        return Client(("127.0.0.1", 57778))


def with_task_runner(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with TaskRunner():
            f(*args, **kwargs)

    return wrapper


class NullTask(Task):
    version = 1
    loggable = False

    def run(self):
        pass


class ProcessIdPrintingTask(Task):
    version = 1

    def run(self):
        self.logger.info(f"Taskin {self.version}: {current_process().pid}")
        return f"Taskin {self.version}: {current_process().pid}"


class ThreadInfoTask(Task):
    version = 1

    def run(self):
        for t in threading.enumerate():
            self.logger.info(t.getName())


class LongSleeperTask(Task):
    version = 1

    def run(self):
        for i in range(1, 10):
            self.logger.info(f"Sleepin' {i}")
            time.sleep(1)


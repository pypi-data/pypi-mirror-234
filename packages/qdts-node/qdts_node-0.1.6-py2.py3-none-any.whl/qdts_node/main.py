import logging
import sys
import os
from datetime import datetime

import asyncio
import qdts_node.backend as backend
import qdts_node.key_synchronization as key_synchronization
import qdts_node.configuration as configuration
import qdts_node.database as database
import qdts_node.key_management as key_management
import signal

import time
import aioconsole
from logging.handlers import QueueListener
from logging import FileHandler, StreamHandler
import queue
from logging.handlers import QueueHandler

CONFIG_FILE = os.path.join(os.getcwd(), "config.json")

logger = None
main_daemon = None


def init():
    # https://stackoverflow.com/questions/45842926/python-asynchronous-logging

    global logger

    log_queue = queue.Queue()
    queue_handler = QueueHandler(log_queue)

    logger = logging.getLogger("qdts_node")

    logger.setLevel(logging.DEBUG)
    log_file_name = "qdts_log" + str(int(time.time())) + ".log"
    file_handler_path = os.path.join(os.getcwd(), log_file_name)
    file_handler = FileHandler(file_handler_path)
    formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
    stream_handler = StreamHandler()
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    queue_listener = QueueListener(log_queue, stream_handler, file_handler)
    queue_listener.start()
    root = logging.getLogger()
    root.addHandler(queue_handler)


class MainLoop:

    def __init__(self):
        self.key_manager = None
        self.key_synchronizator = None
        self.backend = None
        self.database = None

    async def start(self, config):
        init()

        backend.init()
        database.init()
        key_management.init()
        key_synchronization.init()

        logger.info("Initializing database")
        self.database = database.Database(config)

        logger.info("Starting the backend")
        self.backend = backend.QBackend(config)
        self.backend.start()

        logger.info("Starting the key synchronizator")
        self.key_synchronizator = key_synchronization.KeySynchronizationSubsystem(
            config, self.database, self.backend)

        neighbour_node_names = [name for (name, _, _) in config.neighbours]
        waiter_for_nodes = list(filter(lambda x: x < config.node_name, neighbour_node_names))
        self.key_synchronizator.start(waiter_for_nodes)

        logger.info("Starting the application interface")
        self.key_manager = key_management.KeyManagementSubsystem(config, self.database, self.key_synchronizator)
        await self.key_manager.start()

    async def stop(self):
        logger.info("Stopping key manager")
        await self.key_manager.stop()

        logger.info("Stopping key synchronizator")
        self.key_synchronizator.stop()

        logger.info("Stopping quantum backend")
        self.backend.stop()


def start(pidfile, config_file):
    # We load the configuration from this script rather than from the daemon.
    config = configuration.Config(config_file)
    main_loop = MainLoop()
    main_loop.start_as_daemon(pidfile, config)


def restart(pidfile):
    main_daemon = MainLoop()
    main_daemon.restart_as_daemon(pidfile)


def stop(pidfile):
    main_daemon = MainLoop()
    main_daemon.stop_as_daemon(pidfile)


def non_daemon_start(config_file):
    config = configuration.Config(config_file)
    global main_daemon
    main_daemon = MainLoop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_daemon.start(config))


def sig_handler(s,f):
    print("Tiesa")
    loop = asyncio.get_event_loop()
    if main_daemon is not None:
        loop.run_until_complete(main_daemon.stop())


def cli():
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    non_daemon_start(CONFIG_FILE)


if __name__ == "__main__":
    cli()

"""
This module handles system level operations for Sieve.

This includes handling SIGTERM and handling run synchronization.
"""

import signal
import time
import sys
import os
import threading
import traceback
from ..logging.logging import get_sieve_internal_logger

logger = get_sieve_internal_logger()

SIGTERMING = False
main_server = None
health_server = None

run_lock = threading.Lock()

from contextlib import contextmanager


@contextmanager
def get_run_lock_timeout(timeout):
    result = run_lock.acquire(timeout=timeout)
    try:
        yield result
    finally:
        if result:
            run_lock.release()


def default_sigterm_handler(signum, frame):
    """Default sigterm handler for init handling"""

    traceback.print_stack()

    logger.info("shutting down...")
    if main_server is not None:
        logger.info("stopping main server")
    if health_server is not None:
        logger.info("stopping health server")
    global SIGTERMING
    SIGTERMING = True
    # Check if grpc connections are still active
    if signum is "KILL":
        logger.info("Received GRPC request to terminate self, exiting")
        if main_server:
            main_server.stop(1)
            logger.info("stopped main server")
            main_server.wait_for_termination()
            logger.info("main server terminated")
        if health_server:
            health_server.stop(1)
            logger.info("stopped health server")
            health_server.wait_for_termination()
            logger.info("health server terminated")
    else:
        with get_run_lock_timeout(3600 * 24):
            if main_server:
                main_server.stop(3600 * 24)
                logger.info("stopped main server")
                main_server.wait_for_termination()
                logger.info("main server terminated")
        if health_server:
            health_server.stop(60)
            logger.info("stopped health server")
            health_server.wait_for_termination()
            logger.info("health server terminated")
    logger.info("Exiting")
    os._exit(0)


def is_sigterming():
    return SIGTERMING


signal.signal(signal.SIGTERM, default_sigterm_handler)

from __future__ import annotations

import os
import threading
from typing import TYPE_CHECKING

import msgpack
import requests
from bec_lib.core import MessageEndpoints, RedisConnector, bec_logger
from dotenv import dotenv_values

logger = bec_logger.logger

if TYPE_CHECKING:
    from scihub import SciHub


class SciLogConnector:
    token_expiration_time = 86400  # one day

    def __init__(self, scihub: SciHub, connector: RedisConnector) -> None:
        self.scihub = scihub
        self.connector = connector
        self.producer = self.connector.producer()
        self.host = None
        self.user = None
        self.user_secret = None
        self._configured = False
        self._scilog_thread = None
        self._load_environment()
        self._start_scilog_update()

    def get_token(self) -> str:
        """get a new scilog token"""
        response = requests.post(
            f"{self.host}/users/login", json={"principal": self.user, "password": self.user_secret}
        )
        if response.ok:
            return response.json()["token"]
        return None

    def set_bec_token(self, token: str) -> None:
        """set the scilog token in redis"""
        self.producer.set(
            MessageEndpoints.logbook(),
            msgpack.dumps({"url": self.host, "user": self.user, "token": f"Bearer {token}"}),
        )

    def _start_scilog_update(self) -> None:
        if not self._configured:
            logger.warning("No environment file found. Cannot connect to SciLog.")
            return
        self._scilog_update()
        self._scilog_thread = RepeatedTimer(self.token_expiration_time, self._scilog_update)

    def _scilog_update(self):
        logger.info("Updating SciLog token.")
        token = self.get_token()
        if token:
            self.set_bec_token(token)

    def _load_environment(self):
        env_base = self.scihub.config.service_config.get("scilog", {}).get("env_file")
        if not env_base:
            return
        env_file = os.path.join(env_base, ".env")
        config = dotenv_values(env_file)
        self._update_config(**config)

    def _update_config(
        self,
        SCILOG_DEFAULT_HOST: str = None,
        SCILOG_USER: str = None,
        SCILOG_USER_SECRET: str = None,
    ) -> None:
        self.host = SCILOG_DEFAULT_HOST
        self.user = SCILOG_USER
        self.user_secret = SCILOG_USER_SECRET

        if self.host and self.user and self.user_secret:
            self._configured = True

    def shutdown(self):
        if self._scilog_thread:
            self._scilog_thread.stop()


class RepeatedTimer:
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        """start the timer"""
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """stop the timer"""
        self._timer.cancel()
        self.is_running = False

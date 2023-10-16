import json
import logging
import os
from contextvars import ContextVar
from typing import Any, Dict, Optional
from uuid import uuid4

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

# Keeps track of variables in the Thread/Task, across different modules.
_binded_vars: ContextVar = ContextVar("Binded vars in this context")


class LoggingManager:
    def __init__(
        self,
        name: str = __name__,
        logger_id: Optional[str] = None,
        gcp_env_variable: str = "GCP_SERVICE_KEY",
    ):
        """
        Args:
            name (str): Name of the logger. Defaults to __name__.
            logger_id (str, optional): id of the logger.
            gcp_env_variable (str): Name of the Google Service Key environment
                variable. The envionrment variable can hold a file path
                or a json.
        """
        if logger_id:
            self._set_logger_id(logger_id)

        self._gcp_client = None
        try:
            if gcp_env_variable in os.environ:
                # Local testing
                self._gcp_client = (
                    google.cloud.logging.Client.from_service_account_json(
                        os.environ[gcp_env_variable]
                    )
                )
            else:
                self._gcp_client = google.cloud.logging.Client()
        except Exception:
            # What this means is that  there is no GCP logging.
            # The most likely reason for this is local development
            # where there is not a Google Service Key.
            pass

        self._logger = logging.getLogger(name)
        self._logger.handlers.clear()
        self._logger.setLevel(logging.DEBUG)

        if self._gcp_client:
            cloudlogging_formatter = logging.Formatter("%(name)s: %(message)s")
            cloud_handler = CloudLoggingHandler(self._gcp_client)
            cloud_handler.setFormatter(cloudlogging_formatter)
            self._logger.addHandler(cloud_handler)

        stream_handler = logging.StreamHandler()
        streamlog_format = "%(_color)s %(asctime)s [%(levelname)s] - %(name)s: %(message)s - JSON Payload: %(json_fields)s \033[0;0m"  # noqa
        streamlog_formatter = logging.Formatter(fmt=streamlog_format)
        stream_handler.setFormatter(streamlog_formatter)
        self._logger.addHandler(stream_handler)

    @property
    def logger_id(self) -> str:
        if "request_id" not in self.binded:
            self._set_logger_id(uuid4().hex)
        return self.binded.get("request_id", "None")

    def _set_logger_id(self, logger_id: str) -> None:
        self.bind(request_id=logger_id)

    @property
    def binded(self) -> Dict[str, Any]:
        try:
            return _binded_vars.get()
        except LookupError:
            _binded_vars.set({})
            return _binded_vars.get()

    def bind(
        self, _payload: Optional[Dict[str, Any]] = None, **kwargs
    ) -> None:
        "Payload is a hack to bind to threads."
        if _payload and not isinstance(_payload, Dict):
            # TODO(luis): Revisit this logic
            self.warning("_payload must be of type Dict. Skipping the bind")
            _payload = {}
        _binded_vars.set((_payload or {}) | kwargs | self.binded)

    def _preprocess_json_payload(
        self,
        msg: str,
        payload: Optional[Dict[str, Any]],
        kwargs: Optional[Dict[str, Any]],
    ) -> Optional[dict]:
        if not payload:
            payload = {}
        if kwargs:
            payload = payload | kwargs
        payload = payload | self.binded

        payload["_message"] = msg
        payload["request_id"] = self.logger_id
        return payload

    def log(
        self,
        msg: str,
        level: int,
        json_params: Optional[Dict[str, Any]],
        skip_if_local: bool,
        color: str = "\033[0;0m",
        **kwargs,
    ) -> None:
        if skip_if_local and not self._gcp_client:
            return

        json_params = self._preprocess_json_payload(msg, json_params, kwargs)
        if self._gcp_client:
            try:
                self._logger.log(
                    level,
                    msg,
                    extra={"json_fields": json_params, "_color": color},
                )
            except Exception as e:
                self._logger.warning(
                    f"Error serializing JSON log: {e}",
                    extra={
                        "json_fields": {"request_id": self.logger_id},
                        "_color": "\033[0;33m",
                    },
                )
        else:
            try:
                self._logger.log(
                    level,
                    msg,
                    extra={
                        "json_fields": json.dumps(json_params, indent=2),
                        "_color": color,
                    },
                )
            except TypeError as e:
                # TODO(luis): Find a better way to pass color.
                self._logger.warning(
                    f"Error serializing JSON log: {e}",
                    extra={
                        "json_fields": {"request_id": self.logger_id},
                        "_color": "\033[0;33m",
                    },
                )
                self._logger.log(
                    level,
                    msg,
                    extra={"json_fields": json_params, "_color": color},
                )

    def debug(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.DEBUG,
            json_params=json_params,
            skip_if_local=skip_if_local,
            color="\033[0;32m",
            **kwargs,
        )

    def info(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.INFO,
            json_params=json_params,
            skip_if_local=skip_if_local,
            color="\033[0;0m",
            **kwargs,
        )

    def warning(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.WARNING,
            json_params=json_params,
            skip_if_local=skip_if_local,
            color="\033[0;33m",
            **kwargs,
        )

    def error(
        self,
        msg: str,
        json_params: Optional[Dict[str, Any]] = None,
        skip_if_local: bool = False,
        **kwargs,
    ) -> None:
        self.log(
            msg,
            level=logging.ERROR,
            json_params=json_params,
            skip_if_local=skip_if_local,
            color="\033[0;31m",
            **kwargs,
        )

    @property
    def gcp_logging_client(self) -> Optional[google.cloud.logging.Client]:
        "WARNING: To be deprecated."
        return self._gcp_client

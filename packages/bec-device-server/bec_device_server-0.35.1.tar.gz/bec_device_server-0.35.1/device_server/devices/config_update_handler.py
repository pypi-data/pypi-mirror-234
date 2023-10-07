from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from bec_lib.core import (
    BECMessage,
    BECStatus,
    DeviceConfigError,
    MessageEndpoints,
    bec_logger,
)

if TYPE_CHECKING:
    from devicemanager import DeviceManagerDS

logger = bec_logger.logger


class ConfigUpdateHandler:
    def __init__(self, device_manager: DeviceManagerDS) -> None:
        self.device_manager = device_manager
        self.connector = self.device_manager.connector
        self._config_request_handler = None

        self._start_config_handler()

    def _start_config_handler(self) -> None:
        self._config_request_handler = self.connector.consumer(
            MessageEndpoints.device_server_config_request(),
            cb=self._device_config_callback,
            parent=self,
        )
        self._config_request_handler.start()

    @staticmethod
    def _device_config_callback(msg, *, parent, **_kwargs) -> None:
        msg = BECMessage.DeviceConfigMessage.loads(msg.value)
        logger.info(f"Received request: {msg}")
        parent.parse_config_request(msg)

    def parse_config_request(self, msg: BECMessage.DeviceConfigMessage) -> None:
        """Processes a config request. If successful, it emits a config reply

        Args:
            msg (BMessage.DeviceConfigMessage): Config request

        """
        error_msg = ""
        accepted = True
        try:
            self.device_manager.check_request_validity(msg)
            if msg.content["action"] == "update":
                self._update_config(msg)
            if msg.content["action"] == "add":
                raise NotImplementedError
        except DeviceConfigError as dev_conf_error:
            error_msg = traceback.format_exc()
            accepted = False
        finally:
            self.send_config_request_reply(
                accepted=accepted, error_msg=error_msg, metadata=msg.metadata
            )

    def send_config_request_reply(self, accepted: bool, error_msg: str, metadata: dict) -> None:
        """
        Sends a config request reply

        Args:
            accepted (bool): Whether the request was accepted
            error_msg (str): Error message
            metadata (dict): Metadata of the request
        """
        msg = BECMessage.RequestResponseMessage(
            accepted=accepted, message=error_msg, metadata=metadata
        )
        RID = metadata.get("RID")
        self.device_manager.producer.set(
            MessageEndpoints.device_config_request_response(RID), msg.dumps(), expire=60
        )

    def _update_config(self, msg: BECMessage.DeviceConfigMessage) -> None:
        for dev, dev_config in msg.content["config"].items():
            device = self.device_manager.devices[dev]
            if "deviceConfig" in dev_config:
                # store old config
                old_config = device._config["deviceConfig"].copy()

                # apply config
                try:
                    self.device_manager.update_config(device.obj, dev_config["deviceConfig"])
                except Exception as exc:
                    self.device_manager.update_config(device.obj, old_config)
                    raise DeviceConfigError(f"Error during object update. {exc}")

            if "enabled" in dev_config:
                device._config["enabled"] = dev_config["enabled"]
                if dev_config["enabled"]:
                    # pylint:disable=protected-access
                    if device.obj._destroyed:
                        self.device_manager.initialize_device(device._config)
                    else:
                        self.device_manager.initialize_enabled_device(device)
                else:
                    self.device_manager.disconnect_device(device.obj)
                    self.device_manager.reset_device(device)

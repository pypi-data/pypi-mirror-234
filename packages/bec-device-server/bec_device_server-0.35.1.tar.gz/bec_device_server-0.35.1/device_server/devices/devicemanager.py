import inspect
import traceback
from functools import reduce

import ophyd
import ophyd.sim as ops
import ophyd_devices as opd
from bec_lib.core import (
    BECMessage,
    Device,
    DeviceConfigError,
    DeviceManagerBase,
    MessageEndpoints,
    bec_logger,
)
from bec_lib.core.connector import ConnectorBase
from ophyd.ophydobj import OphydObject
from ophyd.signal import EpicsSignalBase

from device_server.devices.config_update_handler import ConfigUpdateHandler
from device_server.devices.device_serializer import get_device_info

try:
    from bec_plugins import devices as plugin_devices
except ImportError:
    plugin_devices = None


logger = bec_logger.logger


def rgetattr(obj, attr, *args):
    """See https://stackoverflow.com/questions/31174295/getattr-and-setattr-on-nested-objects"""

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return reduce(_getattr, [obj] + attr.split("."))


class DSDevice(Device):
    def __init__(self, name, obj, config, parent=None):
        super().__init__(name, config, parent=parent)
        self.obj = obj
        self.metadata = {}
        self.initialized = False

    def initialize_device_buffer(self, producer):
        """initialize the device read and readback buffer on redis with a new reading"""
        dev_msg = BECMessage.DeviceMessage(signals=self.obj.read(), metadata={}).dumps()
        pipe = producer.pipeline()
        producer.set_and_publish(MessageEndpoints.device_readback(self.name), dev_msg, pipe=pipe)
        producer.set(topic=MessageEndpoints.device_read(self.name), msg=dev_msg, pipe=pipe)
        pipe.execute()
        self.initialized = True


class DeviceManagerDS(DeviceManagerBase):
    def __init__(
        self,
        connector: ConnectorBase,
        config_update_handler: ConfigUpdateHandler = None,
        status_cb: list = None,
    ):
        super().__init__(connector, status_cb)
        self._config_request_connector = None
        self._device_instructions_connector = None
        self._config_update_handler_cls = config_update_handler
        self.config_update_handler = None

    def initialize(self, bootstrap_server) -> None:
        self.config_update_handler = (
            self._config_update_handler_cls
            if self._config_update_handler_cls is not None
            else ConfigUpdateHandler(device_manager=self)
        )
        super().initialize(bootstrap_server)

    def _reload_action(self) -> None:
        for dev, obj in self.devices.items():
            try:
                obj.obj.destroy()
            except Exception:
                logger.warning(f"Failed to destroy {obj.obj.name}")
                raise RuntimeError
        self.devices.flush()
        self._get_config()

    def _get_device_class(self, dev_type):
        module = None
        if hasattr(plugin_devices, dev_type):
            module = plugin_devices
        elif hasattr(ophyd, dev_type):
            module = ophyd
        elif hasattr(opd, dev_type):
            module = opd
        elif hasattr(ops, dev_type):
            module = ops
        elif ":" in dev_type:
            dev_type_scope = dev_type.split(":")
            prefix = dev_type_scope[:-1]
            dev_type = dev_type_scope[-1]
            module = rgetattr(opd, ".".join(prefix))
        else:
            raise TypeError(f"Unknown device class {dev_type}")
        return getattr(module, dev_type)

    def _load_session(self, *_args, **_kwargs):
        if self._is_config_valid():
            for dev in self._session["devices"]:
                name = dev.get("name")
                enabled = dev.get("enabled")
                logger.info(f"Adding device {name}: {'ENABLED' if enabled else 'DISABLED'}")
                try:
                    self.initialize_device(dev)
                except Exception as exc:
                    content = traceback.format_exc()
                    logger.error(f"Failed to initialize device: {dev}: {content}.")

    @staticmethod
    def update_config(obj: OphydObject, config: dict) -> None:
        """Update an ophyd device's config

        Args:
            obj (Ophydobj): Ophyd object that should be updated
            config (dict): Config dictionary

        """
        if hasattr(obj, "update_config"):
            obj.update_config(config)
        else:
            for config_key, config_value in config.items():
                # first handle the ophyd exceptions...
                if config_key == "limits":
                    if hasattr(obj, "low_limit_travel") and hasattr(obj, "high_limit_travel"):
                        obj.low_limit_travel.set(config_value[0])
                        obj.high_limit_travel.set(config_value[1])
                        continue
                if config_key == "labels":
                    if not config_value:
                        config_value = set()
                    # pylint: disable=protected-access
                    obj._ophyd_labels_ = set(config_value)
                    continue
                if not hasattr(obj, config_key):
                    raise DeviceConfigError(
                        f"Unknown config parameter {config_key} for device of type {obj.__class__.__name__}."
                    )

                config_attr = getattr(obj, config_key)
                if isinstance(config_attr, ophyd.Signal):
                    config_attr.set(config_value)
                elif callable(config_attr):
                    config_attr(config_value)
                else:
                    setattr(obj, config_key, config_value)

    def initialize_device(self, dev: dict) -> DSDevice:
        """
        Prepares a device for later usage.
        This includes inspecting the device class signature,
        initializing the object, refreshing the device info and buffer,
        as well as adding subscriptions.
        """
        name = dev.get("name")
        enabled = dev.get("enabled")
        enabled_set = dev.get("enabled_set", True)

        dev_cls = self._get_device_class(dev["deviceClass"])
        config = dev["deviceConfig"].copy()

        # pylint: disable=protected-access
        device_classes = [dev_cls]
        if issubclass(dev_cls, ophyd.Signal):
            device_classes.append(ophyd.Signal)
        if issubclass(dev_cls, EpicsSignalBase):
            device_classes.append(EpicsSignalBase)
        if issubclass(dev_cls, ophyd.OphydObject):
            device_classes.append(ophyd.OphydObject)

        # get all init parameters of the device class and its parents
        class_params = set()
        for device_class in device_classes:
            class_params.update(inspect.signature(device_class)._parameters)
        class_params_and_config_keys = class_params & config.keys()

        init_kwargs = {key: config.pop(key) for key in class_params_and_config_keys}
        device_access = config.pop("device_access", None)
        if device_access or (device_access is None and config.get("device_mapping")):
            init_kwargs["device_manager"] = self

        signature = inspect.signature(dev_cls)
        if "device_manager" in signature.parameters:
            init_kwargs["device_manager"] = self

        # initialize the device object
        obj = dev_cls(**init_kwargs)
        self.update_config(obj, config)

        # refresh the device info
        pipe = self.producer.pipeline()
        self.reset_device_data(obj, pipe)
        self.publish_device_info(obj, pipe)
        pipe.execute()

        # insert the created device obj into the device manager
        opaas_obj = DSDevice(name, obj, config=dev, parent=self)

        # pylint:disable=protected-access # this function is shared with clients and it is currently not foreseen that clients add new devices
        self.devices._add_device(name, opaas_obj)

        if not enabled:
            return opaas_obj

        # update device buffer for enabled devices
        try:
            self.initialize_enabled_device(opaas_obj)
        # pylint:disable=broad-except
        except Exception:
            error_traceback = traceback.format_exc()
            logger.error(
                f"{error_traceback}. Failed to stage {opaas_obj.name}. The device will be disabled."
            )
            opaas_obj.enabled = False

        obj = opaas_obj.obj
        # add subscriptions
        if "readback" in obj.event_types:
            obj.subscribe(self._obj_callback_readback, run=opaas_obj.enabled)
        elif "value" in obj.event_types:
            obj.subscribe(self._obj_callback_readback, run=opaas_obj.enabled)

        if "done_moving" in obj.event_types:
            obj.subscribe(self._obj_callback_done_moving, event_type="done_moving", run=False)
        if "flyer" in obj.event_types:
            obj.subscribe(self._obj_flyer_callback, event_type="flyer", run=False)
        if "progress" in obj.event_types:
            obj.subscribe(self._obj_progress_callback, event_type="progress", run=False)
        if hasattr(obj, "motor_is_moving"):
            obj.motor_is_moving.subscribe(self._obj_callback_is_moving, run=opaas_obj.enabled)

        return opaas_obj

    def initialize_enabled_device(self, opaas_obj):
        """connect to an enabled device and initialize the device buffer"""
        self.connect_device(opaas_obj.obj)
        opaas_obj.initialize_device_buffer(self.producer)

    @staticmethod
    def disconnect_device(obj):
        """disconnect from a device"""
        if not obj.connected:
            return
        if hasattr(obj, "controller"):
            obj.controller.off()
            return
        obj.destroy()

    def reset_device(self, obj: DSDevice):
        """reset a device"""
        obj.initialized = False

    @staticmethod
    def connect_device(obj):
        """establish a connection to a device"""
        if obj.connected:
            return
        if hasattr(obj, "controller"):
            obj.controller.on()
            return
        if hasattr(obj, "wait_for_connection"):
            obj.wait_for_connection(timeout=10)
            return

        logger.error(
            f"Device {obj.name} does not implement the socket controller interface nor wait_for_connection and cannot be turned on."
        )
        raise ConnectionError(f"Failed to establish a connection to device {obj.name}")

    def publish_device_info(self, obj: OphydObject, pipe=None) -> None:
        """
        Publish the device info to redis. The device info contains
        inter alia the class name, user functions and signals.

        Args:
            obj (_type_): _description_
        """

        interface = get_device_info(obj, {})
        self.producer.set(
            MessageEndpoints.device_info(obj.name),
            BECMessage.DeviceInfoMessage(device=obj.name, info=interface).dumps(),
            pipe,
        )

    def reset_device_data(self, obj: OphydObject, pipe=None) -> None:
        """delete all device data and device info"""
        self.producer.delete(MessageEndpoints.device_status(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_read(obj.name), pipe)
        self.producer.delete(MessageEndpoints.device_info(obj.name), pipe)

    def _obj_callback_readback(self, *_args, **kwargs):
        obj = kwargs["obj"]
        if obj.connected:
            name = obj.root.name
            signals = obj.read()
            metadata = self.devices.get(obj.root.name).metadata
            dev_msg = BECMessage.DeviceMessage(signals=signals, metadata=metadata).dumps()
            pipe = self.producer.pipeline()
            self.producer.set_and_publish(MessageEndpoints.device_readback(name), dev_msg, pipe)
            pipe.execute()

    def _obj_callback_acq_done(self, *_args, **kwargs):
        device = kwargs["obj"].root.name
        status = 0
        metadata = self.devices[device].metadata
        self.producer.send(
            MessageEndpoints.device_status(device),
            BECMessage.DeviceStatusMessage(device=device, status=status, metadata=metadata).dumps(),
        )

    def _obj_callback_done_moving(self, *args, **kwargs):
        self._obj_callback_readback(*args, **kwargs)
        # self._obj_callback_acq_done(*args, **kwargs)

    def _obj_callback_is_moving(self, *_args, **kwargs):
        device = kwargs["obj"].root.name
        status = int(kwargs.get("value"))
        metadata = self.devices[device].metadata
        self.producer.set(
            MessageEndpoints.device_status(kwargs["obj"].root.name),
            BECMessage.DeviceStatusMessage(device=device, status=status, metadata=metadata).dumps(),
        )

    def _obj_flyer_callback(self, *_args, **kwargs):
        obj = kwargs["obj"]
        data = kwargs["value"].get("data")
        ds_obj = self.devices[obj.root.name]
        metadata = ds_obj.metadata
        if "scanID" not in metadata:
            return

        if not hasattr(ds_obj, "emitted_points"):
            ds_obj.emitted_points = {}

        emitted_points = ds_obj.emitted_points.get(metadata["scanID"], 0)

        # make sure all arrays are of equal length
        max_points = min(len(d) for d in data.values())
        bundle = BECMessage.BundleMessage()
        for ii in range(emitted_points, max_points):
            signals = {}
            for key, val in data.items():
                signals[key] = {"value": val[ii]}
            bundle.append(
                BECMessage.DeviceMessage(
                    signals=signals,
                    metadata={"pointID": ii, **metadata},
                ).dumps()
            )
        ds_obj.emitted_points[metadata["scanID"]] = max_points
        pipe = self.producer.pipeline()
        self.producer.send(MessageEndpoints.device_read(obj.root.name), bundle.dumps(), pipe=pipe)
        msg = BECMessage.DeviceStatusMessage(
            device=obj.root.name, status=max_points, metadata=metadata
        )
        self.producer.set_and_publish(
            MessageEndpoints.device_progress(obj.root.name), msg.dumps(), pipe=pipe
        )
        pipe.execute()

    def _obj_progress_callback(self, *_args, obj, value, max_value, done, **kwargs):
        metadata = self.devices[obj.root.name].metadata
        msg = BECMessage.ProgressMessage(
            value=value,
            max_value=max_value,
            done=done,
            metadata=metadata,
        )
        self.producer.set_and_publish(MessageEndpoints.device_progress(obj.root.name), msg.dumps())

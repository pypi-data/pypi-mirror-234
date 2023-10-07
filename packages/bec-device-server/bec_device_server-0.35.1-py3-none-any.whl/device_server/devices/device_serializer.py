import msgpack
from bec_lib.core.numpy_encoder import numpy_encode
from ophyd import Device, PositionerBase, Signal


def is_serializable(var) -> bool:
    """check if an object is serializable"""
    try:
        msgpack.dumps(var, default=numpy_encode)
        return True
    except (TypeError, OverflowError):
        return False


def get_custom_user_access_info(obj, obj_interface):
    """extract user access method from an object"""
    # user_funcs = get_user_functions(obj)
    if hasattr(obj, "USER_ACCESS"):
        for var in [func for func in dir(obj) if func in obj.USER_ACCESS]:
            obj_member = getattr(obj, var)
            if not callable(obj_member):
                if is_serializable(obj_member):
                    obj_interface[var] = {"type": type(obj_member).__name__}
                elif get_device_base_class(obj_member) == "unknown":
                    obj_interface[var] = get_custom_user_access_info(obj_member, {})
                else:
                    continue
            else:
                obj_interface[var] = {"type": "func", "doc": obj_member.__doc__}
    return obj_interface


def get_device_base_class(obj) -> str:
    if isinstance(obj, PositionerBase):
        return "positioner"
    if isinstance(obj, Signal):
        return "signal"
    if isinstance(obj, Device):
        return "device"
    return "unknown"


def get_device_info(obj, device_info):
    """
    {
        "device_name": "samx",
            "device_info": {
                "device_base_class": "",
                "signals": {},
                "custom_user_access": {},
                "sub_devices": {
                    "device_name": "samx_sub",
                    "device_info": {
                        "device_base_class": "",
                        "signals": {},
                        "custom_user_access": {},
                        "sub_devices": {},
                    },
                },
            },
        }

    Args:
        obj (_type_): _description_
        device_info (_type_): _description_

    Returns:
        _type_: _description_
    """
    user_access = get_custom_user_access_info(obj, {})
    signals = []
    if hasattr(obj, "component_names"):
        for component_name in obj.component_names:
            if get_device_base_class(getattr(obj, component_name)) == "signal":
                signals.append(component_name)
    sub_devices = []
    if hasattr(obj, "walk_subdevices"):
        for _, dev in obj.walk_subdevices():
            sub_devices.append(get_device_info(dev, {}))
    return {
        "device_name": obj.name,
        "device_attr_name": getattr(obj, "attr_name", ""),
        "device_dotted_name": getattr(obj, "dotted_name", ""),
        "device_info": {
            "device_base_class": get_device_base_class(obj),
            "signals": signals,
            "hints": obj.hints,
            "describe": obj.describe(),
            "describe_configuration": obj.describe_configuration(),
            "sub_devices": sub_devices,
            "custom_user_access": user_access,
        },
    }

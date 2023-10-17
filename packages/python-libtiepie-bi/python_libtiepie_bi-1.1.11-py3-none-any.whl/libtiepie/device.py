""" python-libtiepie - Python interface for libtiepie-hw library

Copyright (c) 2023 TiePie engineering

Website: http://www.tiepie.com/LibTiePie

"""

from .api import api
from .const import *
from .utils import *
from .library import library
from .object import Object
from .triggerinputs import TriggerInputs
from .triggeroutputs import TriggerOutputs


class Device(Object):
    """"""

    def __init__(self, handle):
        super(Device, self).__init__(handle)
        self._trigger_inputs = TriggerInputs(handle)
        self._trigger_outputs = TriggerOutputs(handle)

    def _get_trigger_inputs(self):
        return self._trigger_inputs

    def _get_trigger_outputs(self):
        return self._trigger_outputs

    def _get_calibration_date(self):
        """  """
        value = api.tiepie_hw_device_get_calibration_date(self._handle)
        library.check_last_status_raise_on_error()
        return convert_date(value)

    def _get_serial_number(self):
        """ Serial number of the device. """
        value = api.tiepie_hw_device_get_serial_number(self._handle)
        library.check_last_status_raise_on_error()
        return value

    def _get_ip_address(self):
        """ IP address of the device. """
        length = api.tiepie_hw_device_get_ip_address(self._handle, None, 0)
        library.check_last_status_raise_on_error()
        buf = create_string_buffer(length + 1)
        api.tiepie_hw_device_get_ip_address(self._handle, buf, length)
        library.check_last_status_raise_on_error()
        return buf.value.decode('utf-8')

    def _get_ip_port(self):
        """ IP port number of the device. """
        value = api.tiepie_hw_device_get_ip_port(self._handle)
        library.check_last_status_raise_on_error()
        return value

    def _get_product_id(self):
        """ Product id of the device. """
        value = api.tiepie_hw_device_get_product_id(self._handle)
        library.check_last_status_raise_on_error()
        return value

    def _get_type(self):
        """ Device type. """
        value = api.tiepie_hw_device_get_type(self._handle)
        library.check_last_status_raise_on_error()
        return value

    def _get_name(self):
        """ Full name of the device. """
        length = api.tiepie_hw_device_get_name(self._handle, None, 0)
        library.check_last_status_raise_on_error()
        buf = create_string_buffer(length + 1)
        api.tiepie_hw_device_get_name(self._handle, buf, length)
        library.check_last_status_raise_on_error()
        return buf.value.decode('utf-8')

    def _get_name_short(self):
        """ Short name of the device. """
        length = api.tiepie_hw_device_get_name_short(self._handle, None, 0)
        library.check_last_status_raise_on_error()
        buf = create_string_buffer(length + 1)
        api.tiepie_hw_device_get_name_short(self._handle, buf, length)
        library.check_last_status_raise_on_error()
        return buf.value.decode('utf-8')

    def _get_name_shortest(self):
        """ Short name of the device without model postfix. """
        length = api.tiepie_hw_device_get_name_shortest(self._handle, None, 0)
        library.check_last_status_raise_on_error()
        buf = create_string_buffer(length + 1)
        api.tiepie_hw_device_get_name_shortest(self._handle, buf, length)
        library.check_last_status_raise_on_error()
        return buf.value.decode('utf-8')

    def _get_has_wireless_trigger_module(self):
        """ Check whether the device has a wireless trigger module """
        value = api.tiepie_hw_device_has_wireless_trigger_module(self._handle)
        library.check_last_status_raise_on_error()
        return value != BOOL_FALSE

    def _get_has_battery(self):
        """  """
        value = api.tiepie_hw_device_has_battery(self._handle)
        library.check_last_status_raise_on_error()
        return value != BOOL_FALSE

    def _get_battery_charge(self):
        """ Battery charge state of the device's battery in percent. """
        value = api.tiepie_hw_device_get_battery_charge(self._handle)
        library.check_last_status_raise_on_error()
        return value

    def _get_battery_time_to_empty(self):
        """ Expected time in minutes until the battery will be empty. """
        value = api.tiepie_hw_device_get_battery_time_to_empty(self._handle)
        library.check_last_status_raise_on_error()
        return value

    def _get_battery_time_to_full(self):
        """ Expected time in minutes until the battery will be fully charged. """
        value = api.tiepie_hw_device_get_battery_time_to_full(self._handle)
        library.check_last_status_raise_on_error()
        return value

    def _get_is_battery_charger_connected(self):
        """ Check whether a charger is connected to the device. """
        value = api.tiepie_hw_device_is_battery_charger_connected(self._handle)
        library.check_last_status_raise_on_error()
        return value != BOOL_FALSE

    def _get_is_battery_charging(self):
        """ Check whether the device's battery is being charged. """
        value = api.tiepie_hw_device_is_battery_charging(self._handle)
        library.check_last_status_raise_on_error()
        return value != BOOL_FALSE

    def _get_is_battery_broken(self):
        """ Check whether the device's battery is defective. """
        value = api.tiepie_hw_device_is_battery_broken(self._handle)
        library.check_last_status_raise_on_error()
        return value != BOOL_FALSE

    calibration_date = property(_get_calibration_date)
    serial_number = property(_get_serial_number)
    ip_address = property(_get_ip_address)
    ip_port = property(_get_ip_port)
    product_id = property(_get_product_id)
    type = property(_get_type)
    name = property(_get_name)
    name_short = property(_get_name_short)
    name_shortest = property(_get_name_shortest)
    has_wireless_trigger_module = property(_get_has_wireless_trigger_module)
    has_battery = property(_get_has_battery)
    battery_charge = property(_get_battery_charge)
    battery_time_to_empty = property(_get_battery_time_to_empty)
    battery_time_to_full = property(_get_battery_time_to_full)
    is_battery_charger_connected = property(_get_is_battery_charger_connected)
    is_battery_charging = property(_get_is_battery_charging)
    is_battery_broken = property(_get_is_battery_broken)
    trigger_inputs = property(_get_trigger_inputs)
    trigger_outputs = property(_get_trigger_outputs)

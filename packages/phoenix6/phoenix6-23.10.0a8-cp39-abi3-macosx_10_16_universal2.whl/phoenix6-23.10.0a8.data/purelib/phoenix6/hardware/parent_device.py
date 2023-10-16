"""
Base class for Phoenix Hardware Devices
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.base_status_signal import BaseStatusSignal
from phoenix6.status_signal import StatusSignal
from phoenix6.controls.empty_control import EmptyControl
from phoenix6.status_code import StatusCode
from typing import Protocol, Callable, TypeVar

DEFAULT_CONTROL_RATE_PERIOD_SEC = 0.010

class SupportsSendRequest(Protocol):
    control_info: dict

    def _send_request(self, network: str, device_hash: int, cancel_other_requests: bool) -> StatusCode:
        pass

T = TypeVar("T")

class ParentDevice:
    """
    Base class of Phoenix devices.
    This holds the base information for the devices, and
    can be used as a generic type to hold onto a collection
    of multiple devices.
    """

    def __init__(self, device_id: int, model: str, canbus: str):
        """
        Constructor for a device

        :param deviceId: ID of the device
        :type deviceId: int
        :param model: Model of the device
        :type model: str
        :param canbus: CANbus the device is on
        :type canbus: str
        """
        self._device_identifier = DeviceIdentifier(device_id, model, canbus)
        self.__signal_values: dict[int, StatusSignal] = {}
        self.control_request = EmptyControl()

    @property
    def device_id(self) -> int:
        """ID of this device

        :return: ID of this device
        :rtype: int
        """
        return self._device_identifier.device_id

    @property
    def network(self) -> str:
        """
        Network this device is on

        :return: Network this device is on
        :rtype: str
        """
        return self._device_identifier.network

    @property
    def device_hash(self) -> int:
        """
        Hash of this device

        :return: Hash of this device
        :rtype: int
        """
        return self._device_identifier.device_hash

    def optimize_bus_utilization(self, timeoutSeconds: float = 0.05) -> StatusCode:
        """
        Optimizes the device's bus utilization by reducing the
        update frequencies of its status signals.

        All status signals that have not been explicitly gven an
        update frequency will be disabled. Note that if other
        status signals in the same frame have been given an update
        frequency, the update frequency will be honored for the
        entire frame.

        This function only needs to be called once on this device
        in the robot program. Additionally, this method does not
        necessarily need to be called after setting the update
        frequencies of other signals.

        To restore the default status update frequencies, remove
        this method call, redeploy the robot application, and
        power-cycle the devices on the bus. Alternatively, the user
        can override individual status update frequencies using
        setUpdateFrequency.

        :param timeoutSeconds: Maximum amount of time to wait
                               for each status frame when
                               performing the action,
                               defaults to 0.05
        :type timeoutSeconds: float, optional
        :return: Status code of the first failed update frequency
                 set call, or OK if all succeeded.
        :rtype: StatusCode
        """
        pass

    def _report_if_too_old(self):
        pass

    def _set_control_private(self, request: SupportsSendRequest):
        """
        Sets the control request to this device

        :param request: Control request to set
        :type request: SupportsSendRequest
        """
        self._report_if_too_old()
        cancel_other_requests = False
        if request.__class__ is not self.control_request.__class__:
            cancel_other_requests = True

        self.control_request = request
        status = request._send_request(self.network, self.device_hash, cancel_other_requests)

        if not status.is_ok():
            pass # Report error

    def _common_lookup(self, spn: int, map_iter: int, generator: Callable[[], dict[int, StatusSignal]], signal_name: str, report_on_construction: bool, signal_type: type[T]) -> StatusSignal[T]:
        total_hash = spn | (map_iter << 16)
        # Lookup and return if found
        if total_hash in self.__signal_values:
            # Found it, save it under to_find
            to_find = self.__signal_values[total_hash]
            # Since we didn't construct, report errors
            report_on_construction = True
        else:
            # Insert into map
            if map_iter == 0:
                self.__signal_values[total_hash] = StatusSignal(None, self._device_identifier, spn, self._report_if_too_old, None, signal_name, signal_type)
            else:
                if generator is None:
                    return StatusSignal(StatusCode.INVALID_PARAM_VALUE, None, None, None, None, None, None)
                self.__signal_values[total_hash] = StatusSignal(None, self._device_identifier, spn, self._report_if_too_old, generator, signal_name, signal_type)

            # Lookup and return
            to_find = self.__signal_values[total_hash]

        # Refresh and return
        to_find.refresh()
        return to_find

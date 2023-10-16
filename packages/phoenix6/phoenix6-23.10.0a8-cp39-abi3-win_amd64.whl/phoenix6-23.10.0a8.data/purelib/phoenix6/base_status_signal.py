"""
Common base class for StatusSignals
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native, ReturnValues
from phoenix6.timestamp import Timestamp
from phoenix6.all_timestamps import AllTimestamps
from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.status_code import StatusCode
import ctypes


class BaseStatusSignal:
    """
    Common parent type for the :ref:StatusSignal: object.

    This can be used fora  collection of :ref:StatusSignal: object,s
    but we recommend using the derived class instead when possible
    """

    def __init__(self, device_identifer: DeviceIdentifier, spn: int, signal_name: str):
        """
        Normal Constructor for a BaseStatusSignal

        :param deviceIdentifer: Identifier of the device this signal is associated to
        :type deviceIdentifer: DeviceIdentifier
        :param spn: SPN Index of this signal
        :type spn: int
        :param signalName: Name of this signal
        :type signalName: str
        """

        self.__last_timestamp: float = 0
        self._spn: int = spn
        self._value: float = 0
        self._identifier: DeviceIdentifier = device_identifer
        self._status: StatusCode = StatusCode.STATUS_CODE_NOT_INITIALIZED
        self._all_timestamps: AllTimestamps = AllTimestamps()
        self._name: str = signal_name

        # Get the units for this signal
        rets: ReturnValues = ReturnValues()
        Native.instance().c_ctre_phoenix6_get_rets(self._spn, 2, ctypes.byref(rets))

        self._units = rets.units.decode("utf-8")

    @property
    def value_as_double(self) -> float:
        """
        Gets the value as a double instead of the generic
        type. This may be helpful when working with the
        base class.

        :return: Signal as a double
        :rtype: float
        """
        return self._value

    @property
    def identifier(self) -> DeviceIdentifier:
        """
        Identifier for the device this signal is associated to.
        Users may use it for access tot he Device's ID, network
        name, or unique-per-canbus device hash.

        :return: This signal's associated device
        :rtype: DeviceIdentifier
        """
        return self._identifier

    @property
    def units(self) -> str:
        """
        The units associated with this signal.

        :return: Units associated with this signal
        :rtype: str
        """
        return self._units

    @property
    def status(self) -> StatusCode:
        """
        The status of the last time this signal was updated.

        :return: Status of the last time this signal was updated.
        :rtype: StatusCode
        """
        return self._status

    @property
    def all_timestamps(self) -> AllTimestamps:
        """
        All the timestamps associated with this signal.

        :return: All the timestamps associated with this signal.
        :rtype: AllTimestamps
        """
        return self._all_timestamps

    @property
    def timestamp(self) -> Timestamp:
        """
        The most accurate timestamp associated with this signal

        :return: The most accurate timestamp associated with this signal.
        :rtype: Timestamp
        """
        return self._all_timestamps.get_best_timestamp()

    @property
    def name(self) -> str:
        """
        The name of this signal.

        :return: The name of this signal.
        :rtype: str
        """
        return self._name

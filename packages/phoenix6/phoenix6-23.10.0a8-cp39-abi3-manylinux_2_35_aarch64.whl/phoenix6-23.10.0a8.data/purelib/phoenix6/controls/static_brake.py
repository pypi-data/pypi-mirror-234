"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class StaticBrake:
    def __init__(self):
        """
        Applies full neutral-brake by shorting motor leads together.
        
        """
        self.control_info = {}
        self.control_info["name"] = "StaticBrake"
        self.update_freq_hz = 100.0
        

    def _send_request(self, network: str, device_hash: int, cancel_other_requests: bool) -> StatusCode:
        """
        Sends this request out over CAN bus to the device for
        the device to apply.

        :param network: Network to send request over
        :type network: str
        :param device_hash: Device to send request to
        :type device_hash: int
        :param cancel_other_requests: True to cancel other requests
        :type cancel_other_requests: bool
        :returns: Status of the send operation
        :rtype: StatusCode
        """

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlStaticBrake(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests))

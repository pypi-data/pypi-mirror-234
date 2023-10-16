"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class EmptyControl:
    """
    Generic empty control class used to do nothing
    """

    def __init__(self):
        """
        Constructs an empty control request
        """
        self.control_info = dict()
        self.control_info["name"] = "EmptyControl"

    def __str__(self):
        return "class: EmptyControl"

    def _send_request(
        self, network: str, device_hash: int, cancel_other_requests: bool
    ) -> StatusCode:
        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlEmpty(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, 0, cancel_other_requests))

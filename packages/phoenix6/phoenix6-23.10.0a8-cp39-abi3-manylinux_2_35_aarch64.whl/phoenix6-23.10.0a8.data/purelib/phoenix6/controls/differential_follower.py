"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class DifferentialFollower:
    def __init__(self, master_id: int, oppose_master_direction: bool):
        """
        Follow the differential motor output of another Talon.
        |
        If Talon is in torque control, the torque is copied - which will increase the
        total torque applied. If Talon is in percent supply output control, the duty
        cycle is matched.  Motor direction either matches master's configured direction
        or opposes it based on OpposeMasterDirection.
        
        :param master_id:    Device ID of the differential master to follow.
        :type master_id: int
        :param oppose_master_direction:    Set to false for motor invert to match the
                                           master's configured Invert - which is typical
                                           when master and follower are mechanically
                                           linked and spin in the same direction.  Set
                                           to true for motor invert to oppose the
                                           master's configured Invert - this is typical
                                           where the the master and follower
                                           mechanically spin in opposite directions.
        :type oppose_master_direction: bool
        """
        self.control_info = {}
        self.control_info["name"] = "DifferentialFollower"
        self.update_freq_hz = 100.0
        
        self.master_id = master_id
        """
        Device ID of the differential master to follow.
        """
        self.oppose_master_direction = oppose_master_direction
        """
        Set to false for motor invert to match the master's configured Invert - which is
        typical when master and follower are mechanically linked and spin in the same
        direction.  Set to true for motor invert to oppose the master's configured
        Invert - this is typical where the the master and follower mechanically spin in
        opposite directions.
        """

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

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlDifferentialFollower(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.master_id, self.oppose_master_direction))

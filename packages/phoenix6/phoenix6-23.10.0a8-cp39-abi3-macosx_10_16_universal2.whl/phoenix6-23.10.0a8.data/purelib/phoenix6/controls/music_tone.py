"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class MusicTone:
    def __init__(self, audio_frequency: float):
        """
        Plays a single tone at the user specified frequency.
        
        :param audio_frequency:    Sound frequency to play.  A value of zero will
                                   silence the device. The effective frequency range is
                                   10-10000Hz.  Any nonzero frequency less than 10 Hz
                                   will be capped to 10Hz.  Any frequency above 10Khz
                                   will be capped to 10KHz.
        :type audio_frequency: float
        """
        self.control_info = {}
        self.control_info["name"] = "MusicTone"
        self.update_freq_hz = 100.0
        
        self.audio_frequency = audio_frequency
        """
        Sound frequency to play.  A value of zero will silence the device. The effective
        frequency range is 10-10000Hz.  Any nonzero frequency less than 10 Hz will be
        capped to 10Hz.  Any frequency above 10Khz will be capped to 10KHz.
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

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlMusicTone(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.audio_frequency))

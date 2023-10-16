"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class TorqueCurrentFOC:
    def __init__(self, output: float, max_abs_duty_cycle: float, deadband: float, override_coast_dur_neutral: bool):
        """
        Requires Phoenix Pro;
        Request a specified motor current (field oriented
        control).
        |
        This control request will drive the motor to the requested motor (stator)
        current value.  This leverages field oriented control (FOC), which means greater
        peak power than what is documented.  This scales to torque based on Motor's kT
        constant.
        
        :param output:    Amount of motor current in Amperes
        :type output: float
        :param max_abs_duty_cycle:    The maximum absolute motor output that can be
                                      applied, which effectively limits the velocity.
                                      For example, 0.50 means no more than 50% output in
                                      either direction.  This is useful for preventing
                                      the motor from spinning to its terminal velocity
                                      when there is no external torque applied unto the
                                      rotor.  Note this is absolute maximum, so the
                                      value should be between zero and one.
        :type max_abs_duty_cycle: float
        :param deadband:    Deadband in Amperes.  If torque request is within deadband,
                            the bridge output is neutral. If deadband is set to zero
                            then there is effectively no deadband. Note if deadband is
                            zero, a free spinning motor will spin for quite a while as
                            the firmware attempts to hold the motor's bemf. If user
                            expects motor to cease spinning quickly with a demand of
                            zero, we recommend a deadband of one Ampere. This value will
                            be converted to an integral value of amps.
        :type deadband: float
        :param override_coast_dur_neutral:    Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
        :type override_coast_dur_neutral: bool
        """
        self.control_info = {}
        self.control_info["name"] = "TorqueCurrentFOC"
        self.update_freq_hz = 100.0
        
        self.output = output
        """
        Amount of motor current in Amperes
        """
        self.max_abs_duty_cycle = max_abs_duty_cycle
        """
        The maximum absolute motor output that can be applied, which effectively limits
        the velocity. For example, 0.50 means no more than 50% output in either
        direction.  This is useful for preventing the motor from spinning to its
        terminal velocity when there is no external torque applied unto the rotor.  Note
        this is absolute maximum, so the value should be between zero and one.
        """
        self.deadband = deadband
        """
        Deadband in Amperes.  If torque request is within deadband, the bridge output is
        neutral. If deadband is set to zero then there is effectively no deadband. Note
        if deadband is zero, a free spinning motor will spin for quite a while as the
        firmware attempts to hold the motor's bemf. If user expects motor to cease
        spinning quickly with a demand of zero, we recommend a deadband of one Ampere.
        This value will be converted to an integral value of amps.
        """
        self.override_coast_dur_neutral = override_coast_dur_neutral
        """
        Set to true to coast the rotor when output is zero (or within deadband).  Set to
        false to use the NeutralMode configuration setting (default). This flag exists
        to provide the fundamental behavior of this control when output is zero, which
        is to provide 0A (zero torque).
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

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlTorqueCurrentFOC(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.output, self.max_abs_duty_cycle, self.deadband, self.override_coast_dur_neutral))

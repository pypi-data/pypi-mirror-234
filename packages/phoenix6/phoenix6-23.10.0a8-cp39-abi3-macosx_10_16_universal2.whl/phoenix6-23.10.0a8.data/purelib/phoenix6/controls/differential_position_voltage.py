"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class DifferentialPositionVoltage:
    def __init__(self, target_position: float, differential_position: float, enable_foc: bool, target_slot: int, differential_slot: int, override_brake_dur_neutral: bool):
        """
        Request PID to target position with a differential position setpoint
        |
        This control mode will set the motor's position setpoint to the position
        specified by the user. It will also set the motor's differential position
        setpoint to the specified position.
        
        :param target_position:    Average position to drive toward in rotations.
        :type target_position: float
        :param differential_position:    Differential position to drive toward in
                                         rotations.
        :type differential_position: float
        :param enable_foc:    Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.  FOC improves motor performance
                              by leveraging torque (current) control.  However, this may
                              be inconvenient for applications that require specifying
                              duty cycle or voltage.  CTR-Electronics has developed a
                              hybrid method that combines the performances gains of FOC
                              while still allowing applications to provide duty cycle or
                              voltage demand.  This not to be confused with simple
                              sinusoidal control or phase voltage control which lacks
                              the performance gains.
        :type enable_foc: bool
        :param target_slot:    Select which gains are applied to the primary controller
                               by selecting the slot.  Use the configuration api to set
                               the gain values for the selected slot before enabling
                               this feature. Slot must be within [0,2].
        :type target_slot: int
        :param differential_slot:    Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
        :type differential_slot: int
        :param override_brake_dur_neutral:    Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
        :type override_brake_dur_neutral: bool
        """
        self.control_info = {}
        self.control_info["name"] = "DifferentialPositionVoltage"
        self.update_freq_hz = 100.0
        
        self.target_position = target_position
        """
        Average position to drive toward in rotations.
        """
        self.differential_position = differential_position
        """
        Differential position to drive toward in rotations.
        """
        self.enable_foc = enable_foc
        """
        Set to true to use FOC commutation (requires Phoenix Pro), which increases peak
        power by ~15%. Set to false to use trapezoidal commutation.  FOC improves motor
        performance by leveraging torque (current) control.  However, this may be
        inconvenient for applications that require specifying duty cycle or voltage. 
        CTR-Electronics has developed a hybrid method that combines the performances
        gains of FOC while still allowing applications to provide duty cycle or voltage
        demand.  This not to be confused with simple sinusoidal control or phase voltage
        control which lacks the performance gains.
        """
        self.target_slot = target_slot
        """
        Select which gains are applied to the primary controller by selecting the slot. 
        Use the configuration api to set the gain values for the selected slot before
        enabling this feature. Slot must be within [0,2].
        """
        self.differential_slot = differential_slot
        """
        Select which gains are applied to the differential controller by selecting the
        slot.  Use the configuration api to set the gain values for the selected slot
        before enabling this feature. Slot must be within [0,2].
        """
        self.override_brake_dur_neutral = override_brake_dur_neutral
        """
        Set to true to static-brake the rotor when output is zero (or within deadband). 
        Set to false to use the NeutralMode configuration setting (default). This flag
        exists to provide the fundamental behavior of this control when output is zero,
        which is to provide 0V to the motor.
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

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlDifferentialPositionVoltage(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.target_position, self.differential_position, self.enable_foc, self.target_slot, self.differential_slot, self.override_brake_dur_neutral))

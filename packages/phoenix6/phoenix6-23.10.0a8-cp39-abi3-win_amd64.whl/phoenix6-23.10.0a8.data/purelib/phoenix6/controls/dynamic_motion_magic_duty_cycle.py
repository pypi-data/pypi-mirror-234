"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
import ctypes


class DynamicMotionMagicDutyCycle:
    def __init__(self, position: float, velocity: float, acceleration: float, jerk: float, enable_foc: bool, feed_forward: float, slot: int, override_brake_dur_neutral: bool):
        """
        Requires Phoenix Pro and CANivore;
        Requests Motion Magic® to target a final
        position using a motion profile.  This dynamic request allows runtime changes to
        Cruise Velocity, Acceleration, and Jerk.  Users can optionally provide a duty
        cycle feedforward.  This control requires use of a CANivore.
        |
        Motion Magic® produces a motion profile in real-time while attempting to honor
        the specified Cruise Velocity, Acceleration, and Jerk value.  Target position
        can be changed on-the-fly and Motion Magic® will do its best to adjust the
        profile. This control mode is duty cycle based, so relevant closed-loop gains
        will use fractional duty cycle for the numerator:  +1.0 represents full forward
        output.
        
        :param position:    Position to drive toward in rotations.
        :type position: float
        :param velocity:    Cruise velocity for profiling.  The signage does not matter
                            as the device will use the absolute value for profile
                            generation.
        :type velocity: float
        :param acceleration:    Acceleration for profiling.  The signage does not matter
                                as the device will use the absolute value for profile
                                generation
        :type acceleration: float
        :param jerk:    Jerk for profiling.  The signage does not matter as the device
                        will use the absolute value for profile generation
        :type jerk: float
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
        :param feed_forward:    Feedforward to apply in fractional units between -1 and
                                +1.
        :type feed_forward: float
        :param slot:    Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
        :type slot: int
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
        self.control_info["name"] = "DynamicMotionMagicDutyCycle"
        self.update_freq_hz = 100.0
        
        self.position = position
        """
        Position to drive toward in rotations.
        """
        self.velocity = velocity
        """
        Cruise velocity for profiling.  The signage does not matter as the device will
        use the absolute value for profile generation.
        """
        self.acceleration = acceleration
        """
        Acceleration for profiling.  The signage does not matter as the device will use
        the absolute value for profile generation
        """
        self.jerk = jerk
        """
        Jerk for profiling.  The signage does not matter as the device will use the
        absolute value for profile generation
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
        self.feed_forward = feed_forward
        """
        Feedforward to apply in fractional units between -1 and +1.
        """
        self.slot = slot
        """
        Select which gains are applied by selecting the slot.  Use the configuration api
        to set the gain values for the selected slot before enabling this feature. Slot
        must be within [0,2].
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

        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlDynamicMotionMagicDutyCycle(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, cancel_other_requests, self.position, self.velocity, self.acceleration, self.jerk, self.enable_foc, self.feed_forward, self.slot, self.override_brake_dur_neutral))

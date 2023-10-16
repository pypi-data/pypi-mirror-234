"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.configs.config_groups import *
from phoenix6.configs.parent_configurator import ParentConfigurator
from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.status_code import StatusCode


class TalonFXConfiguration:
    """
    Class description for the Talon FX integrated motor controller that runs on
    associated Falcon motors.

    This handles the configurations for TalonFX
    """

    def __init__(self):

        self.future_proof_configs: bool = True
        """
        True if we should factory default newer unsupported configs,
        false to leave newer unsupported configs alone.

        This flag addresses a corner case where the device may have
        firmware with newer configs that didn't exist when this
        version of the API was built. If this occurs and this
        flag is true, unsupported new configs will be factory
        defaulted to avoid unexpected behavior.

        This is also the behavior in Phoenix 5, so this flag
        is defaulted to true to match.
        """

        
        self.motor_output: MotorOutputConfigs = MotorOutputConfigs()
        """
        Configs that directly affect motor-output.
        |
        Includes Motor Invert and various limit features.
        """
        
        
        self.current_limits: CurrentLimitsConfigs = CurrentLimitsConfigs()
        """
        Configs that directly affect current limiting features.
        |
        Contains the supply/stator current limit thresholds and whether to
        enable them or not.
        """
        
        
        self.voltage: VoltageConfigs = VoltageConfigs()
        """
        Voltage-specific configs
        |
        Voltage-specific configs
        """
        
        
        self.torque_current: TorqueCurrentConfigs = TorqueCurrentConfigs()
        """
        Configs to control the maximum and minimum applied torque when using
        Torque Current control types.
        |
        Similar to peak output, but for the TorqueCurrentFOC control type
        requests.
        """
        
        
        self.feedback: FeedbackConfigs = FeedbackConfigs()
        """
        Configs that affect the feedback of this motor controller.
        |
        Includes feedback sensor source, any offsets for the feedback sensor,
        and various ratios to describe the relationship between the sensor and
        the mechanism for closed looping.
        """
        
        
        self.differential_sensors: DifferentialSensorsConfigs = DifferentialSensorsConfigs()
        """
        Configs related to sensors used for differential control of a
        mechanism.
        |
        Includes the differential sensor sources and IDs.
        """
        
        
        self.differential_constants: DifferentialConstantsConfigs = DifferentialConstantsConfigs()
        """
        Configs related to constants used for differential control of a
        mechanism.
        |
        Includes the differential peak outputs.
        """
        
        
        self.open_loop_ramps: OpenLoopRampsConfigs = OpenLoopRampsConfigs()
        """
        Configs that affect the open-loop control of this motor controller.
        |
        Open-loop ramp rates for the various control types.
        """
        
        
        self.closed_loop_ramps: ClosedLoopRampsConfigs = ClosedLoopRampsConfigs()
        """
        Configs that affect the closed-loop control of this motor controller.
        |
        Closed-loop ramp rates for the various control types.
        """
        
        
        self.hardware_limit_switch: HardwareLimitSwitchConfigs = HardwareLimitSwitchConfigs()
        """
        Configs that change how the motor controller behaves under different
        limit switch statse.
        |
        Includes configs such as enabling limit switches, configuring the
        remote sensor ID, the source, and the position to set on limit.
        """
        
        
        self.audio: AudioConfigs = AudioConfigs()
        """
        Configs that affect audible components of the device.
        |
        Includes configuration for the beep on boot.
        """
        
        
        self.software_limit_switch: SoftwareLimitSwitchConfigs = SoftwareLimitSwitchConfigs()
        """
        Configs that affect how software-limit switches behave.
        |
        Includes enabling software-limit switches and the threshold at which
        they're tripped.
        """
        
        
        self.motion_magic: MotionMagicConfigs = MotionMagicConfigs()
        """
        Configs for Motion Magic®.
        |
        Includes Velocity, Acceleration, and Jerk parameters.
        """
        
        
        self.custom_params: CustomParamsConfigs = CustomParamsConfigs()
        """
        Custom Params.
        |
        Custom paramaters that have no real impact on controller.
        """
        
        
        self.closed_loop_general: ClosedLoopGeneralConfigs = ClosedLoopGeneralConfigs()
        """
        Configs that affect general behavior during closed-looping.
        |
        Includes Continuous Wrap features.
        """
        
        
        self.slot0: Slot0Configs = Slot0Configs()
        """
        Gains for the specified slot.
        |
        If this slot is selected, these gains are used in closed loop control
        requests.
        """
        
        
        self.slot1: Slot1Configs = Slot1Configs()
        """
        Gains for the specified slot.
        |
        If this slot is selected, these gains are used in closed loop control
        requests.
        """
        
        
        self.slot2: Slot2Configs = Slot2Configs()
        """
        Gains for the specified slot.
        |
        If this slot is selected, these gains are used in closed loop control
        requests.
        """
        

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation of this object
        :rtype: str
        """
        ss = []
        ss.append(str(self.motor_output))
        ss.append(str(self.current_limits))
        ss.append(str(self.voltage))
        ss.append(str(self.torque_current))
        ss.append(str(self.feedback))
        ss.append(str(self.differential_sensors))
        ss.append(str(self.differential_constants))
        ss.append(str(self.open_loop_ramps))
        ss.append(str(self.closed_loop_ramps))
        ss.append(str(self.hardware_limit_switch))
        ss.append(str(self.audio))
        ss.append(str(self.software_limit_switch))
        ss.append(str(self.motion_magic))
        ss.append(str(self.custom_params))
        ss.append(str(self.closed_loop_general))
        ss.append(str(self.slot0))
        ss.append(str(self.slot1))
        ss.append(str(self.slot2))
        return "\n".join(ss)


    def serialize(self) -> str:
        """
        Get the serialized form of this configuration

        :return: Serialized form of this config group
        :rtype: str
        """
        ss = []
        ss.append(self.motor_output.serialize())
        ss.append(self.current_limits.serialize())
        ss.append(self.voltage.serialize())
        ss.append(self.torque_current.serialize())
        ss.append(self.feedback.serialize())
        ss.append(self.differential_sensors.serialize())
        ss.append(self.differential_constants.serialize())
        ss.append(self.open_loop_ramps.serialize())
        ss.append(self.closed_loop_ramps.serialize())
        ss.append(self.hardware_limit_switch.serialize())
        ss.append(self.audio.serialize())
        ss.append(self.software_limit_switch.serialize())
        ss.append(self.motion_magic.serialize())
        ss.append(self.custom_params.serialize())
        ss.append(self.closed_loop_general.serialize())
        ss.append(self.slot0.serialize())
        ss.append(self.slot1.serialize())
        ss.append(self.slot2.serialize())
        return "".join(ss)

    def deserialize(self, to_deserialize: str) -> StatusCode:
        """
        Take a string and deserialize it to this configuration

        :return: Return code of the deserialize method
        :rtype: str
        """
        err: StatusCode = StatusCode.OK
        err = self.motor_output.deserialize(to_deserialize)
        err = self.current_limits.deserialize(to_deserialize)
        err = self.voltage.deserialize(to_deserialize)
        err = self.torque_current.deserialize(to_deserialize)
        err = self.feedback.deserialize(to_deserialize)
        err = self.differential_sensors.deserialize(to_deserialize)
        err = self.differential_constants.deserialize(to_deserialize)
        err = self.open_loop_ramps.deserialize(to_deserialize)
        err = self.closed_loop_ramps.deserialize(to_deserialize)
        err = self.hardware_limit_switch.deserialize(to_deserialize)
        err = self.audio.deserialize(to_deserialize)
        err = self.software_limit_switch.deserialize(to_deserialize)
        err = self.motion_magic.deserialize(to_deserialize)
        err = self.custom_params.deserialize(to_deserialize)
        err = self.closed_loop_general.deserialize(to_deserialize)
        err = self.slot0.deserialize(to_deserialize)
        err = self.slot1.deserialize(to_deserialize)
        err = self.slot2.deserialize(to_deserialize)
        return err



class TalonFXConfigurator(ParentConfigurator):
    """
 * Class description for the Talon FX integrated motor controller that runs on
 * associated Falcon motors.

    This handles the configurations for TalonFX
    """

    def __init__(self, id: DeviceIdentifier):
        super().__init__(id)

    def refresh(self, configs: SupportsSerialization, timeout_seconds: float = 0.050) -> StatusCode:
        """
        Refreshes the values of the specified config group.

        Call to refresh the selected configs from the device.

        :param configs: The configs to refresh
        :type configs: name
        :param timeout_seconds: Maximum amount of time to wait when performing configuration
        :type timeout_seconds: double
        :return: StatusCode of refreshing the configs
        :rtype: StatusCode
        """
        err, serialized_string = self._get_configs_private(timeout_seconds)
        if err.is_ok():
            # Only deserialize if we successfully got configs
            configs.deserialize(serialized_string)
        return err

    def apply(self, configs: SupportsSerialization, timeout_seconds: float = 0.050) -> StatusCode:
        """
        Applies the contents of the specified config to the device.

        Call to apply the selected configs.

        :param configs: Configs to apply
        :type configs: SupportsSerialization
        :param timeout_seconds: Maximum amount of time to wait when performing configuration
        :type timeout_seconds: float
        :return: StatusCode of the apply method
        :rtype: StatusCode
        """
        if hasattr(configs, "future_proof_configs"):
            # If this object has a future_proof_configs member variable, use it
            future_proof_configs = getattr(configs, "future_proof_configs")
        else:
            # Otherwise default to not using it so our config-groups don't overwrite other groups
            future_proof_configs = False
        return self._set_configs_private(configs.serialize(), timeout_seconds, future_proof_configs, False)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


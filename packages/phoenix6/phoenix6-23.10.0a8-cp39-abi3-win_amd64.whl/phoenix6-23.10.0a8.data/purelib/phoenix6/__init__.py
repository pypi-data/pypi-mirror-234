"""
Phoenix 6 library built for Python.

View documentation for Phoenix 6, Tuner, and other CTR documentation
at the CTR documentation landing page: docs.ctr-electronics.com
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""


from .all_timestamps import AllTimestamps
from .timestamp import Timestamp
from .status_signal import (StatusSignal, volt, ampere, rotation, rotations_per_second,
                            rotations_per_second_squared, rotations_per_second_cubed,
                            degree, degrees_per_second, celcius, microsecond,
                            millisecond, second, microtesla, g, hertz)
from .status_code import StatusCode
from .controls.duty_cycle_out import DutyCycleOut
from .controls.torque_current_foc import TorqueCurrentFOC
from .controls.voltage_out import VoltageOut
from .controls.position_duty_cycle import PositionDutyCycle
from .controls.position_voltage import PositionVoltage
from .controls.position_torque_current_foc import PositionTorqueCurrentFOC
from .controls.velocity_duty_cycle import VelocityDutyCycle
from .controls.velocity_voltage import VelocityVoltage
from .controls.velocity_torque_current_foc import VelocityTorqueCurrentFOC
from .controls.motion_magic_duty_cycle import MotionMagicDutyCycle
from .controls.motion_magic_voltage import MotionMagicVoltage
from .controls.motion_magic_torque_current_foc import MotionMagicTorqueCurrentFOC
from .controls.differential_duty_cycle import DifferentialDutyCycle
from .controls.differential_voltage import DifferentialVoltage
from .controls.differential_position_duty_cycle import DifferentialPositionDutyCycle
from .controls.differential_position_voltage import DifferentialPositionVoltage
from .controls.differential_velocity_duty_cycle import DifferentialVelocityDutyCycle
from .controls.differential_velocity_voltage import DifferentialVelocityVoltage
from .controls.differential_motion_magic_duty_cycle import DifferentialMotionMagicDutyCycle
from .controls.differential_motion_magic_voltage import DifferentialMotionMagicVoltage
from .controls.follower import Follower
from .controls.strict_follower import StrictFollower
from .controls.differential_follower import DifferentialFollower
from .controls.differential_strict_follower import DifferentialStrictFollower
from .controls.neutral_out import NeutralOut
from .controls.coast_out import CoastOut
from .controls.static_brake import StaticBrake
from .controls.music_tone import MusicTone
from .controls.motion_magic_velocity_duty_cycle import MotionMagicVelocityDutyCycle
from .controls.motion_magic_velocity_torque_current_foc import MotionMagicVelocityTorqueCurrentFOC
from .controls.motion_magic_velocity_voltage import MotionMagicVelocityVoltage
from .controls.dynamic_motion_magic_duty_cycle import DynamicMotionMagicDutyCycle
from .controls.dynamic_motion_magic_voltage import DynamicMotionMagicVoltage
from .controls.dynamic_motion_magic_torque_current_foc import DynamicMotionMagicTorqueCurrentFOC
from .hardware.core.core_talon_fx import CoreTalonFX
from .hardware.core.core_cancoder import CoreCANcoder
from .hardware.core.core_pigeon2 import CorePigeon2
from .configs.talon_fx_configs import TalonFXConfiguration, TalonFXConfigurator
from .configs.cancoder_configs import CANcoderConfiguration, CANcoderConfigurator
from .configs.pigeon2_configs import Pigeon2Configuration, Pigeon2Configurator

__all__ = [
    StatusSignal,
    volt,
    ampere,
    rotation,
    rotations_per_second,
    rotations_per_second_squared,
    rotations_per_second_cubed,
    degree,
    degrees_per_second,
    celcius,
    microsecond,
    millisecond,
    second,
    microtesla,
    g,
    hertz,
    StatusCode,
    Timestamp,
    AllTimestamps,
    StatusCode,
    DutyCycleOut,
    TorqueCurrentFOC,
    VoltageOut,
    PositionDutyCycle,
    PositionVoltage,
    PositionTorqueCurrentFOC,
    VelocityDutyCycle,
    VelocityVoltage,
    VelocityTorqueCurrentFOC,
    MotionMagicDutyCycle,
    MotionMagicVoltage,
    MotionMagicTorqueCurrentFOC,
    DifferentialDutyCycle,
    DifferentialVoltage,
    DifferentialPositionDutyCycle,
    DifferentialPositionVoltage,
    DifferentialVelocityDutyCycle,
    DifferentialVelocityVoltage,
    DifferentialMotionMagicDutyCycle,
    DifferentialMotionMagicVoltage,
    Follower,
    StrictFollower,
    DifferentialFollower,
    DifferentialStrictFollower,
    NeutralOut,
    CoastOut,
    StaticBrake,
    MusicTone,
    MotionMagicVelocityDutyCycle,
    MotionMagicVelocityTorqueCurrentFOC,
    MotionMagicVelocityVoltage,
    DynamicMotionMagicDutyCycle,
    DynamicMotionMagicVoltage,
    DynamicMotionMagicTorqueCurrentFOC,
    CoreTalonFX,
    CoreCANcoder,
    CorePigeon2,
    TalonFXConfiguration,
    TalonFXConfigurator,
    CANcoderConfiguration,
    CANcoderConfigurator,
    Pigeon2Configuration,
    Pigeon2Configurator,
]

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.hardware.parent_device import ParentDevice, SupportsSendRequest
from phoenix6.spns.spn_value import SpnValue
from phoenix6.status_code import StatusCode
from phoenix6.status_signal import *
from phoenix6.sim.device_type import DeviceType
from phoenix6.configs.pigeon2_configs import Pigeon2Configurator

class CorePigeon2(ParentDevice):

    def __init__(self, device_id: int, canbus: str = ""):
        """
        Constructs a new Pigeon 2 sensor object.

        :param device_id: ID of the device, as configured in Phoenix Tuner.
        :type device_id: int
        :param canbus: Name of the CAN bus this device is on. Possible CAN bus strings are:
                          rio - The native roboRIO CAN bus
                          CANivore Name or Serial Number
                          SocketCAN interface - non-FRC Linux only
                          * - Any CANivore seen by the program
                          Empty String - Default for the system ("rio" for roboRIO, "can0" for linux, "*" for Windows)
        :type canbus: str, optional
        """
        super().__init__(device_id, "pigeon 2", canbus)
        self.__version = self.get_version()
        self.__reset_signal = self._common_lookup(SpnValue.STARTUP_RESET_FLAGS.value, 0, None, "ResetFlags", False, int)

        self.configurator = Pigeon2Configurator(self._device_identifier)
        Native.instance().c_ctre_phoenix6_platform_sim_create(DeviceType.PRO_Pigeon2Type.value, device_id)

    @property
    def has_reset_occurred(self) -> bool:
        """
        Check if the device has reset since the previous call to this routine

        :return: True if device has reset
        :rtype: bool
        """
        return self.__reset_signal.refresh(False).has_updated

    def _report_if_too_old(self):
        # If we're not initialized, we can't even check the versions
        pass

    def get_version_major(self) -> StatusSignal[int]:
        """
        App Major Version number.
        
          Minimum Value: 0
          Maximum Value: 255
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: VersionMajor Status Signal Object
        """
        return self._common_lookup(SpnValue.VERSION_MAJOR.value, 0, None, "version_major", False, int)
    
    def get_version_minor(self) -> StatusSignal[int]:
        """
        App Minor Version number.
        
          Minimum Value: 0
          Maximum Value: 255
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: VersionMinor Status Signal Object
        """
        return self._common_lookup(SpnValue.VERSION_MINOR.value, 0, None, "version_minor", False, int)
    
    def get_version_bugfix(self) -> StatusSignal[int]:
        """
        App Bugfix Version number.
        
          Minimum Value: 0
          Maximum Value: 255
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: VersionBugfix Status Signal Object
        """
        return self._common_lookup(SpnValue.VERSION_BUGFIX.value, 0, None, "version_bugfix", False, int)
    
    def get_version_build(self) -> StatusSignal[int]:
        """
        App Build Version number.
        
          Minimum Value: 0
          Maximum Value: 255
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: VersionBuild Status Signal Object
        """
        return self._common_lookup(SpnValue.VERSION_BUILD.value, 0, None, "version_build", False, int)
    
    def get_version(self) -> StatusSignal[int]:
        """
        Full Version.  The format is a four byte value.
        |
        Full Version of firmware in device. The format is a four byte value.
        
          Minimum Value: 0
          Maximum Value: 4294967295
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Version Status Signal Object
        """
        return self._common_lookup(SpnValue.VERSION_FULL.value, 0, None, "version", False, int)
    
    def get_fault_field(self) -> StatusSignal[int]:
        """
        Integer representing all faults
        |
        This returns the fault flags reported by the device. These are device
        specific and are not used directly in typical applications. Use the
        signal specific GetFault_*() methods instead.  
        
          Minimum Value: 0
          Maximum Value: 16777215
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: FaultField Status Signal Object
        """
        return self._common_lookup(SpnValue.ALL_FAULTS.value, 0, None, "fault_field", True, int)
    
    def get_sticky_fault_field(self) -> StatusSignal[int]:
        """
        Integer representing all sticky faults
        |
        This returns the persistent "sticky" fault flags reported by the
        device. These are device specific and are not used directly in typical
        applications. Use the signal specific GetStickyFault_*() methods
        instead.  
        
          Minimum Value: 0
          Maximum Value: 16777215
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFaultField Status Signal Object
        """
        return self._common_lookup(SpnValue.ALL_STICKY_FAULTS.value, 0, None, "sticky_fault_field", True, int)
    
    def get_yaw(self) -> StatusSignal[degree]:
        """
        Current reported yaw of the Pigeon2.
        
          Minimum Value: -368640.0
          Maximum Value: 368639.99725341797
          Default Value: 0
          Units: deg
        
        Default Rates:
          CAN: 100.0 Hz
        
         :returns: Yaw Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_YAW.value, 0, None, "yaw", True, degree)
    
    def get_pitch(self) -> StatusSignal[degree]:
        """
        Current reported pitch of the Pigeon2.
        
          Minimum Value: -90.0
          Maximum Value: 89.9560546875
          Default Value: 0
          Units: deg
        
        Default Rates:
          CAN: 100.0 Hz
        
         :returns: Pitch Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_PITCH.value, 0, None, "pitch", True, degree)
    
    def get_roll(self) -> StatusSignal[degree]:
        """
        Current reported roll of the Pigeon2.
        
          Minimum Value: -180.0
          Maximum Value: 179.9560546875
          Default Value: 0
          Units: deg
        
        Default Rates:
          CAN: 100.0 Hz
        
         :returns: Roll Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ROLL.value, 0, None, "roll", True, degree)
    
    def get_quat_w(self) -> StatusSignal[float]:
        """
        The W component of the reported Quaternion.
        
          Minimum Value: -1.0001220852154804
          Maximum Value: 1.0
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 50.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: QuatW Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATW.value, 0, None, "quat_w", True, float)
    
    def get_quat_x(self) -> StatusSignal[float]:
        """
        The X component of the reported Quaternion.
        
          Minimum Value: -1.0001220852154804
          Maximum Value: 1.0
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 50.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: QuatX Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATX.value, 0, None, "quat_x", True, float)
    
    def get_quat_y(self) -> StatusSignal[float]:
        """
        The Y component of the reported Quaternion.
        
          Minimum Value: -1.0001220852154804
          Maximum Value: 1.0
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 50.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: QuatY Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATY.value, 0, None, "quat_y", True, float)
    
    def get_quat_z(self) -> StatusSignal[float]:
        """
        The Z component of the reported Quaternion.
        
          Minimum Value: -1.0001220852154804
          Maximum Value: 1.0
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 50.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: QuatZ Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATZ.value, 0, None, "quat_z", True, float)
    
    def get_gravity_vector_x(self) -> StatusSignal[float]:
        """
        The X component of the gravity vector.
        |
        This is the X component of the reported gravity-vector. The gravity
        vector is not the acceleration experienced by the Pigeon2, rather it
        is where the Pigeon2 believes "Down" is. This can be used for
        mechanisms that are linearly related to gravity, such as an arm
        pivoting about a point, as the contribution of gravity to the arm is
        directly proportional to the contribution of gravity about one of
        these primary axis.
        
          Minimum Value: -1.000030518509476
          Maximum Value: 1.0
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: GravityVectorX Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_GRAVITY_VECTORX.value, 0, None, "gravity_vector_x", True, float)
    
    def get_gravity_vector_y(self) -> StatusSignal[float]:
        """
        The Y component of the gravity vector.
        |
        This is the X component of the reported gravity-vector. The gravity
        vector is not the acceleration experienced by the Pigeon2, rather it
        is where the Pigeon2 believes "Down" is. This can be used for
        mechanisms that are linearly related to gravity, such as an arm
        pivoting about a point, as the contribution of gravity to the arm is
        directly proportional to the contribution of gravity about one of
        these primary axis.
        
          Minimum Value: -1.000030518509476
          Maximum Value: 1.0
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: GravityVectorY Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_GRAVITY_VECTORY.value, 0, None, "gravity_vector_y", True, float)
    
    def get_gravity_vector_z(self) -> StatusSignal[float]:
        """
        The Z component of the gravity vector.
        |
        This is the Z component of the reported gravity-vector. The gravity
        vector is not the acceleration experienced by the Pigeon2, rather it
        is where the Pigeon2 believes "Down" is. This can be used for
        mechanisms that are linearly related to gravity, such as an arm
        pivoting about a point, as the contribution of gravity to the arm is
        directly proportional to the contribution of gravity about one of
        these primary axis.
        
          Minimum Value: -1.000030518509476
          Maximum Value: 1.0
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: GravityVectorZ Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_GRAVITY_VECTORZ.value, 0, None, "gravity_vector_z", True, float)
    
    def get_temperature(self) -> StatusSignal[celcius]:
        """
        Temperature of the Pigeon 2.
        
          Minimum Value: -128.0
          Maximum Value: 127.99609375
          Default Value: 0
          Units: ℃
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: Temperature Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_TEMPERATURE.value, 0, None, "temperature", True, celcius)
    
    def get_no_motion_enabled(self) -> StatusSignal[bool]:
        """
        Whether the no-motion calibration feature is enabled.
        
          Default Value: 0
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: NoMotionEnabled Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_NO_MOTION_CAL_ENABLED.value, 0, None, "no_motion_enabled", True, bool)
    
    def get_no_motion_count(self) -> StatusSignal[float]:
        """
        The number of times a no-motion event occurred, wraps at 15.
        
          Minimum Value: 0
          Maximum Value: 15
          Default Value: 0
          Units: 
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: NoMotionCount Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_NO_MOTION_COUNT.value, 0, None, "no_motion_count", True, float)
    
    def get_temperature_compensation_disabled(self) -> StatusSignal[bool]:
        """
        Whether the temperature-compensation feature is disabled.
        
          Default Value: 0
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: TemperatureCompensationDisabled Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_TEMP_COMP_DISABLED.value, 0, None, "temperature_compensation_disabled", True, bool)
    
    def get_up_time(self) -> StatusSignal[second]:
        """
        How long the Pigeon 2's been up in seconds, caps at 255 seconds.
        
          Minimum Value: 0
          Maximum Value: 255
          Default Value: 0
          Units: s
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: UpTime Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_UP_TIME.value, 0, None, "up_time", True, second)
    
    def get_accum_gyro_x(self) -> StatusSignal[degree]:
        """
        The accumulated gyro about the X axis without any sensor fusing.
        
          Minimum Value: -23040.0
          Maximum Value: 23039.9560546875
          Default Value: 0
          Units: deg
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AccumGyroX Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCUM_GYROX.value, 0, None, "accum_gyro_x", True, degree)
    
    def get_accum_gyro_y(self) -> StatusSignal[degree]:
        """
        The accumulated gyro about the Y axis without any sensor fusing.
        
          Minimum Value: -23040.0
          Maximum Value: 23039.9560546875
          Default Value: 0
          Units: deg
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AccumGyroY Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCUM_GYROY.value, 0, None, "accum_gyro_y", True, degree)
    
    def get_accum_gyro_z(self) -> StatusSignal[degree]:
        """
        The accumulated gyro about the Z axis without any sensor fusing.
        
          Minimum Value: -23040.0
          Maximum Value: 23039.9560546875
          Default Value: 0
          Units: deg
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AccumGyroZ Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCUM_GYROZ.value, 0, None, "accum_gyro_z", True, degree)
    
    def get_angular_velocity_x(self) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the X axis.
        
          Minimum Value: -1998.048780487805
          Maximum Value: 1997.987804878049
          Default Value: 0
          Units: dps
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AngularVelocityX Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITYX.value, 0, None, "angular_velocity_x", True, degrees_per_second)
    
    def get_angular_velocity_y(self) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the Y axis.
        
          Minimum Value: -1998.048780487805
          Maximum Value: 1997.987804878049
          Default Value: 0
          Units: dps
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AngularVelocityY Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITYY.value, 0, None, "angular_velocity_y", True, degrees_per_second)
    
    def get_angular_velocity_z(self) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the Z axis.
        
          Minimum Value: -1998.048780487805
          Maximum Value: 1997.987804878049
          Default Value: 0
          Units: dps
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AngularVelocityZ Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITYZ.value, 0, None, "angular_velocity_z", True, degrees_per_second)
    
    def get_acceleration_x(self) -> StatusSignal[g]:
        """
        The acceleration measured by Pigeon2 in the X direction.
        |
        This value includes the acceleration due to gravity. If this is
        undesirable, get the gravity vector and subtract out the contribution
        in this direction.
        
          Minimum Value: -2.0
          Maximum Value: 1.99993896484375
          Default Value: 0
          Units: g
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AccelerationX Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCELERATIONX.value, 0, None, "acceleration_x", True, g)
    
    def get_acceleration_y(self) -> StatusSignal[g]:
        """
        The acceleration measured by Pigeon2 in the Y direction.
        |
        This value includes the acceleration due to gravity. If this is
        undesirable, get the gravity vector and subtract out the contribution
        in this direction.
        
          Minimum Value: -2.0
          Maximum Value: 1.99993896484375
          Default Value: 0
          Units: g
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AccelerationY Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCELERATIONY.value, 0, None, "acceleration_y", True, g)
    
    def get_acceleration_z(self) -> StatusSignal[g]:
        """
        The acceleration measured by Pigeon2 in the Z direction.
        |
        This value includes the acceleration due to gravity. If this is
        undesirable, get the gravity vector and subtract out the contribution
        in this direction.
        
          Minimum Value: -2.0
          Maximum Value: 1.99993896484375
          Default Value: 0
          Units: g
        
        Default Rates:
          CAN 2.0: 10.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: AccelerationZ Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCELERATIONZ.value, 0, None, "acceleration_z", True, g)
    
    def get_supply_voltage(self) -> StatusSignal[volt]:
        """
        Measured supply voltage to the Pigeon2.
        
          Minimum Value: 0.0
          Maximum Value: 31.99951171875
          Default Value: 0
          Units: V
        
        Default Rates:
          CAN 2.0: 4.0 Hz
          CAN FD: 100.0 Hz
        
         :returns: SupplyVoltage Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_SUPPLY_VOLTAGE.value, 0, None, "supply_voltage", True, volt)
    
    def get_magnetic_field_x(self) -> StatusSignal[microtesla]:
        """
        The biased magnitude of the magnetic field measured by the Pigeon 2 in
        the X direction. This is only valid after performing a magnetometer
        calibration.
        
          Minimum Value: -19660.8
          Maximum Value: 19660.2
          Default Value: 0
          Units: uT
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: MagneticFieldX Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_MAGNETIC_FIELDX.value, 0, None, "magnetic_field_x", True, microtesla)
    
    def get_magnetic_field_y(self) -> StatusSignal[microtesla]:
        """
        The biased magnitude of the magnetic field measured by the Pigeon 2 in
        the Y direction. This is only valid after performing a magnetometer
        calibration.
        
          Minimum Value: -19660.8
          Maximum Value: 19660.2
          Default Value: 0
          Units: uT
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: MagneticFieldY Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_MAGNETIC_FIELDY.value, 0, None, "magnetic_field_y", True, microtesla)
    
    def get_magnetic_field_z(self) -> StatusSignal[microtesla]:
        """
        The biased magnitude of the magnetic field measured by the Pigeon 2 in
        the Z direction. This is only valid after performing a magnetometer
        calibration.
        
          Minimum Value: -19660.8
          Maximum Value: 19660.2
          Default Value: 0
          Units: uT
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: MagneticFieldZ Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_MAGNETIC_FIELDZ.value, 0, None, "magnetic_field_z", True, microtesla)
    
    def get_raw_magnetic_field_x(self) -> StatusSignal[microtesla]:
        """
        The raw magnitude of the magnetic field measured by the Pigeon 2 in
        the X direction. This is only valid after performing a magnetometer
        calibration.
        
          Minimum Value: -19660.8
          Maximum Value: 19660.2
          Default Value: 0
          Units: uT
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: RawMagneticFieldX Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_RAW_MAGNETIC_FIELDX.value, 0, None, "raw_magnetic_field_x", True, microtesla)
    
    def get_raw_magnetic_field_y(self) -> StatusSignal[microtesla]:
        """
        The raw magnitude of the magnetic field measured by the Pigeon 2 in
        the Y direction. This is only valid after performing a magnetometer
        calibration.
        
          Minimum Value: -19660.8
          Maximum Value: 19660.2
          Default Value: 0
          Units: uT
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: RawMagneticFieldY Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_RAW_MAGNETIC_FIELDY.value, 0, None, "raw_magnetic_field_y", True, microtesla)
    
    def get_raw_magnetic_field_z(self) -> StatusSignal[microtesla]:
        """
        The raw magnitude of the magnetic field measured by the Pigeon 2 in
        the Z direction. This is only valid after performing a magnetometer
        calibration.
        
          Minimum Value: -19660.8
          Maximum Value: 19660.2
          Default Value: 0
          Units: uT
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: RawMagneticFieldZ Status Signal Object
        """
        return self._common_lookup(SpnValue.PIGEON2_RAW_MAGNETIC_FIELDZ.value, 0, None, "raw_magnetic_field_z", True, microtesla)
    
    def get_is_pro_licensed(self) -> StatusSignal[bool]:
        """
        Whether the device is Phoenix Pro licensed.
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: IsProLicensed Status Signal Object
        """
        return self._common_lookup(SpnValue.VERSION_IS_PRO_LICENSED.value, 0, None, "is_pro_licensed", True, bool)
    
    def get_fault_hardware(self) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_Hardware Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_HARDWARE.value, 0, None, "fault_hardware", True, bool)
    
    def get_sticky_fault_hardware(self) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_Hardware Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_HARDWARE.value, 0, None, "sticky_fault_hardware", True, bool)
    
    def get_fault_undervoltage(self) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_Undervoltage Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_UNDERVOLTAGE.value, 0, None, "fault_undervoltage", True, bool)
    
    def get_sticky_fault_undervoltage(self) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_Undervoltage Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_UNDERVOLTAGE.value, 0, None, "sticky_fault_undervoltage", True, bool)
    
    def get_fault_boot_during_enable(self) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_BootDuringEnable Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_BOOT_DURING_ENABLE.value, 0, None, "fault_boot_during_enable", True, bool)
    
    def get_sticky_fault_boot_during_enable(self) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_BootDuringEnable Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_BOOT_DURING_ENABLE.value, 0, None, "sticky_fault_boot_during_enable", True, bool)
    
    def get_fault_unlicensed_feature_in_use(self) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_UnlicensedFeatureInUse Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_UNLICENSED_FEATURE_IN_USE.value, 0, None, "fault_unlicensed_feature_in_use", True, bool)
    
    def get_sticky_fault_unlicensed_feature_in_use(self) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_UnlicensedFeatureInUse Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_UNLICENSED_FEATURE_IN_USE.value, 0, None, "sticky_fault_unlicensed_feature_in_use", True, bool)
    
    def get_fault_bootup_accelerometer(self) -> StatusSignal[bool]:
        """
        Bootup checks failed: Accelerometer
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_BootupAccelerometer Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOTUP_ACCEL.value, 0, None, "fault_bootup_accelerometer", True, bool)
    
    def get_sticky_fault_bootup_accelerometer(self) -> StatusSignal[bool]:
        """
        Bootup checks failed: Accelerometer
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_BootupAccelerometer Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOTUP_ACCEL.value, 0, None, "sticky_fault_bootup_accelerometer", True, bool)
    
    def get_fault_bootup_gyroscope(self) -> StatusSignal[bool]:
        """
        Bootup checks failed: Gyroscope
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_BootupGyroscope Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOTUP_GYROS.value, 0, None, "fault_bootup_gyroscope", True, bool)
    
    def get_sticky_fault_bootup_gyroscope(self) -> StatusSignal[bool]:
        """
        Bootup checks failed: Gyroscope
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_BootupGyroscope Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOTUP_GYROS.value, 0, None, "sticky_fault_bootup_gyroscope", True, bool)
    
    def get_fault_bootup_magnetometer(self) -> StatusSignal[bool]:
        """
        Bootup checks failed: Magnetometer
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_BootupMagnetometer Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOTUP_MAGNE.value, 0, None, "fault_bootup_magnetometer", True, bool)
    
    def get_sticky_fault_bootup_magnetometer(self) -> StatusSignal[bool]:
        """
        Bootup checks failed: Magnetometer
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_BootupMagnetometer Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOTUP_MAGNE.value, 0, None, "sticky_fault_bootup_magnetometer", True, bool)
    
    def get_fault_boot_into_motion(self) -> StatusSignal[bool]:
        """
        Motion Detected during bootup.
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_BootIntoMotion Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOT_INTO_MOTION.value, 0, None, "fault_boot_into_motion", True, bool)
    
    def get_sticky_fault_boot_into_motion(self) -> StatusSignal[bool]:
        """
        Motion Detected during bootup.
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_BootIntoMotion Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOT_INTO_MOTION.value, 0, None, "sticky_fault_boot_into_motion", True, bool)
    
    def get_fault_data_acquired_late(self) -> StatusSignal[bool]:
        """
        Motion stack data acquisition was slower than expected
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_DataAcquiredLate Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_DATA_ACQUIRED_LATE.value, 0, None, "fault_data_acquired_late", True, bool)
    
    def get_sticky_fault_data_acquired_late(self) -> StatusSignal[bool]:
        """
        Motion stack data acquisition was slower than expected
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_DataAcquiredLate Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_DATA_ACQUIRED_LATE.value, 0, None, "sticky_fault_data_acquired_late", True, bool)
    
    def get_fault_loop_time_slow(self) -> StatusSignal[bool]:
        """
        Motion stack loop time was slower than expected.
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_LoopTimeSlow Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_LOOP_TIME_SLOW.value, 0, None, "fault_loop_time_slow", True, bool)
    
    def get_sticky_fault_loop_time_slow(self) -> StatusSignal[bool]:
        """
        Motion stack loop time was slower than expected.
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_LoopTimeSlow Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_LOOP_TIME_SLOW.value, 0, None, "sticky_fault_loop_time_slow", True, bool)
    
    def get_fault_saturated_magnetometer(self) -> StatusSignal[bool]:
        """
        Magnetometer values are saturated
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_SaturatedMagnetometer Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_SATURATED_MAGNE.value, 0, None, "fault_saturated_magnetometer", True, bool)
    
    def get_sticky_fault_saturated_magnetometer(self) -> StatusSignal[bool]:
        """
        Magnetometer values are saturated
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_SaturatedMagnetometer Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_SATURATED_MAGNE.value, 0, None, "sticky_fault_saturated_magnetometer", True, bool)
    
    def get_fault_saturated_accelometer(self) -> StatusSignal[bool]:
        """
        Accelerometer values are saturated
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_SaturatedAccelometer Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_SATURATED_ACCEL.value, 0, None, "fault_saturated_accelometer", True, bool)
    
    def get_sticky_fault_saturated_accelometer(self) -> StatusSignal[bool]:
        """
        Accelerometer values are saturated
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_SaturatedAccelometer Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_SATURATED_ACCEL.value, 0, None, "sticky_fault_saturated_accelometer", True, bool)
    
    def get_fault_saturated_gyroscope(self) -> StatusSignal[bool]:
        """
        Gyroscope values are saturated
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: Fault_SaturatedGyroscope Status Signal Object
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_SATURATED_GYROS.value, 0, None, "fault_saturated_gyroscope", True, bool)
    
    def get_sticky_fault_saturated_gyroscope(self) -> StatusSignal[bool]:
        """
        Gyroscope values are saturated
        
          Default Value: False
        
        Default Rates:
          CAN: 4.0 Hz
        
         :returns: StickyFault_SaturatedGyroscope Status Signal Object
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_SATURATED_GYROS.value, 0, None, "sticky_fault_saturated_gyroscope", True, bool)
    

    def set_control(self, request: SupportsSendRequest) -> StatusCode:
        """
        Control motor with generic control request object.

        If control request is not supported by device, this request
        will fail with StatusCode NotSupported

        :param request: Control object to request of the device
        :type request: SupportsSendRequest
        :return: StatusCode of the request
        :rtype: StatusCode
        """
        if isinstance(request, ()):
            return self._set_control_private(request)
        return StatusCode.NOT_SUPPORTED


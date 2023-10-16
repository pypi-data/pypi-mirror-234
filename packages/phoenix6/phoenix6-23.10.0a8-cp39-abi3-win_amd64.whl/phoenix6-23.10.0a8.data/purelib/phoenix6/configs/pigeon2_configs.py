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


class Pigeon2Configuration:
    """
    Class description for the Pigeon 2 IMU sensor that measures orientation.

    This handles the configurations for Pigeon2
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

        
        self.mount_pose: MountPoseConfigs = MountPoseConfigs()
        """
        Configs for Pigeon 2's Mount Pose configuration.
        |
        These configs allow the Pigeon2 to be mounted in whatever orientation
        that's desired and ensure the reported Yaw/Pitch/Roll is from the
        robot's reference.
        """
        
        
        self.gyro_trim: GyroTrimConfigs = GyroTrimConfigs()
        """
        Configs to trim the Pigeon2's gyroscope.
        |
        Pigeon2 allows the user to trim the gyroscope's sensitivity. While
        this isn't necessary for the Pigeon2, as it comes calibrated
        out-of-the-box, users can make use of this to make the Pigeon2 even
        more accurate for their application.
        """
        
        
        self.pigeon2_features: Pigeon2FeaturesConfigs = Pigeon2FeaturesConfigs()
        """
        Configs to enable/disable various features of the Pigeon2.
        |
        These configs allow the user to enable or disable various aspects of
        the Pigeon2.
        """
        

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :return: String representation of this object
        :rtype: str
        """
        ss = []
        ss.append(str(self.mount_pose))
        ss.append(str(self.gyro_trim))
        ss.append(str(self.pigeon2_features))
        return "\n".join(ss)


    def serialize(self) -> str:
        """
        Get the serialized form of this configuration

        :return: Serialized form of this config group
        :rtype: str
        """
        ss = []
        ss.append(self.mount_pose.serialize())
        ss.append(self.gyro_trim.serialize())
        ss.append(self.pigeon2_features.serialize())
        return "".join(ss)

    def deserialize(self, to_deserialize: str) -> StatusCode:
        """
        Take a string and deserialize it to this configuration

        :return: Return code of the deserialize method
        :rtype: str
        """
        err: StatusCode = StatusCode.OK
        err = self.mount_pose.deserialize(to_deserialize)
        err = self.gyro_trim.deserialize(to_deserialize)
        err = self.pigeon2_features.deserialize(to_deserialize)
        return err



class Pigeon2Configurator(ParentConfigurator):
    """
 * Class description for the Pigeon 2 IMU sensor that measures orientation.

    This handles the configurations for Pigeon2
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

    
    
    
    
    
    
    
    
    
    
    
    
    
    


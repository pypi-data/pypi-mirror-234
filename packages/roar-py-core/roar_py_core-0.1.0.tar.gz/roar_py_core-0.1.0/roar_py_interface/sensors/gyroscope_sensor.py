from ..base import RoarPySensor, RoarPyRemoteSupportedSensorData
from ..base.sensor import remote_support_sensor_data_register
from serde import serde
from dataclasses import dataclass
import numpy as np
import gymnasium as gym

@remote_support_sensor_data_register
@serde
@dataclass
class RoarPyGyroscopeSensorData(RoarPyRemoteSupportedSensorData):
    # angular velocity (x,y,z local axis) in rad/s
    angular_velocity: np.ndarray #np.NDArray[np.float32]

    def get_gym_observation_spec(self) -> gym.Space:
        return gym.spaces.Box(
            low =-np.inf,
            high=np.inf,
            shape=(3,),
            dtype=np.float32
        )

    def convert_obs_to_gym_obs(self):
        return self.angular_velocity

class RoarPyGyroscopeSensor(RoarPySensor[RoarPyGyroscopeSensorData]):
    sensordata_type = RoarPyGyroscopeSensorData
    def __init__(
        self, 
        name: str,
        control_timestep: float,
    ):
        super().__init__(name, control_timestep)

    def get_gym_observation_spec(self) -> gym.Space:
        return gym.spaces.Box(
            low =-np.inf,
            high=np.inf,
            shape=(3,),
            dtype=np.float32
        )
    
    def convert_obs_to_gym_obs(self, obs: RoarPyGyroscopeSensorData):
        return obs.convert_obs_to_gym_obs()

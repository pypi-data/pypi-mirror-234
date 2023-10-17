import copy
from typing import Dict, Optional

import numpy as np
import rclpy  # pants: no-infer-dep
from geometry_msgs.msg import Transform  # pants: no-infer-dep
from geometry_msgs.msg import TransformStamped  # pants: no-infer-dep
from pyquaternion import Quaternion


class TFPair:
    def __init__(
        self, source_frame: str, target_frame: str, angular_thres=0.0, trans_thres=0.0, max_publish_period=1.0
    ) -> None:
        self.is_ok = True
        self._source_frame = source_frame
        self._target_frame = target_frame
        self._angular_thres = angular_thres
        self._trans_thres = trans_thres
        self._max_publish_period = max_publish_period

        self._tf_transmitted = {"translation": np.array([0.0, 0.0, 0.0]), "rotation": Quaternion(1.0, 0.0, 0.0, 0.0)}
        self._tf_received = {"translation": np.array([0.0, 0.0, 0.0]), "rotation": Quaternion(1.0, 0.0, 0.0, 0.0)}

        self._last_tf_msg = Transform()
        self._last_publish_time: Optional[rclpy.time.Time] = None

        self.first_transmission = True
        self._updated = False

    @property
    def id(self) -> str:
        return self._source_frame + "-" + self._target_frame

    @property
    def source_frame(self) -> str:
        return self._source_frame

    @source_frame.setter
    def source_frame(self, value: str) -> None:
        self._source_frame = value
        self._updated = True

    @property
    def target_frame(self) -> str:
        return self._target_frame

    @target_frame.setter
    def target_frame(self, value: str) -> None:
        self._target_frame = value
        self._updated = True

    @property
    def angular_thres(self) -> float:
        assert isinstance(self._angular_thres, float)
        return self._angular_thres

    @angular_thres.setter
    def angular_thres(self, value: float) -> None:
        self._angular_thres = value
        self._updated = True

    @property
    def trans_thres(self) -> float:
        assert isinstance(self._trans_thres, float)
        return self._trans_thres

    @trans_thres.setter
    def trans_thres(self, value: float) -> None:
        self._trans_thres = value
        self._updated = True

    @property
    def last_tf_msg(self) -> Transform:
        return self._last_tf_msg

    def transmission_triggered(self, current_time: rclpy.time.Time) -> None:
        self._tf_transmitted = copy.deepcopy(self._tf_received)
        self._last_publish_time = current_time

    def update_transform(self, update: TransformStamped) -> None:
        self._tf_received["translation"] = np.array(
            [update.transform.translation.x, update.transform.translation.y, update.transform.translation.z]
        )
        self._tf_received["rotation"] = Quaternion(
            update.transform.rotation.w,
            update.transform.rotation.x,
            update.transform.rotation.y,
            update.transform.rotation.z,
        )
        self._last_tf_msg = update.transform
        self._updated = True

    def update_needed(self, current_time: rclpy.time.Time) -> bool:
        result = False
        if self._updated:
            if self._trans_thres and (self.distance(self._tf_transmitted, self._tf_received) > self._trans_thres):
                result = True
                self.first_transmission = False
            elif self._angular_thres and (self.angle(self._tf_transmitted, self._tf_received) > self._angular_thres):
                result = True
                self.first_transmission = False
            elif self._max_publish_period and (
                self._last_publish_time is None
                or (current_time - self._last_publish_time > rclpy.duration.Duration(seconds=self._max_publish_period))
            ):
                result = True
                self.first_transmission = False
            elif self.first_transmission:
                result = True
                self.first_transmission = False

        self._updated = False
        return result

    @staticmethod
    def distance(tf1: Dict, tf2: Dict) -> float:
        return np.linalg.norm(tf1["translation"] - tf2["translation"])  # type: ignore

    @staticmethod
    def angle(tf1: Dict, tf2: Dict) -> float:
        ret = Quaternion.absolute_distance(tf1["rotation"], tf2["rotation"])
        assert isinstance(ret, float)
        return ret

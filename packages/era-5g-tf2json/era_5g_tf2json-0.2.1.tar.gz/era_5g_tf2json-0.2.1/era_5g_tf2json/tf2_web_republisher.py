from typing import Callable, List

import rclpy  # pants: no-infer-dep
from geometry_msgs.msg import TransformStamped  # pants: no-infer-dep
from rclpy.node import Node  # pants: no-infer-dep
from tf2_ros import TransformListener  # pants: no-infer-dep
from tf2_ros import Buffer, TransformException  # pants: no-infer-dep

from era_5g_tf2json.tf_pair import TFPair


class TFRepublisher:
    def __init__(self, node: Node, callback: Callable[[List[TransformStamped]], None], rate: float = 10.0):

        self._node = node
        self._tf_buffer = Buffer()
        self._tf_listener = TransformListener(self._tf_buffer, node=node)
        self._timer = self._node.create_timer(1.0 / rate, lambda: self._process())
        self._tf_pairs: List[TFPair] = []
        self._callback = callback

    def subscribe_transform(
        self,
        source_frame: str,
        target_frame: str,
        angular_thres: float,
        trans_thres: float,
        max_publish_period: float = 0.0,
    ) -> None:

        self._tf_pairs.append(
            TFPair(
                self._clean_tf_frame(source_frame),
                self._clean_tf_frame(target_frame),
                angular_thres,
                trans_thres,
                max_publish_period,
            )
        )

    @staticmethod
    def _clean_tf_frame(frame_id: str) -> str:
        # if frame_id[0] != '/':
        #    frame_id = '/'+frame_id
        return frame_id

    def _process(self) -> None:

        transforms: TransformStamped = []

        current_time = self._node.get_clock().now()

        # iterate over tf_subscription vector
        for pair in self._tf_pairs:
            try:
                # lookup transformation for tf_pair
                transform = self._tf_buffer.lookup_transform(pair.target_frame, pair.source_frame, rclpy.time.Time())
                # If the transform broke earlier, but worked now (we didn't get
                # booted into the catch block), tell the user all is well again
                if not pair.is_ok:
                    self._node.get_logger().info(
                        "Transform from {0} to {1} is working again".format(pair.source_frame, pair.target_frame)
                    )
                    pair.is_ok = True
                # update tf_pair with transformtion
                pair.update_transform(transform)

            except TransformException as e:
                if pair.is_ok:
                    # Only log an error if the transform was okay before
                    self._node.get_logger().warning(str(e))
                pair.is_ok = False

            # check angular and translational thresholds
            if pair.update_needed(current_time):
                transform_msg = TransformStamped()
                transform_msg.header.stamp = current_time.to_msg()
                transform_msg.header.frame_id = pair.target_frame
                transform_msg.child_frame_id = pair.source_frame
                transform_msg.transform = pair.last_tf_msg
                pair.transmission_triggered(current_time)
                transforms.append(transform_msg)

        if transforms:
            self._callback(transforms)

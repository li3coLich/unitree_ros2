import rclpy
from rclpy.node import Node
from unitree_go.msg import LowCmd
from unitree_go.msg import LowState
import numpy as np

from unitree_sdk2py.idl.default import unitree_go_msg_dds__LowCmd_
from unitree_sdk2py.utils.crc import CRC

class LowStateSubscriper(Node):
    def __init__(self):
        super().__init__('lowstate_subscriber')
        self.subscription = self.create_subscription(
            LowState,            # Message type
            '/lowstate',         # Topic name
            self.listener_callback,  # Callback function
            10                 # Queue size
        )

        self.publisher_ = self.create_publisher(LowState, '/lowstate_gt', 10)

        self.motor_state_dtype = np.dtype([
            ('mode', np.uint8),
            ('q', np.float32),
            ('dq', np.float32),
            ('tau', np.float32),
            ('kp', np.float32),
            ('kd', np.float32),
            ('reserve', np.uint32, (3,))  # 3-element array of uint32
        ])

        self.num_motors = 12
        self.motor_cmd = np.zeros(self.num_motors, dtype=self.motor_state_dtype)

        self.low_cmd = unitree_go_msg_dds__LowCmd_()
        self.crc = CRC()

    def listener_callback(self, msg):
        # lowstate_gt = LowState
        # lowstate_gt = msg
        self.publisher_.publish(msg)

        
def main(args=None):
    rclpy.init(args=args)
    node = LowStateSubscriper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

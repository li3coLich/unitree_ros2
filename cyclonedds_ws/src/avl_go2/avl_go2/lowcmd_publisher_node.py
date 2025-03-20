import rclpy
from rclpy.node import Node
from unitree_go.msg import LowCmd
import numpy as np

from unitree_sdk2py.idl.default import unitree_go_msg_dds__LowCmd_
from unitree_sdk2py.utils.crc import CRC

class LowCmdPublisher(Node):
    def __init__(self):
        super().__init__('lowcmd_subscriber')
        self.subscription = self.create_subscription(
            LowCmd,            # Message type
            '/lowcmd',         # Topic name
            self.listener_callback,  # Callback function
            10                 # Queue size
        )

        self.publisher_ = self.create_publisher(LowCmd, '/lowcmd', 10)

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

        # self.low_cmd.head[0] = 254
        # self.low_cmd.head[1] = 239
        # self.low_cmd.level_flag = 255
        # # print(msg.motor_cmd[0].reserve)
        # for i in range(self.num_motors):
        #     # self.motor_cmd[i] = (msg.motor_cmd[i].mode, msg.motor_cmd[i].q, msg.motor_cmd[i].dq,
        #     #                      msg.motor_cmd[i].tau, msg.motor_cmd[i].kp, msg.motor_cmd[i].kd, msg.motor_cmd[i].reserve)
        #     self.low_cmd.motor_cmd[i].mode = msg.motor_cmd[i].mode
        #     self.low_cmd.motor_cmd[i].q = msg.motor_cmd[i].q
        #     self.low_cmd.motor_cmd[i].dq = msg.motor_cmd[i].dq
        #     self.low_cmd.motor_cmd[i].tau = msg.motor_cmd[i].tau
        #     self.low_cmd.motor_cmd[i].kp = msg.motor_cmd[i].kp
        #     self.low_cmd.motor_cmd[i].kd = msg.motor_cmd[i].kd
        #     self.low_cmd.motor_cmd[i].reserve = msg.motor_cmd[i].reserve

        # self.low_cmd.crc = self.crc.Crc(self.low_cmd)
        # print(self.low_cmd.crc, msg.crc)
        
def main(args=None):
    rclpy.init(args=args)
    node = LowCmdPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

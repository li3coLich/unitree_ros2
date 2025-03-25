import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from unitree_go.msg import SportModeCmd

import numpy as np


class HighCmdPublisher(Node):
    def __init__(self):
        super().__init__('highcmd_publisher')
        self.declare_parameter("publish_rate", 10.0)

        self.cmd_subscription = self.create_subscription(
            Twist,
            '/cmd_vel_go2',
            self.cmd_listener_callback,
            10
        )
        self.vx = 0.0
        self.vy = 0.0
        self.wyaw = 0.0

        self.highcmd_publisher_ = self.create_publisher(SportModeCmd, '/sportmodecmd', 10)
        rate = 1 / self.get_parameter("publish_rate").value
        self.create_timer(rate, self.highcmd_publisher_callback)
    
    def cmd_listener_callback(self, msg):
        self.vx = msg.linear.x
        self.vy = msg.linear.y
        self.wyaw = msg.angular.z
        self.get_logger().info(f"Linear x: {msg.linear.x}, Linear y: {msg.linear.y}, Angular z: {msg.angular.z}")

    def highcmd_publisher_callback(self):
        go2_cmd = SportModeCmd()
        go2_cmd.mode = 0
        go2_cmd.gait_type = 1
        go2_cmd.speed_level = 0
        go2_cmd.foot_raise_height = 0.0
        go2_cmd.body_height = 0.0
        go2_cmd.position[0] = 0.0
        go2_cmd.position[1] = 0.0
        go2_cmd.euler[0] = 0.0
        go2_cmd.euler[1] = 0.0
        go2_cmd.euler[2] = 0.0
        go2_cmd.velocity[0] = 0.0
        go2_cmd.velocity[1] = 0.0
        go2_cmd.yaw_speed = 0.0


def main(args=None):
    rclpy.init(args=args)
    node = HighCmdPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

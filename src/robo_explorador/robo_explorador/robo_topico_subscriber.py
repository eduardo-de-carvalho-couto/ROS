#!/usr/bin/env python3
# Q4 - Estação base: lê o tópico "monitoramento" e classifica o ambiente como Safe / Not Safe.
import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from robo_interfaces.msg import Monitoramento


class RoboTopicoSubscriber(Node):

    def __init__(self):
        super().__init__('robo_topico_subscriber')
        self.subscription = self.create_subscription(
            Monitoramento, 'monitoramento', self.receber, 10)
        self.get_logger().info('Estação base ouvindo o tópico "monitoramento"')

    def receber(self, msg):
        if 10 <= msg.temperatura <= 40 and msg.oxigenio > 80:
            status = 'Safe'
        else:
            status = 'Not Safe'
        self.get_logger().info(
            f'oxigenio={msg.oxigenio:.2f} temperatura={msg.temperatura:.2f} -> {status}')


def main(args=None):
    rclpy.init(args=args)
    node = RoboTopicoSubscriber()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()

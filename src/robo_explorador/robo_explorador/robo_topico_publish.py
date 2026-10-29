#!/usr/bin/env python3
# Q3 - Nó do robô: publica nível de oxigênio e temperatura no tópico "monitoramento".
import random

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from robo_interfaces.msg import Monitoramento


class RoboTopicoPublish(Node):

    def __init__(self):
        super().__init__('robo_topico_publish')
        self.publisher_ = self.create_publisher(Monitoramento, 'monitoramento', 10)
        self.timer = self.create_timer(1.0, self.publicar)
        self.get_logger().info('Robô publicando no tópico "monitoramento"')

    def publicar(self):
        msg = Monitoramento()
        msg.oxigenio = random.uniform(1, 100)
        msg.temperatura = random.uniform(1, 100)
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publicado: oxigenio={msg.oxigenio:.2f} temperatura={msg.temperatura:.2f}')


def main(args=None):
    rclpy.init(args=args)
    node = RoboTopicoPublish()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()

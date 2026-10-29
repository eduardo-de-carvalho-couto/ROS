#!/usr/bin/env python3
# Q7 - Robô: servidor do serviço "coleta_material" (sucesso com 70% de probabilidade).
import random

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from robo_interfaces.srv import ColetaAmostra


class RoboColetaServidor(Node):

    def __init__(self):
        super().__init__('robo_coleta_servidor')
        self.server = self.create_service(ColetaAmostra, 'coleta_material', self.coletar)
        self.get_logger().info('Serviço "coleta_material" disponível')

    def coletar(self, request, response):
        sorteio = random.random()
        response.sucesso = sorteio <= 0.7
        self.get_logger().info(
            f'Coleta a {request.profundidade:.2f} de profundidade: '
            f'sorteio={sorteio:.2f} -> sucesso={response.sucesso}')
        return response


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaServidor()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()

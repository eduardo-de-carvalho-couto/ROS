#!/usr/bin/env python3
# Q6 - Estação base: cliente do serviço "coleta_material" com profundidade aleatória (0,1 a 0,5).
import random

import rclpy
from rclpy.node import Node

from robo_interfaces.srv import ColetaAmostra


class RoboColetaCliente(Node):

    def __init__(self):
        super().__init__('robo_coleta_cliente')
        self.client = self.create_client(ColetaAmostra, 'coleta_material')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando o serviço "coleta_material"...')

    def solicitar_coleta(self):
        request = ColetaAmostra.Request()
        request.profundidade = random.uniform(0.1, 0.5)
        self.get_logger().info(f'Solicitando coleta a {request.profundidade:.2f} de profundidade')
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    node = RoboColetaCliente()
    response = node.solicitar_coleta()
    if response.sucesso:
        node.get_logger().info('Coleta bem sucedida')
    else:
        node.get_logger().info('Coleta não foi bem sucedida')
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()

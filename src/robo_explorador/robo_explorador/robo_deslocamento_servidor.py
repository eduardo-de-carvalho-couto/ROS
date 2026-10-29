#!/usr/bin/env python3
# Q9 - Robô: servidor da action "deslocamento".
# Aceita a meta se o destino for diferente da posição atual, anda a cada 1 s
# conforme as velocidades, publica a posição como feedback e retorna a distância percorrida.
import math
import time

import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node

from robo_interfaces.action import Deslocamento


def avancar(atual, destino, velocidade):
    """Anda no máximo `velocidade` unidades em direção ao destino, sem ultrapassá-lo."""
    restante = destino - atual
    if abs(restante) <= abs(velocidade):
        return destino
    return atual + math.copysign(abs(velocidade), restante)


class RoboDeslocamentoServidor(Node):

    def __init__(self):
        super().__init__('robo_deslocamento_servidor')
        self.latitude = 0.0
        self.longitude = 0.0
        self.action_server = ActionServer(
            self,
            Deslocamento,
            'deslocamento',
            execute_callback=self.executar,
            goal_callback=self.avaliar_meta,
            cancel_callback=self.avaliar_cancelamento,
            callback_group=ReentrantCallbackGroup())
        self.get_logger().info(
            f'Action "deslocamento" disponível. Posição atual: '
            f'({self.latitude:.2f}, {self.longitude:.2f})')

    def avaliar_meta(self, goal):
        if goal.latitude == self.latitude and goal.longitude == self.longitude:
            self.get_logger().warn('Meta rejeitada: destino igual à posição atual')
            return GoalResponse.REJECT
        if (goal.latitude != self.latitude and goal.velocidade_latitude == 0) or \
                (goal.longitude != self.longitude and goal.velocidade_longitude == 0):
            self.get_logger().warn('Meta rejeitada: velocidade zero em um eixo com deslocamento')
            return GoalResponse.REJECT
        self.get_logger().info(
            f'Meta aceita: ir para ({goal.latitude:.2f}, {goal.longitude:.2f})')
        return GoalResponse.ACCEPT

    def avaliar_cancelamento(self, goal_handle):
        self.get_logger().info('Pedido de cancelamento recebido')
        return CancelResponse.ACCEPT

    def executar(self, goal_handle):
        meta = goal_handle.request
        feedback = Deslocamento.Feedback()
        result = Deslocamento.Result()
        distancia = 0.0

        while (self.latitude, self.longitude) != (meta.latitude, meta.longitude):
            time.sleep(1.0)

            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.distancia_percorrida = distancia
                self.get_logger().info(
                    f'Deslocamento cancelado. Distância percorrida: {distancia:.2f}')
                return result

            nova_lat = avancar(self.latitude, meta.latitude, meta.velocidade_latitude)
            nova_lon = avancar(self.longitude, meta.longitude, meta.velocidade_longitude)
            distancia += math.hypot(nova_lat - self.latitude, nova_lon - self.longitude)
            self.latitude, self.longitude = nova_lat, nova_lon

            feedback.latitude_atual = self.latitude
            feedback.longitude_atual = self.longitude
            goal_handle.publish_feedback(feedback)
            self.get_logger().info(
                f'Posição atual: ({self.latitude:.2f}, {self.longitude:.2f})')

        goal_handle.succeed()
        result.distancia_percorrida = distancia
        self.get_logger().info(f'Destino alcançado. Distância percorrida: {distancia:.2f}')
        return result


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoServidor()
    try:
        rclpy.spin(node, executor=MultiThreadedExecutor())
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()

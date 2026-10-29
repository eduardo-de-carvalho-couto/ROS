#!/usr/bin/env python3
# Q10 - Cliente da action "deslocamento": envia a meta e espera até o final.
# Uso: ros2 run robo_explorador robo_deslocamento_cliente [lat lon vel_lat vel_lon]
import sys

import rclpy
from action_msgs.msg import GoalStatus
from rclpy.action import ActionClient
from rclpy.node import Node
from rclpy.utilities import remove_ros_args

from robo_interfaces.action import Deslocamento


class RoboDeslocamentoCliente(Node):

    def __init__(self, nome='robo_deslocamento_cliente'):
        super().__init__(nome)
        self.client = ActionClient(self, Deslocamento, 'deslocamento')
        self.goal_handle = None
        self.terminou = False

    def enviar_meta(self, latitude, longitude, vel_latitude, vel_longitude):
        self.client.wait_for_server()
        goal = Deslocamento.Goal()
        goal.latitude = latitude
        goal.longitude = longitude
        goal.velocidade_latitude = vel_latitude
        goal.velocidade_longitude = vel_longitude
        self.get_logger().info(
            f'Enviando meta: ({latitude:.2f}, {longitude:.2f}) '
            f'com velocidades ({vel_latitude:.2f}, {vel_longitude:.2f}) u/s')
        future = self.client.send_goal_async(goal, feedback_callback=self.ao_receber_feedback)
        future.add_done_callback(self.ao_responder_meta)

    def ao_responder_meta(self, future):
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().warn('Meta rejeitada pelo robô')
            self.terminou = True
            return
        self.get_logger().info('Meta aceita pelo robô')
        self.goal_handle.get_result_async().add_done_callback(self.ao_receber_resultado)

    def ao_receber_feedback(self, msg):
        fb = msg.feedback
        self.get_logger().info(
            f'Feedback - posição atual: ({fb.latitude_atual:.2f}, {fb.longitude_atual:.2f})')

    def ao_receber_resultado(self, future):
        resposta = future.result()
        distancia = resposta.result.distancia_percorrida
        if resposta.status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info(f'Deslocamento concluído. Distância percorrida: {distancia:.2f}')
        elif resposta.status == GoalStatus.STATUS_CANCELED:
            self.get_logger().info(f'Deslocamento cancelado. Distância percorrida: {distancia:.2f}')
        else:
            self.get_logger().warn(f'Deslocamento terminou com status {resposta.status}')
        self.terminou = True


def ler_meta(padrao):
    valores = remove_ros_args(sys.argv)[1:]
    if len(valores) == 4:
        return [float(v) for v in valores]
    return padrao


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoCliente()
    node.enviar_meta(*ler_meta([10.0, 5.0, 1.0, 1.0]))
    while rclpy.ok() and not node.terminou:
        rclpy.spin_once(node)
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()

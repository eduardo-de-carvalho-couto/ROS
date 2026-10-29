#!/usr/bin/env python3
# Q11 - Cliente da action "deslocamento": envia a meta e cancela após 5 segundos.
# Uso: ros2 run robo_explorador robo_deslocamento_cancela [lat lon vel_lat vel_lon]
import rclpy

from robo_explorador.robo_deslocamento_cliente import RoboDeslocamentoCliente, ler_meta

TEMPO_ATE_CANCELAR = 5.0


class RoboDeslocamentoCancela(RoboDeslocamentoCliente):

    def __init__(self):
        super().__init__('robo_deslocamento_cancela')
        self.timer_cancelamento = None

    def ao_responder_meta(self, future):
        super().ao_responder_meta(future)
        if self.goal_handle.accepted:
            self.timer_cancelamento = self.create_timer(TEMPO_ATE_CANCELAR, self.cancelar)

    def cancelar(self):
        self.timer_cancelamento.cancel()
        self.get_logger().info(f'{TEMPO_ATE_CANCELAR:.0f} segundos se passaram: cancelando a ação')
        self.goal_handle.cancel_goal_async()


def main(args=None):
    rclpy.init(args=args)
    node = RoboDeslocamentoCancela()
    node.enviar_meta(*ler_meta([-10.0, -5.0, 1.0, 1.0]))
    while rclpy.ok() and not node.terminou:
        rclpy.spin_once(node)
    node.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()

# ROS 2 — Robô Explorador

1ª Avaliação Prática da disciplina **Tópicos Especiais em Redes de Computadores** (UERN — 2026.2).

Simulação de um robô móvel em ambiente insalubre usando **ROS 2 Jazzy**:

- **Tópico** — o robô publica nível de oxigênio e temperatura; a estação base classifica o ambiente como `Safe` / `Not Safe`.
- **Serviço** — a estação base solicita a coleta de solo a uma profundidade; o robô responde se a coleta foi bem sucedida (70% de chance).
- **Action** — o robô se desloca até uma latitude/longitude, enviando a posição atual como feedback a cada segundo e a distância percorrida como resultado; a ação pode ser cancelada.

## Estrutura

```
.
├── Dockerfile                 # ambiente ROS 2 Jazzy (Ubuntu 24.04)
├── run_lab.sh                 # sobe o container montando este repositório em ~/ros2_ws
└── src/
    ├── robo_interfaces/       # ament_cmake — definição das interfaces
    │   ├── msg/Monitoramento.msg
    │   ├── srv/ColetaAmostra.srv
    │   └── action/Deslocamento.action
    └── robo_explorador/       # ament_python — nós
        └── robo_explorador/
            ├── robo_topico_publish.py         # Q3
            ├── robo_topico_subscriber.py      # Q4
            ├── robo_coleta_cliente.py         # Q6
            ├── robo_coleta_servidor.py        # Q7
            ├── robo_deslocamento_servidor.py  # Q9
            ├── robo_deslocamento_cliente.py   # Q10
            └── robo_deslocamento_cancela.py   # Q11
```

## Interfaces

| Tipo | Nome | Definição |
|---|---|---|
| Tópico (`monitoramento`) | `robo_interfaces/msg/Monitoramento` | `float64 oxigenio`, `float64 temperatura` |
| Serviço (`coleta_material`) | `robo_interfaces/srv/ColetaAmostra` | Request: `float64 profundidade` · Response: `bool sucesso` |
| Action (`deslocamento`) | `robo_interfaces/action/Deslocamento` | Goal: `latitude`, `longitude`, `velocidade_latitude`, `velocidade_longitude` · Result: `distancia_percorrida` · Feedback: `latitude_atual`, `longitude_atual` (todos `float64`) |

## Ambiente

Requer Docker. Na raiz do repositório:

```bash
./run_lab.sh
```

O script constrói a imagem `ros2-jazzy-lab` (se ainda não existir) e abre um shell no container, com este repositório montado em `/home/aluno/ros2_ws`. Para abrir outro terminal no mesmo container, rode `./run_lab.sh` novamente.

> **Linux + imagem carregada de `.tar`:** se aparecer `Permission denied` ao criar arquivos dentro de
> `~/ros2_ws`, o usuário `aluno` da imagem não tem o mesmo UID do seu usuário no host (`id -u`).
> Construir a imagem a partir deste `Dockerfile` cria o `aluno` com UID 1000.

## Compilação

Dentro do container:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash
```

Verificação:

```bash
ros2 pkg executables robo_explorador
ros2 interface show robo_interfaces/msg/Monitoramento
ros2 interface show robo_interfaces/srv/ColetaAmostra
ros2 interface show robo_interfaces/action/Deslocamento
```

## Execução

Cada par pode rodar em dois terminais (`./run_lab.sh` em cada um) ou no mesmo terminal, com o primeiro nó em segundo plano.

### Tópico — Q3 e Q4

```bash
ros2 run robo_explorador robo_topico_publish      # terminal 1
ros2 run robo_explorador robo_topico_subscriber   # terminal 2
```

`Safe` quando `10 <= temperatura <= 40` e `oxigenio > 80`; `Not Safe` caso contrário.

### Serviço — Q6 e Q7

```bash
ros2 run robo_explorador robo_coleta_servidor     # terminal 1
ros2 run robo_explorador robo_coleta_cliente      # terminal 2 (pode repetir)
```

O cliente sorteia uma profundidade entre 0,1 e 0,5; o servidor responde `sucesso = true` quando um número aleatório entre 0 e 1 é ≤ 0,7.

### Action — Q9, Q10 e Q11

```bash
ros2 run robo_explorador robo_deslocamento_servidor   # terminal 1

ros2 run robo_explorador robo_deslocamento_cliente    # terminal 2 — espera até o fim
ros2 run robo_explorador robo_deslocamento_cancela    # terminal 2 — cancela após 5 s
```

- O robô começa em `(0, 0)` e mantém a posição entre metas.
- A meta é **rejeitada** se o destino for igual à posição atual (ou se a velocidade for zero num eixo que precisa se mover).
- A cada 1 s o robô avança até `velocidade` unidades em cada eixo, publica a posição como feedback e acumula a distância percorrida.
- Metas padrão: cliente → `(10, 5)`; cancela → `(-10, -5)`, ambas com velocidades `(1, 1)` u/s. Outra meta pode ser passada como argumento:

```bash
ros2 run robo_explorador robo_deslocamento_cliente 3 2 0.5 0.5   # lat lon vel_lat vel_lon
```

Também é possível enviar a meta pela CLI:

```bash
ros2 action send_goal --feedback /deslocamento robo_interfaces/action/Deslocamento \
  "{latitude: 5.0, longitude: 3.0, velocidade_latitude: 1.0, velocidade_longitude: 1.0}"
```

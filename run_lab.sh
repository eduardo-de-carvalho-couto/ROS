#!/bin/bash
# ==============================================================================
# Script de Inicialização do Container ROS 2 Jazzy (Linux / macOS)
# ==============================================================================

IMAGE_NAME="ros2-jazzy-lab"
CONTAINER_NAME="ros2_jazzy_container"
WORKSPACE_HOST="$(cd "$(dirname "$0")" && pwd)"

mkdir -p "${WORKSPACE_HOST}/src"

echo "=========================================================="
echo "🚀 Verificando/Construindo Imagem Docker: ${IMAGE_NAME}..."
echo "=========================================================="

if [[ "$(docker images -q ${IMAGE_NAME} 2> /dev/null)" == "" ]]; then
    echo "📌 Imagem não encontrada. Construindo imagem ROS 2 Jazzy..."
    docker build -t ${IMAGE_NAME} .
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao construir a imagem Docker."
        exit 1
    fi
fi

echo "🖥️ Configurando acesso X11 e permissões de GPU..."
xhost +local:root > /dev/null 2>&1 || xhost + > /dev/null 2>&1

# Ajusta permissões dos nós da GPU no hospedeiro para evitar avisos libEGL
if [ -d "/dev/dri" ]; then
    sudo chmod 666 /dev/dri/* 2>/dev/null || true
fi

if [ $(docker ps -q -f name=^/${CONTAINER_NAME}$) ]; then
    echo "🔄 Container já ativo. Conectando novo terminal..."
    docker exec -it ${CONTAINER_NAME} bash
    exit 0
fi

if [ $(docker ps -a -q -f name=^/${CONTAINER_NAME}$) ]; then
    echo "▶️ Iniciando container existente..."
    docker start ${CONTAINER_NAME}
    docker exec -it ${CONTAINER_NAME} bash
    exit 0
fi

docker run -it \
    --name ${CONTAINER_NAME} \
    --net=host \
    --ipc=host \
    --privileged \
    --device=/dev/dri:/dev/dri \
    --group-add video \
    --group-add $(getent group render | cut -d: -f3) \
    --env="DISPLAY=${DISPLAY}" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="${WORKSPACE_HOST}:/home/aluno/ros2_ws:rw" \
    --volume="/dev:/dev:rw" \
    ${IMAGE_NAME} bash

# ==============================================================================
# Ambiente ROS 2 Jazzy Jalisco / Gazebo Sim - Laboratório Universitário
# Disciplina: Robot Operating System (ROS 2)
# Base do OS: Ubuntu 24.04 LTS (Noble Numbat)
# ==============================================================================

FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Atualizar pacotes e instalar dependências atualizadas do ROS 2 Jazzy
RUN apt-get update && apt-get install -y --no-install-recommends \
    sudo \
    bash-completion \
    git \
    wget \
    curl \
    nano \
    vim \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    python3-argcomplete \
    mesa-utils \
    libgl1-mesa-dri \
    libglx-mesa0 \
    libgl1 \
    x11-apps \
    ros-jazzy-ros-gz \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-slam-toolbox \
    ros-jazzy-turtlebot3 \
    ros-jazzy-turtlebot3-simulations \
    ros-jazzy-rmw-cyclonedds-cpp \
    && rm -rf /var/lib/apt/lists/*

ENV TURTLEBOT3_MODEL=waffle_pi
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# ==============================================================================
# Ajuste do Usuário 'aluno' (Evita conflitos de UID/GID e resolve GPU/Render)
# ==============================================================================
ARG USERNAME=aluno

RUN if id "ubuntu" &>/dev/null; then \
        usermod -l $USERNAME ubuntu && \
        groupmod -n $USERNAME ubuntu && \
        usermod -d /home/$USERNAME -m $USERNAME; \
    else \
        groupadd --gid 1000 $USERNAME && \
        useradd --uid 1000 --gid 1000 -m $USERNAME -s /bin/bash; \
    fi \
    && usermod -aG sudo,video,render $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Configurar Workspace do aluno
USER $USERNAME
WORKDIR /home/$USERNAME
RUN mkdir -p /home/$USERNAME/ros2_ws/src

# Auto-source do ROS 2 Jazzy no .bashrc
RUN echo "source /opt/ros/jazzy/setup.bash" >> /home/$USERNAME/.bashrc && \
    echo "if [ -f /home/$USERNAME/ros2_ws/install/setup.bash ]; then source /home/$USERNAME/ros2_ws/install/setup.bash; fi" >> /home/$USERNAME/.bashrc && \
    echo "export TURTLEBOT3_MODEL=waffle_pi" >> /home/$USERNAME/.bashrc && \
    echo "export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp" >> /home/$USERNAME/.bashrc && \
    echo "cd /home/$USERNAME/ros2_ws" >> /home/$USERNAME/.bashrc

WORKDIR /home/$USERNAME/ros2_ws
CMD ["bash"]

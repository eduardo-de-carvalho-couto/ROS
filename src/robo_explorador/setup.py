from setuptools import find_packages, setup

package_name = 'robo_explorador'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aluno',
    maintainer_email='aluno@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'robo_topico_publish = robo_explorador.robo_topico_publish:main',
            'robo_topico_subscriber = robo_explorador.robo_topico_subscriber:main',
            'robo_coleta_cliente = robo_explorador.robo_coleta_cliente:main',
            'robo_coleta_servidor = robo_explorador.robo_coleta_servidor:main',
            'robo_deslocamento_servidor = robo_explorador.robo_deslocamento_servidor:main',
            'robo_deslocamento_cliente = robo_explorador.robo_deslocamento_cliente:main',
            'robo_deslocamento_cancela = robo_explorador.robo_deslocamento_cancela:main',
        ],
    },
)

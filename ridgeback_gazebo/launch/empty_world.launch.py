import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression


def generate_launch_description():
    # Get the launch directory
    this_directory = get_package_share_directory('ridgeback_gazebo')

    # Launch configuration variables specific to simulation
    headless = LaunchConfiguration('headless')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    z_pose = LaunchConfiguration('z_pose')
    yaw = LaunchConfiguration('yaw')
    config = LaunchConfiguration('config')

    # Declare the launch arguments
    declare_x_position_cmd = DeclareLaunchArgument(
        'x_pose', default_value='0.0',
        description='x_pose')

    declare_y_position_cmd = DeclareLaunchArgument(
        'y_pose', default_value='0.0',
        description='y_pose')

    declare_z_position_cmd = DeclareLaunchArgument(
        'z_pose', default_value='0.1',
        description='z_pose')

    declare_yaw_cmd = DeclareLaunchArgument(
        'yaw', default_value='0.0',
        description='yaw')

    declare_config_cmd = DeclareLaunchArgument(
        'config',
        default_value=os.getenv('RIDGEBACK_CONFIG', 'base'),
        description='get the ridgeback configuration')

    declare_headless_cmd = DeclareLaunchArgument(
        'headless',
        default_value='False',
        description='Whether to execute gzclient)')

    # Specify the actions
    start_gazebo_server_cmd = ExecuteProcess(
        cmd=['gzserver', '--verbose', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so'],
        cwd=[this_directory], output='screen')

    start_gazebo_client_cmd = ExecuteProcess(
        condition=IfCondition(PythonExpression(['not ', headless])),
        cmd=['gzclient'],
        cwd=[this_directory], output='screen')

    spawn_ridgeback_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(this_directory, 'launch', 'spawn_ridgeback.launch.py')),
        launch_arguments={
            'config': config,
            'x_pose': x_pose,
            'y_pose': y_pose,
            'z_pose': z_pose,
            'yaw': yaw
        }.items()
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_headless_cmd)
    ld.add_action(declare_x_position_cmd)
    ld.add_action(declare_y_position_cmd)
    ld.add_action(declare_z_position_cmd)
    ld.add_action(declare_yaw_cmd)
    ld.add_action(declare_config_cmd)

    # Add any conditioned actions
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(spawn_ridgeback_cmd)

    return ld

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro
import time

def generate_launch_description():
    xacro_name = "my_car"
    pkg_name = 'gazebo_spawner_test'
    pkg_path = os.path.join(get_package_share_directory('gazebo_spawner_test'))
    
    xacro_path = os.path.join(get_package_share_directory(pkg_name), 'urdf', 'my_car.xacro')
    world_path = os.path.join(get_package_share_directory(pkg_name), 'world', 'my_world.world')
    rvizConfigPath= os.path.join(pkg_path, 'config','config.rviz')
    # Process the XACRO file to get robot description
    robot_description = xacro.process_file(xacro_path).toxml()
    
    # Gazebo launch inclusion
    gazebo_ros_pkg = get_package_share_directory('gazebo_ros')
    gazebo_launch = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(os.path.join(gazebo_ros_pkg, 'launch', 'gazebo.launch.py')),launch_arguments={'world':world_path}.items()
    )

    # Node to spawn the robot entity
    spawner_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', xacro_name],
        output='screen'
    )
    
    # Node to publish robot state
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}]
    )
    rviz_node=Node(package='rviz2',executable='rviz2',name='rviz2',output='screen',arguments=['-d',rvizConfigPath])


    return LaunchDescription([
        robot_state_publisher_node,
        gazebo_launch,
        spawner_node,
        rviz_node
    ])

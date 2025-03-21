#!python3
import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Process the URDF file
    pkg_name = 'rviz2_trial'
    pkg_path = os.path.join(get_package_share_directory(pkg_name))
    xacro_file = os.path.join(pkg_path,'urdf','my_bot.xacro')
    rvizConfigPath= os.path.join(pkg_path, 'config','config.rviz')
    robot_description_config = xacro.process_file(xacro_file).toxml()
    # with open(xacro_file,'r') as file1:
    	# robot_desc=file1.read()
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    rviz_node=Node(package='rviz2',executable='rviz2',name='rviz2',output='screen',arguments=['-d',rvizConfigPath])



    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),

        node_robot_state_publisher,
        rviz_node
    ])

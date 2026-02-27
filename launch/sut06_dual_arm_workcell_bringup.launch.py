from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
import os


def launch_setup():
    left_robot_ip = LaunchConfiguration('left_robot_ip')
    right_robot_ip = LaunchConfiguration('right_robot_ip')
    use_fake_hardware = LaunchConfiguration('use_fake_hardware')
    use_sim_time = LaunchConfiguration('use_sim_time')
    launch_cameras = LaunchConfiguration('launch_cameras')
    
    dual_arm_workcell_driver_pkg = FindPackageShare('dual_arm_workcell_driver').find('dual_arm_workcell_driver')
    dual_arm_workcell_moveit_pkg = FindPackageShare('dual_arm_workcell_moveit_config').find('dual_arm_workcell_moveit_config')
    realsense2_camera_pkg = FindPackageShare('realsense2_camera').find('realsense2_camera')
    bringup_pkg = FindPackageShare('dual_arm_workcell_bringup').find('dual_arm_workcell_bringup')

    dual_arm_workcell_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(dual_arm_workcell_driver_pkg, 'launch', 'dual_arm_workcell_control.launch.py')
        ),
        launch_arguments={
            'left_robot_ip': left_robot_ip,
            'right_robot_ip': right_robot_ip,
            'use_fake_hardware': use_fake_hardware,
            'use_sim_time': use_sim_time,
        }.items()
    )

    dual_arm_workcell_moveit_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(dual_arm_workcell_moveit_pkg, 'launch', 'dual_arm_workcell_moveit.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items()
    )

    return [
        dual_arm_workcell_control_launch,
        dual_arm_workcell_moveit_launch,
    ]


def generate_launch_description():
    declared_arguments = []
    
    declared_arguments.append(
        DeclareLaunchArgument(
            name="left_robot_ip",
            default_value="192.168.131.40",
            description="Left ur16e ip address",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            name="right_robot_ip",
            default_value="192.168.131.41",
            description="Right ur16e ip address",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            name="use_fake_hardware",
            default_value="false",
            description="Use fake hardware?",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            name="use_sim_time",
            default_value="false",
            description="Use sim time?",
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            name="launch_camera",
            default_value="true",
            description="Launch Cameras?",
        )
    )

    nodes = launch_setup()
    return LaunchDescription(declared_arguments + nodes)

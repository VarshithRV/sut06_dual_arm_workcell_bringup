from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue
import os,math


def launch_setup():
    left_robot_ip = LaunchConfiguration('left_robot_ip')
    left_translation = [-0.331,0.529,0.006]
    left_rotation = [0.0,0.0,math.pi/2]
    right_robot_ip = LaunchConfiguration('right_robot_ip')
    right_translation = [0.587,0.542,0.001]
    right_rotation = [0.0,0.0,math.pi/2]
    use_fake_hardware = LaunchConfiguration('use_fake_hardware')
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    dual_arm_workcell_driver_pkg = FindPackageShare('dual_arm_workcell_driver').find('dual_arm_workcell_driver')
    dual_arm_workcell_moveit_pkg = FindPackageShare('dual_arm_workcell_moveit_config').find('dual_arm_workcell_moveit_config')

    dual_arm_workcell_control_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(dual_arm_workcell_driver_pkg, 'launch', 'dual_arm_workcell_control.launch.py')
        ),
        launch_arguments={
            'left_robot_ip': left_robot_ip,
            'left_translation_x': str(left_translation[0]),
            'left_translation_y': str(left_translation[1]),
            'left_translation_z': str(left_translation[2]),
            'left_rotation_r': str(left_rotation[0]),
            'left_rotation_p': str(left_rotation[1]),
            'left_rotation_y': str(left_rotation[2]),
            'right_robot_ip': right_robot_ip,
            'right_translation_x': str(right_translation[0]),
            'right_translation_y': str(right_translation[1]),
            'right_translation_z': str(right_translation[2]),
            'right_rotation_r': str(right_rotation[0]),
            'right_rotation_p': str(right_rotation[1]),
            'right_rotation_y': str(right_rotation[2]),
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

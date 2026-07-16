"""Run the MoveItPy motion-planning API example against the rox_fr3 (FR3 arm).

Only starts the example node. The robot (mock hardware, ros2_control
controllers, robot_state_publisher) and MoveIt must already be running,
e.g. via rox_fr3_demo_bringup.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    # MoveIt config for the FR3 arm, plus the MoveItPy (moveit_cpp) parameters
    # that this example needs (planning pipelines, plan request params, ...).
    moveit_cpp_config = os.path.join(
        get_package_share_directory("moveit_python_examples"),
        "config",
        "motion_planning_api.yaml",
    )
    moveit_config = (
        MoveItConfigsBuilder("rox_fr3", package_name="rox_fr3_demo_config")
        .moveit_cpp(file_path=moveit_cpp_config)
        .to_moveit_configs()
    )

    example_node = Node(
        package="moveit_python_examples",
        executable="motion_planning_api",
        output="screen",
        parameters=[moveit_config.to_dict()],
    )

    return LaunchDescription([example_node])

#!/usr/bin/env python3
"""Send Cartesian pose goals loaded from config/poses.yaml to the FR3 arm.

The poses.yaml file stores one or more named frames, each with a parent
frame, a position and an orientation (quaternion), e.g.::

    frames:
      move_to:
        parent: base_footprint
        position: {x: ..., y: ..., z: ...}
        orientation: {x: ..., y: ..., z: ..., w: ...}

This example loads every frame and, for each, plans and executes a motion
that brings the arm end-effector to that pose.
"""

import os
import time

import yaml

# generic ros libraries
import rclpy
from rclpy.logging import get_logger

from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import PoseStamped

# moveit python library
from moveit.planning import MoveItPy

# Planning group and the link the pose goal is applied to (the 'arm' group's
# tip link, see the SRDF chain fr3_link0 -> fr3_link8).
PLANNING_GROUP = "arm"
END_EFFECTOR_LINK = "fr3_link8"


def load_frames(poses_file):
    """Load the 'frames' dictionary from a poses.yaml file."""
    with open(poses_file, "r") as f:
        data = yaml.safe_load(f) or {}
    return data.get("frames", {})


def make_pose_stamped(frame_def):
    """Build a PoseStamped message from a single poses.yaml frame entry."""
    pose = PoseStamped()
    pose.header.frame_id = frame_def["parent"]
    position = frame_def["position"]
    orientation = frame_def["orientation"]
    pose.pose.position.x = float(position["x"])
    pose.pose.position.y = float(position["y"])
    pose.pose.position.z = float(position["z"])
    pose.pose.orientation.x = float(orientation["x"])
    pose.pose.orientation.y = float(orientation["y"])
    pose.pose.orientation.z = float(orientation["z"])
    pose.pose.orientation.w = float(orientation["w"])
    return pose


def plan_and_execute(robot, planning_component, logger, sleep_time=0.0):
    """Plan to the currently set goal and execute the resulting trajectory."""
    logger.info("Planning trajectory")
    plan_result = planning_component.plan()

    if plan_result:
        logger.info("Executing plan")
        robot.execute(plan_result.trajectory, controllers=[])
    else:
        logger.error("Planning failed")

    time.sleep(sleep_time)


def main():
    rclpy.init()
    logger = get_logger("moveit_py.send_pose_goal")

    # Locate poses.yaml inside this package's share directory.
    poses_file = os.path.join(
        get_package_share_directory("moveit_python_examples"),
        "config",
        "poses.yaml",
    )
    frames = load_frames(poses_file)
    logger.info(f"Loaded {len(frames)} pose(s) from {poses_file}")

    # instantiate MoveItPy instance and get planning component
    fr3 = MoveItPy(node_name="moveit_py")
    arm = fr3.get_planning_component(PLANNING_GROUP)
    logger.info("MoveItPy instance created")

    for name, frame_def in frames.items():
        pose_goal = make_pose_stamped(frame_def)
        logger.info(
            f"Sending goal '{name}' for link '{END_EFFECTOR_LINK}' "
            f"in frame '{pose_goal.header.frame_id}'"
        )

        # plan from the current state to the pose goal
        arm.set_start_state_to_current_state()
        arm.set_goal_state(pose_stamped_msg=pose_goal, pose_link=END_EFFECTOR_LINK)
        plan_and_execute(fr3, arm, logger, sleep_time=3.0)

    # shut down cleanly
    rclpy.shutdown()


if __name__ == "__main__":
    main()

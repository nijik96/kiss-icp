#!/usr/bin/env python3
"""
Launch-Datei für den KISS-ICP Lokalisierungsalgorithmus.

Dieses Launch-File startet den Knoten `kiss_icp_node`, der eine Punktwolke
vom angegebenen Topic empfängt und daraus die Odometriedaten berechnet.

Parameter:
  - input_topic:   Eingehendes PointCloud2 Topic (z.B. /velodyne_points_noisy)
  - visualize:     Ob RViz gestartet werden soll
  - config_file:   Pfad zur KISS-ICP Konfigurationsdatei
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition


def generate_launch_description():
    kiss_icp_pkg = get_package_share_directory("kiss_icp")
    default_config = os.path.join(kiss_icp_pkg, "config", "config.yaml")
    default_rviz = os.path.join(kiss_icp_pkg, "rviz", "kiss_icp.rviz")

    input_topic = LaunchConfiguration("input_topic")
    visualize = LaunchConfiguration("visualize", default="true")
    config_file = LaunchConfiguration("config_file", default=default_config)

    declare_input_topic = DeclareLaunchArgument(
        "input_topic",
        default_value="/velodyne_points_noisy",
        description="Eingangs-Topic für die Punktwolke"
    )

    declare_visualize = DeclareLaunchArgument(
        "visualize",
        default_value="true",
        description="Starte RViz zur Visualisierung"
    )

    declare_config_file = DeclareLaunchArgument(
        "config_file",
        default_value=default_config,
        description="Pfad zur KISS-ICP Konfigurationsdatei"
    )

    kiss_icp_node = Node(
        package="kiss_icp",
        executable="kiss_icp_node",
        name="kiss_icp_node",
        output="screen",
        remappings=[("pointcloud_topic", input_topic)],
        parameters=[
            config_file,
            {
                "base_frame": "base_link",
                "lidar_odom_frame": "odom_lidar",
                "publish_odom_tf": True,
                "invert_odom_tf": True,
                "publish_debug_clouds": True,
                "position_covariance": 0.1,
                "orientation_covariance": 0.1,
            },
        ],
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen",
        arguments=["-d", default_rviz],
        condition=IfCondition(visualize),
    )

    return LaunchDescription([
        declare_input_topic,
        declare_visualize,
        declare_config_file,
        kiss_icp_node,
        rviz_node,
    ])

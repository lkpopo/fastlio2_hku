# import launch
# import launch_ros.actions
# from launch.substitutions import PathJoinSubstitution
# from launch_ros.substitutions import FindPackageShare


# def generate_launch_description():
#     rviz_cfg = PathJoinSubstitution(
#         [FindPackageShare("localizer"), "rviz", "localizer.rviz"]
#     )
#     localizer_config_path = PathJoinSubstitution(
#         [FindPackageShare("localizer"), "config", "localizer.yaml"]
#     )

#     lio_config_path = PathJoinSubstitution(
#         [FindPackageShare("fastlio"), "config", "mid360.yaml"]
#     )
#     return launch.LaunchDescription(
#         [
#             launch_ros.actions.Node(
#                 package="fast_lio",
#                 executable='fastlio_mapping',
#                 output="screen",
#                 parameters=[
#                     {"config_path": lio_config_path.perform(launch.LaunchContext())}
#                 ],
#             ),
#             launch_ros.actions.Node(
#                 package="localizer",
#                 namespace="localizer",
#                 executable="localizer_node",
#                 name="localizer_node",
#                 output="screen",
#                 parameters=[
#                     {
#                         "config_path": localizer_config_path.perform(
#                             launch.LaunchContext()
#                         )
#                     }
#                 ],
#             ),
#             launch_ros.actions.Node(
#                 package="rviz2",
#                 namespace="localizer",
#                 executable="rviz2",
#                 name="rviz2",
#                 output="screen",
#                 arguments=["-d", rviz_cfg.perform(launch.LaunchContext())],
#             )
#         ]
#     )

from ament_index_python.packages import get_package_share_directory
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.conditions import IfCondition
from launch_ros.actions import Node


def generate_launch_description():

    # ---------------- paths ----------------
    fastlio_share = get_package_share_directory('fast_lio')
    localizer_share = get_package_share_directory('localizer')

    default_fastlio_cfg = os.path.join(fastlio_share, 'config')
    default_localizer_cfg = os.path.join(localizer_share, 'config')
    default_rviz_cfg = os.path.join(localizer_share, 'rviz', 'localizer.rviz')

    # ---------------- launch args ----------------
    use_sim_time = LaunchConfiguration('use_sim_time')
    fastlio_cfg_path = LaunchConfiguration('fastlio_cfg_path')
    fastlio_cfg_file = LaunchConfiguration('fastlio_cfg_file')
    localizer_cfg_path = LaunchConfiguration('localizer_cfg_path')
    localizer_cfg_file = LaunchConfiguration('localizer_cfg_file')
    rviz = LaunchConfiguration('rviz')
    rviz_cfg = LaunchConfiguration('rviz_cfg')

    # ---------------- declare ----------------
    declare_args = [
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('fastlio_cfg_path', default_value=default_fastlio_cfg),
        DeclareLaunchArgument('fastlio_cfg_file', default_value='mid360.yaml'),
        DeclareLaunchArgument('localizer_cfg_path', default_value=default_localizer_cfg),
        DeclareLaunchArgument('localizer_cfg_file', default_value='localizer.yaml'),
        DeclareLaunchArgument('rviz', default_value='true'),
        DeclareLaunchArgument('rviz_cfg', default_value=default_rviz_cfg),
    ]

    # ---------------- nodes ----------------
    fastlio_node = Node(
        package='fast_lio',
        executable='fastlio_mapping',
        parameters=[
            PathJoinSubstitution([fastlio_cfg_path, fastlio_cfg_file]),
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    localizer_node = Node(
        package='localizer',
        executable='localizer_node',
        parameters=[
            PathJoinSubstitution([localizer_cfg_path, localizer_cfg_file]),
            {'use_sim_time': use_sim_time}
        ],
        output='screen'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_cfg],
        condition=IfCondition(rviz)
    )

    ld = LaunchDescription()
    for arg in declare_args:
        ld.add_action(arg)

    ld.add_action(fastlio_node)
    ld.add_action(localizer_node)
    ld.add_action(rviz_node)

    return ld

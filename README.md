# ROS 2 Autonomous Turtle Tracking

An event-driven ROS 2 package where a pursuer turtle autonomously tracks, intercepts, and removes dynamically spawned target turtles within the `turtlesim` environment. 
[Screencast from 2026-08-28 20-57-43.webm](https://github.com/user-attachments/assets/f657815e-6419-4afb-873e-dfb99218e34c)

## System Architecture

This project utilizes a multi-node architecture communicating via ROS 2 topics and services:
*   **`turtlesim_node`**: The core simulation environment.
*   **`turtle_spawner`**: Custom node that generates random coordinate data and calls the `/spawn` service to continuously introduce new targets. Publishes target locations to the `NewTurtlePose` custom topic.
*   **`turtle_controller`**: Custom node that calculates the Euclidean distance and angular difference between the pursuer and the target. It publishes proportional `Twist` commands to `/turtle1/cmd_vel` and calls the `/kill` service upon successful interception.

## Prerequisites

*   Ubuntu 22.04 / 24.04
*   ROS 2 (Humble / Iron / Jazzy)
*   `turtlesim` package
*   `my_interfaces` (Custom message package containing the `NewTurtlePose.msg` definition)

## Installation & Build

1. **Navigate to your workspace source directory:**
   ```bash
   cd ~/ros2_ws/src
2. Clone the repository:
   ```bash
   git clone [https://github.com/mohamedabdulhamid-bot/ros2-autonomous-turtle-tracking.git](https://github.com/mohamedabdulhamid-bot/ros2-autonomous-turtle-tracking.git)

3. Build the workspace:
   ```bash
   cd ~/ros2_ws
   colcon build --packages-select turtle_tracking_pkg
   
4. Source the setup file:
   ```bash
   source install/setup.bash

## Usage

Launch the complete system (simulation, controller, and delayed spawner) using the provided XML launch file:
   ```bash
   ros2 launch turtle_tracking_pkg turtle_project.launch.xml
   ```
🛠️ Configuration

If the tracking turtle oscillates or overshoots the target, you can adjust the proportional gains (P-gains) directly inside turtle_controller.py:

    Linear Gain: Modifies interception speed.

    Angular Gain: Modifies rotation speed for target alignment.

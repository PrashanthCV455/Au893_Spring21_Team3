This folder includes he files for the final capstone project for the course AuE8930 Autonomy: Science and Systems. It includes details on Gazebo implementation and real world (Sim2Real) implementation of the following tasks:

--> Wall

--> Obstacle Avoidance

--> Line following

--> Stop sign detection

--> April Tag tracking

The Turtlebot Burger will have to autonomously navigate through the Gazebo environment as shown below:

**PROJECT PROBLEM STATEMENT**

The robot will have to complete the following tasks:

- Task 1: Wall following/Obstacle avoidance - The Turtlebot starts here. It must successfully follow the wall and avoid the obstacles until it reaches the yellow line. Create a map of this corridor using a SLAM package of your choice. (You could also come up with your own solution for wall following and obstacle avoidance).

- Task 2: Line following & Stop Sign Detection -The Turtlebot must successfully follow the yellow line. Stop Sign detection
While navigating the yellow line, the Turtlebot should stop at the stop sign for 3 seconds before continuing. The stop-sign will be detectedbyTinyYOLO

- Task 3: AprilTag tracking - For this task you will need to spawn another TB3 in the environment in the empty space past the yellow line and attach an AprilTag to the robot. TheTB3 with the AprilTag will be teleoperated by the user and the preceding TB3 needs to track its motion.

**INSTRUCTIONS**

- run roscore
- ssh into the robot
- launch turtlebot bring up
- launch the camera node on the turtlebot
- Launch the
_turtlebot3_autonomy_final.launch launch file_

- This will launch the final world in an empty world with the turtlebot3 burger spawned in it.
- Next the turtlebot3 burger will start performing the wall following task.
- The bot will automatically switch from wall following to obstacle avoidance task once it comes across an obstacle in its path.
- When the bot detects that there are no more obstacle on its way and the yellow line comes into view the bot will automatically switch to line following task.
- As the bot is performing the line following task, when it detects the stop sign, it will stop for 3-4 seconds and then start following the line again till the yellow line goes out of its sight.
- As the yellow line goes out of its sight and an april tag is in sight, the bot will start performing April Tag detection and tracking.
- As the April Tag is moved, the bot will automatically start following it until the AprilTag is removed from its camera frame.



**BONUS**

Can you navigate the above course completely autonomously without the need to switch tasks with keyboard presses? What are the different ways you can implement this?

We were able to fully automate the code seamlessly without the need for key presses to switch between tasks. This code is in scripts folder under the name main_mission.py

**_Certain prerequisites_**

- To properly launch the environment in Gazebo, set the GAZEBO_MODEL_PATH variable to point to models in auefinals package too. Use the following command to do so:

export GAZEBO_MODEL_PATH=/path/to/workspace/src/aue_finals/models:/path/to/workspace/src/turtlebot3_simulations/turtlebot3_gazebo/models

- Download the environment, build your workspace and launch the world with the following command:

roslaunch aue_finals turtlebot3_autonomy_final.launch

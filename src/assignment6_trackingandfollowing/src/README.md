*Part 1: Turtlebot3 Line Tracking*

(i) Line Tracking in Gazebo
 The line_follower.mp4 video under videos shows that the turtlebot is able to perform line tracking in Gazebo.


Please follow the steps to run the code:

1. run roscore

2. Run roslaunch assignment6_trackingandfollowing turtlebot3_follow_line.launch
This launch file opens the Gazebo world and runs the python script follow_line_step_hsv.py

--> Subscribtion topic: /camera/rgb/image_raw to obtain the data from camera

3. Calculate the centroid of the blob of the image which represents the track.

4. Implement a proportional controller to adjust the angular velocity command to steer this centroid to the center of the image frame.

(ii) Real world Line Tracking

1. ssh into the turtlebot burger's raspberrypi

2. run python3 follow_line_step_hsv_BOT.py

--------This script executes the same image processing and the p-controller implemented in part 1.1--------

- Refer to the Real_World_line-following.mp4 video under Videos folder.

*Part 2: April Tags*

Clone the two git repositories into your src folder:

https://github.com/AprilRobotics/apriltag_ros

https://github.com/AprilRobotics/apriltag


- These repositories will fecilitate in using apriltags in ROS
- run catkin_make to compile an source the batchrc and setup.bash files.


------ *to run the apriltag* -----------
- run the commad to bring up the turtlebot

- ssh into the turtlebot to connect to it

- After the TurtleBot and camera have been brought up, execute the python script (the commad given below) on the remote PC.
      -----> python3 tagdemo3.py

- This script uses the 'apriltag' package to detect the apriltag and extract the coordinates of its center.

- Then the p-controller from part1 is implemented to steer the bot towards the April Tag.

- If the tag is not detected (menaing no tag is present), a velocity of zero is commanded to the bot.

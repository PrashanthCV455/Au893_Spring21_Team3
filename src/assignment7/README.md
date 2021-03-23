This file consists of an explanation for Assignment 7.

-----------------------------PART 1----------------------------------

This part is done completely on the physical turtlebot.

1. The launch file, slam.launch, launche the nodes:
   turtlebot3_bringup
   turtlebot3_slam
   turtlebot3_teleop_key.
   Using the turtlebot3_teleop_key, turtlebot burger moves and maps the environment.
2. The generated map is then used to navigate the turtlebot around the environment autonomously.

Karto SLAM:

3. After installing the karto packages launch the karto node by running
   roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=karto
4. Using the turtlebot3_teleop_key, turtlebot is moved in the environment and the karto_map is generated.
5. This generated karto_map is then used to navigate the turtlebot around the environment autonomously.


------------------------------PART 2----------------------------------

Part 2 deals with the comparison between LDS lidar which is a default 2D lidar on turtlebot3 and Hokuyo 3D lidar.
Configuration for Hokuyo lidar is done by following the instructions given in:
    i. http://amanbreakingthings.blogspot.com/2014/11/adding-hokuyo-lidar-to-turtlebot-in-ros.html

    ii. http://wiki.ros.org/turtlebot/Tutorials/indigo/Adding%20a%20lidar%20to%20the%20turtlebot%20using%20hector_models%20%28Hokuyo%20UTM-30LX%29

    iii. http://wiki.ros.org/turtlebot/Tutorials/hydro/Adding%20a%20Hokuyo%20laser%20to%20your%20Turtlebot

A launch file is created to launch turtlebot_world, slam node and the teleop node.

Slam node is run to save the map using both LDS_lidar and Hokuyo_lidar.

-- Maps folder contains the maps for both Part 1 and Part 2

--Videos folder contains the videos for Navigation in Part1 and both SLAM and Navigation in Part2

 *Observations*

 1. Time: Hokuyo_lidar generated the map much faster than the default LDS_lidar.
 2. Computational demand: Since Hokuyo_lidar took lesser time to generate the map it seemed to be computationally less demanding than LDS_lidar.
 3. Graphics: Hokuyo_lidar seemed to generate the map more accurately in lesser span of time compared to LDS_lidar which took more time to generate comparitively less accurate map. Hence, it seems like Hokuyo_lidar is graphically more demanding than LDS_lidar.
 4. Performance: Hokuyo_lidar has better performance when compared to LDS_lidar for the fact that the former is a 3D lidar whilst the latter is a 2D lidar.
 5. Another reason for Hokuyo_lidar to generate a better map in less time is that it seemed to cover more area for every time step compared to LDS_lidar which could cover lesser area for a given time step. 

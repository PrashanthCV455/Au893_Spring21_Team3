#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
PI= 3.1415926535897

def move():
    # Starts a new node
    rospy.init_node('square', anonymous=True)
    velocity_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    vel_msg = Twist()

    #Receiveing the user's input
    print("Let's move your robot")

    ang_vel = 0.3
    #float(input ("Input your angular velocity:"))
    speed = 0.3
    #float(input("Input your speed:"))

    distance = 2
    error = 0.0

    #We wont use these components
    vel_msg.linear.y = 0
    vel_msg.linear.z = 0
    vel_msg.angular.x = 0
    vel_msg.angular.y = 0



    while not rospy.is_shutdown():

        #Setting the current time for distance calculus
        current_distance = 0
        current_angle = 0
        error = 0
	#Loop to move the turtle in an specified distance
        for i in range (4):
            t0 = rospy.Time.now().to_sec()
            current_distance = 0
            while(current_distance <= 2.0):
                vel_msg.linear.x = speed
                vel_msg.angular.z = 0
                #Publish the velocity
                velocity_publisher.publish(vel_msg)
                t1=rospy.Time.now().to_sec() #Takes actual time to velocity calculus
                current_distance= speed*(t1-t0) #Calculates distancePoseStamped



            t2 = rospy.Time.now().to_sec()
            current_angle = 0
            while(current_angle <= PI/2.0):
                vel_msg.linear.x = 0
                vel_msg.angular.z = ang_vel
                velocity_publisher.publish(vel_msg)
                t3= rospy.Time.now().to_sec()
                current_angle = ang_vel*(t3-t2)


        #After the loop, stops the robot
        vel_msg.linear.x = 0
        vel_msg.linear.y = 0
        vel_msg.angular.z = 0
        #Force the robot to stop
        velocity_publisher.publish(vel_msg)
        rospy.spin()


if __name__ == '__main__':
    try:

        #Testing our function
        move()
    except rospy.ROSInterruptException: pass

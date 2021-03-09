#!/usr/bin/env python3
import roslib
import sys
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from move_robot import MoveTurtlebot3

kp = 0.05
kd = 0
ki = 0.001
pre_error = 0
err_sum = 0
temp = 0
t1 = 0
first_line_confirmation = False
line_find_factor = 0
n = 0

class LineFollower(object):
    def __init__(self):
        self.bridge_object = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.camera_callback)
        self.moveTurtlebot3_object = MoveTurtlebot3()

    def camera_callback(self,data):
        # We select bgr8 because its the OpneCV encoding by default
        cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="brg8")
        height, width, channels = cv_image.shape
        crop_img = cv_image[int((height/2)+100):int((height/2)+120)][2:int(width)]

        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

        # Define the yellow section in HSV
        yellow_lower = np.array([20,100,100])
        yellow_higher = np.array([50,255,255])
        mask = cv2.inRange(hsv, yellow_lower, yellow_higher)
        M = cv2.moments(mask) #False

        cv_image2 = cv_image
        global first_line_confirmation

        try:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            rospy.loginfo("Mode - Line following")
            cv_image2 = cv2.putText(cv_image2,"Mode: Line following maneuver", (20,24),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_4)
            invoke_line_finder = False
            first_lane_confirmation = True
        except ZeroDivisionError:
            cx = height/2
            cy = width/2
            rospy.loginfo("no version")
            invoke_line_finder = True

        # Draw the centroid in the result image
        cv2.circle(mask, (int(cx),int(cy)), 5, (255,0,0),-1)

        global kp,ki,kd,pre_error,err_sum,temp
        err = cx - width/2

        #define the nodes
        cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        twist_object = Twist()

        #avoid steady state oscillation
        if err > -5 or err < 5:
            err = 0
        
        # line following maneuver control/// why here use - err
        twist_object.linear.x = np.clip(-float(err)*kp/100 + kd*(-err+pre_error),-0.2,0.2)
        a_temp = np.clip((-float(err)*kp/100 + kd*(-err+pre_error)),-0.2,0.2)

        twist_object.angular.z = np.clip(0.2*(1-abs(a_temp)/2),0,0.2)
        b_temp = np.clip(0.2*(1-abs(a_temp)/2),0,0.2)


        # after each control
        pre_error =temp
        err_sum = err_sum + err

        global t1,n
        global line_find_factor

        
        # control to find lane
        t0 = float(rospy.Time.now().to_sec())
        timestep = (t0-t1)

        if invoke_line_finder:
            if first_line_confirmation == False:
                print("Mode - Line finding maneuver")
                cv_image2 = cv2.putText(cv_image2,"Mode: Line following maneuver - 1", (20,24),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,cv2.LINE_4)

            twist_object.linear.x = 0.2
            twist_object.angular.z = 0.02

            if first_line_confirmation:
                twist_object.linear.x = np.clip((line_find_factor * 0.05),0,0.08)
                twist_object.angular.z = 0.2
                n = n + timestep*twist_object.angular.z

                if n > 3.1415*1.5 and invoke_line_finder:
                    n = 0
                    line_find_factor = line_find_factor + 1

                print("Mode - Line finding maneuver - 2")
                cv_image2 = cv2.putText(cv_image2,"Mode: Line following maneuver - 2", (20,24),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1,cv2.LINE_4)
                print("Angle turned by bot=>"+str(n))
        t1 = t0
        if a_temp == twist_object.angular.z and b_temp == twist_object.linear.x:
            line_find_factor = 0
            n = 0
        cmd_vel_pub.publish(twist_object)

        # Display
        cv_image2 = cv2.rectangle(cv_image2,(10,5),(290,100),(0,255,0),2)
        msg1 = str("Line error" + str(int(err*100/width)) + "%")
        cv2.putText(cv_image2, msg1, (20,45),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0),1,cv2.LINE_4)
        msg2 = str("Line velocity" + str(twist_object.linear.x) + "%")
        cv2.putText(cv_image2, msg2, (20,60),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0),1,cv2.LINE_4)
        msg3 = str("Angular velocity" + str(twist_object.angular.z) )
        cv2.putText(cv_image2, msg3, (20,75),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0),1,cv2.LINE_4)
        msg4 = str("Update time (ms)" + str(1000*timestep))
        cv2.putText(cv_image2, msg4, (20,90),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,255,0),1,cv2.LINE_4)

        cv2.namedWindow("Original",cv2.WINDOW_NORMAL)
        cv2.imshow("Original",cv_image2)
        cv2.waitKey(1)

        rospy.loginfo("Angular Value Sent ===>" + str(twist_object.angular.z))
        self.moveTurtlebot3_object.move_robot(twist_object)

    def clean_up(self):
        self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()

def main():
    
    rospy.init_node('line_following_node', anonymous=True)
    line_follower_object = LineFollower()
    rate = rospy.Rate(5)
    ctrl_c = False

    def shutdown():
        line_follower_object.clean_up()
        rospy.loginfo("Shutdown")
        ctrl_c = True
    rospy.on_shutdown(shutdown)
    while not ctrl_c:
        rate.sleep()
    

if __name__ == '__main__':
    main()
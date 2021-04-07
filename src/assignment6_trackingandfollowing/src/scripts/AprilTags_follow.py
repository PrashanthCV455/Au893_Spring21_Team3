#!/usr/bin/env python3
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from apriltag_ros.msg import AprilTagDetectionArray
from move_robot import MoveTurtlebot3

rot = 0
fwd = 0


class Apriltag_follower(object):

    def __init__(self):

        self.bridge_object = CvBridge()
        self.publish = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.image_sub = rospy.Subscriber('/tag_detections_image', Image, self.camera_callback)
        self.sub = rospy.Subscriber('/tag_detections', AprilTagDetectionArray, self.callback)

    def camera_callback(self, data):

        cv_image = self.bridge_object.imgmsg_to_cv2(data, desired_encoding="bgr8")
        cv2.imshow("Scan", cv_image)
        cv2.waitKey(1)

    def callback(self, data):
        global rot, fwd
        try:
            rot = data.detections[0].pose.pose.pose.position.x - 0.09
            fwd = data.detections[0].pose.pose.pose.position.z
            vel_msg = Twist()
	
            Kp_fwd = 0.2    #proportional gains
            Kp_rot = 1.8     #proportional gains

            flag= 0
            if fwd < 0.1:
                vel_msg.linear.x = 0
            else:
                vel_msg.linear.x = forward * Kp_forward
                if rot < 0:
                    flag= 1
                if rot > 0:
                    flag= -1
                vel_msg.angular.z = flag* Kp_rot * abs(rot) / 2

            self.publish.publish(vel_msg)

        except IndexError:
            rospy.loginfo('Tag not present')

    def clean_up(self):
        self.moveTurtlebot3_object.clean_class()
        cv2.destroyAllWindows()


def main():
    rospy.init_node('april_tag_node', anonymous=True)

    Apriltag_follower()

    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    main()

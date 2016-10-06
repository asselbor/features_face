#!/usr/bin/env python
#coding: utf-8

'''
Author: Thibault Asselborn 																				  
Date: 15.08.2016	        																				  
this node is used to track the gaze of the user and estimate the region in space where he/she is looking at.  
Work with the libraryOpenFace (https://github.com/TadasBaltrusaitis/OpenFace)								    


	Referential of camera:


									   (watching you)
								############################
			x positive  		###                      ###
		    --------------------###-------web+cam        ### z positive pointing at you
								###          |           ###
								#############|##############
											 |
											 |
											 |
											 |
											 | y positive
'''

import rospy
from std_msgs.msg import Float32MultiArray, UInt8
from numpy import array, mat
from math import cos, sin


def callBackGaze(data):

	### Transform the data given by OpenFace in a carthisian position in the plan of the webcam. You can change the plan's z position by
	### changing the variable planOIzPos. Here we put z0 because z0 is the distance between the camera and the user's face.

	# get inputs from OpenFace
	inputs = data.data
	# get yaw, pitch, roll from vector
	yaw = inputs[8]
	pitch = inputs[7]
	roll = inputs[6]
	# get position cathesian in space of head
	x0 = inputs[9]
	y0 = inputs[10]
	z0 = inputs[11]
	# get direction of gaze for each eyes
	x_gaze0 = inputs[0]
	y_gaze0 = inputs[1]
	z_gaze0 = inputs[2]
	x_gaze1 = inputs[3]
	y_gaze1 = inputs[4]
	z_gaze1 = inputs[5]

	# matric to change referential according to yaw, pitch, roll
	matixTransform = array([ [cos(yaw)*cos(pitch), cos(yaw)*sin(pitch)*sin(roll) - sin(yaw)*cos(roll), cos(yaw)*sin(pitch)*cos(roll) + sin(yaw)*sin(roll)],
            [sin(yaw)*cos(pitch), sin(yaw)*sin(pitch)*sin(roll) + cos(yaw)*cos(roll), sin(yaw)*sin(pitch)*cos(roll) - cos(yaw)*sin(roll)],
            [-sin(pitch), cos(pitch)*sin(roll), cos(pitch)*cos(roll)] ])

	#vectorGaze = array([[x_gaze0], [y_gaze0], [z_gaze0]])
	planOIzPos = z0
	# let's assume that the gaze it's orthogonal to the head face
	vectorGaze = array([[0], [0], [-1.0]])
	# change referential
	vectorGaze_ref = mat(matixTransform)*vectorGaze
	# get position where user looks in webcam's plan
	positionRefRobot = vectorGaze_ref*planOIzPos/1000.0 +  array([[x0], [y0], [z0]])/1000.0
	# check if this position is the position of a robot
	getRobotMatch(positionRefRobot)

def getRobotMatch(positionRefRobot):
	### in function of the cartisian position given, publish in topic topic_gaze which object we are looking at

	# carthesian position of the view in webcam's plan
	x = positionRefRobot.item(0, 0)
	y = positionRefRobot.item(1, 0)

	# left robot has id 1 = Clem and right robot is R1
	if y < positionY1_r12 and y > positionY2_r12:

		# robot left gaze match
		if x > positionX1_r1 and x < positionX2_r1:
			publisher_gaze_match.publish(1)
		# robot right gaze match
		elif x < positionX1_r2 and x > positionX2_r2:
			publisher_gaze_match.publish(2)
		# touch pad gaze match	
		elif x > positionX1_tab and x < positionX2_tab and y > positionY_tab:
			publisher_gaze_match.publish(0)


if __name__ == '__main__':

	# create node
	rospy.init_node('detect_gaze_match')

	# Subscribe to topic gaze, giving all features needed to compute the gaze
	TOPIC_GAZE = rospy.get_param('~topic_gaze')
	rospy.Subscriber(TOPIC_GAZE, Float32MultiArray, callBackGaze)

	# Create publisher to send when te user watch one robot
	TOPIC_GAZE_MATCH = rospy.get_param('~topic_gaze_match')
	publisher_gaze_match = rospy.Publisher(TOPIC_GAZE_MATCH, UInt8, queue_size=10)

	# position parameters for gaze match 
	###### robots ######
	# position x robot left -> id 1 (# x1 always position the more in left)
	positionX1_r1 = rospy.get_param('~positionX1_r1')
	positionX2_r1 = rospy.get_param('~positionX2_r1')
	# position x robot left -> id 1
	positionX1_r2 = rospy.get_param('~positionX1_r2')
	positionX2_r2 = rospy.get_param('~positionX2_r2')
	# position y robots
	positionY1_r12 = rospy.get_param('~positionY1_r12')
	positionY2_r12 = rospy.get_param('~positionY2_r12')
	###### touch pad ######
	# position touch pad
	positionX1_tab = rospy.get_param('~positionX1_tab')
	positionX2_tab = rospy.get_param('~positionX2_tab')
	positionY_tab = rospy.get_param('~positionY_tab')

	rospy.spin()
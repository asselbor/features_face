#!/usr/bin/env python
#coding: utf-8

### just used to launch the openFace tracker

import rospy
import os

if __name__ == '__main__':
	rospy.init_node('executable_launcher')

	# get current open face face
	path = rospy.get_param('~pathOpenFace')
	path += '/build/bin/FeatureExtraction' 
	#path += ' -rigid -verbose -f "/home/asselbor/outputMemory/adriana_5/outputVideo_2016-09-27 14:35:20.avi" -of "output_features/default.txt" -simalign output_features/aligned'

	os.system(path)

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


TO launch it:
change the path to the executable of open space in features_face.launch. You can change the position of the objects tracked by the gate in this launch file. use roslaunch features_face.launch to run the node.

Installation of open face: 
go to the build directory of Open face and run: 
cmake -D CMAKE_BUILD_TYPE=RELEASE ..
make

more details about openface installation here:   https://github.com/TadasBaltrusaitis/OpenFace/wiki/Unix-Installation


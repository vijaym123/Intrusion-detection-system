"""
I would like to call this program as Intrusion detection system. Because it does a functionality similar to it ;).
This program involves the following componets :
	1) Capturing frames from the camera with a time in betweeen 
	2) Each successive frame are converted to grayscale image (which is the measure of intensity of light).
	3) Form these grayscale frames. We find the difference of the successive frames.  
	4) Later get the binary image of this differenced image.
	5) We compute the Change in intensity of light from this differenced images. 
		From the value of change in intensity we can infer two things.
		         - If the value peaks at some point. ( We can infer that a object has shown a sudden movement.)
		         - If the value is normal, i.e does not show any peak. (We can infer that no object is moving.)        
	6) If the value is above threshold, the images are stored to make a not of the object which has trespassed the area under           		   cover.	         
	
Basic Instructions to run the program.

$ python trespass.py
the program is in while loop.

press "crtl+c" to break	out of the program.
A polt and images are the output of the program
	- Plot denotes at which frame what is the difference value ( i.e the The value peaks if there is a tresspass in the region undercover.)
	- Images are stored for these peak values in the specified path.

Testing :
	- The place under surveillance is left undisturbed for few seconds. If Suddent movements are made in the place the images are captured.
	- Tested this program for various lighting conditions in the room.
	- Works fine with respect to various condition.
"""

import SimpleCV as sv
import time
import matplotlib.pyplot as plt

def difference(img0,img1):
  """
  This module takes in two images and converts it to grayscale. Later finds the difference of the two images and returns the differenced image.
  Syntax : difference(img0,img1)
  where img0 and img1 are two images.  	
  """
  img2 = img0.grayscale()
  img3 = img1.grayscale()
  return img2-img3  
  

def main():
  """
  Main function. 
  This initialise the webcam. 
  """ 	
  cam = sv.Camera(0)
  k=0;
  x_axis = [] 
  #This the Path were the images are stored in the region where the object have shown movement.  
  path = raw_input("Enter the destination path, for storing the frames : \n")
  try :
   while(True):
     	img0 = cam.getImage().flipHorizontal().scale(320, 240)
        time.sleep(0.001)
        img1 = cam.getImage().flipHorizontal().scale(320, 240)
    	#The difference of two grayscale images.
    	diff_image = difference(img0,img1)
    	#Binary image computed form the above difference image.
       	bina_image = diff_image.binarize()
       	k+=1
       	count_white = 0
       	count_black = 0
       	width = bina_image.size()[0]
       	height = bina_image.size()[1]
       	#Computes the number of black and white pixels in the binary image.
       	for i in range(0,width):
       	   for j in range(0,height):	
       	  	pix = bina_image.getPixel(i,j)
       	  	if pix == (255.0, 255.0, 255.0) :
       	  		count_white += 1
       	  	else :
       	  		count_black += 1		
       	#If there is a sudden movement the abs(count_white-count_black) becomes high. 		
       	print k ,"th frame, abs(count_white-count_black):" , abs(count_white-count_black)
       	#abs(count_white-count_black) is stored in the array and later used for ploting the graph
       	x_axis.append(abs(count_white-count_black))
       	if (abs (count_white-count_black) > 50000):
 	      	img1.save( path +'image'+str(k)+'.jpg')
       	time.sleep(0.0416)
  except KeyboardInterrupt :
	#Ploting the graph: X-axis : Frames . Y-axis : abs(count_white-count_black).
	plt.plot(range(len(x_axis)),x_axis)
	plt.show()  			  	
main()

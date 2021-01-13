#java -cp /home/nemo/openpnp/openpnp-gui-0.0.1-alpha-SNAPSHOT.jar org.openpnp.vision.pipeline.ui.StandaloneEditor
# https://github.com/openpnp/openpnp/issues/573
from __future__ import division
import cv2 as cv
import numpy as np

image = cv.imread("1.png")

# Performs gaussian blurring on the working image
# Imgproc.GaussianBlur(mat, mat, new Size(kernelSize, kernelSize), 0);

# <cv-stage class="org.openpnp.vision.pipeline.stages.ImageCapture" name="capture" enabled="true" settle-first="true"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.ImageWriteDebug" name="0" enabled="true" prefix="debug" suffix=".png"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.ConvertColor" name="gray" enabled="true" conversion="Bgr2Gray"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.Threshold" name="highlights" enabled="true" threshold="240" auto="false" invert="false"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.ImageRecall" name="recall1" enabled="true" image-stage-name="gray"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.Threshold" name="lowlights" enabled="true" threshold="120" auto="false" invert="true"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.Add" name="combined" enabled="true" first-stage-name="highlights" second-stage-name="lowlights"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.BlurMedian" name="merged" enabled="true" kernel-size="9"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.FindContours" name="contours" enabled="true" retrieval-mode="External" approximation-method="None"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.FilterContours" name="filtered_contours" enabled="true" contours-stage-name="contours" min-area="300.0" max-area="2000.0"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.MinAreaRectContours" name="rects" enabled="true" contours-stage-name="filtered_contours"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.OrientRotatedRects" name="oriented_rects" enabled="true" rotated-rects-stage-name="rects" orientation="Landscape" negate-angle="false"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.OrientRotatedRects" name="results" enabled="true" rotated-rects-stage-name="rects" orientation="Landscape" negate-angle="true"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.ImageRecall" name="recall2" enabled="true" image-stage-name="capture"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.DrawContours" name="draw_contours" enabled="true" contours-stage-name="filtered_contours" thickness="2" index="-1"/>
# <cv-stage class="org.openpnp.vision.pipeline.stages.DrawRotatedRects" name="draw_results" enabled="true" rotated-rects-stage-name="oriented_rects" thickness="2" draw-rect-center="true" rect-center-radius="3" show-orientation="true">
#    <color r="51" g="255" b="51" a="255"/>
# </cv-stage>


# Convert BGR to HSV https://docs.opencv.org/3.4.2/df/d9d/tutorial_py_colorspaces.html
hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
upper_color = np.array([130,255,255])
lower_color = np.array([40,10,50])

# Threshold the HSV image to get only blue colors
mask = cv.inRange(hsv, lower_color, upper_color)
mask = 255 - mask # invert mask
# Bitwise-AND mask and original image
masked_image = cv.bitwise_and(image,image, mask= mask)
cv.imshow("masked_image", masked_image)
cv.waitKey(0)
quit()

# ConvertColor
image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
cv.imshow("image_gray", image_gray)


# Threshold" name="highlights https://github.com/openpnp/openpnp/blob/d881befa3f289dd0db4b19524efcaea3fe36d665/src/main/java/org/openpnp/vision/pipeline/stages/Threshold.java#L39
a, image_highlights = cv.threshold(image_gray,240,255,cv.THRESH_BINARY)
cv.imshow("image_highlights", image_highlights)
# ImageRecall
# Threshold" name="lowlights https://github.com/openpnp/openpnp/blob/d881befa3f289dd0db4b19524efcaea3fe36d665/src/main/java/org/openpnp/vision/pipeline/stages/Threshold.java#L39
a, image_lowlights = cv.threshold(image_gray,120,255,cv.THRESH_BINARY_INV)
cv.imshow("image_lowlights", image_lowlights)

# Add" name="combined 
image_added = cv.add(image_highlights, image_lowlights)
cv.imshow("image_added", image_added)

# BlurMedian" name="merged  
image_blurred = cv.medianBlur(image_added, 9)
cv.imshow("image_blurred", image_blurred)

# FindContours https://github.com/openpnp/openpnp/blob/d881befa3f289dd0db4b19524efcaea3fe36d665/src/main/java/org/openpnp/vision/pipeline/stages/FindContours.java
image_contours, contours, hierarchy = cv.findContours(image_blurred,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
clone = image.copy()
cv.drawContours(clone, contours, -1, (0,255,0), 3)
# loop over the contours
for c in contours:
	# compute the moments of the contour which can be used to compute the
	# centroid or "center of mass" of the region
	M = cv.moments(c)
	area = cv.contourArea(c)
	print(area)
	if area > 5000 and area < 7000:
		try:
			cx = int(M['m10']/M['m00'])
			cy = int(M['m01']/M['m00'])
			cv.circle(clone, (cx, cy), 10, (0, 0, 255), -1)
			cv.putText(clone, "#{}".format(area), (cx - 20, cy), cv.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 4)
		except ZeroDivisionError:
			print('0') #or whatever
	
	# cX = int(M["m10"] / M["m00"])
	# cY = int(M["m01"] / M["m00"])
	# # draw the center of the contour on the image
	# cv.circle(clone, (cX, cY), 10, (0, 255, 0), -1)
	
# Rotated Rectangle
for c in contours:
	rect = cv.minAreaRect(c)
	box = cv.boxPoints(rect)
	box = np.int0(box)
	cv.drawContours(clone,[box],0,(0,0,255),2)
	
cv.imshow("image_contours", clone)



# FilterContours
# MinAreaRectContours
# OrientRotatedRects
# OrientRotatedRects
# ImageRecall
# DrawContours
# DrawRotatedRects



# show the image and wait for a keypress

cv.waitKey(0)
# cv.imwrite("newimage.jpg", image)

# java -cp openpnp-gui-0.0.1-alpha-SNAPSHOT.jar org.openpnp.vision.pipeline.ui.StandaloneEditor
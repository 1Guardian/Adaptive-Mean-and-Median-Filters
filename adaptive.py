#==============================================================================
#
# Class : CS 6420
#
# Author : Tyler Martin
#
# Project Name : Project 3 | Adaptive filters
# Date: 3/16/2023
#
# Description: This project implements two filters working as adaptive filters
#
# Notes: Since I know you prefer to read and work in C++, this file is set
#        up to mimic a standard C/C++ flow style, including a __main__()
#        declaration for ease of viewing. Also, while semi-colons are not 
#        required in python, they can be placed at the end of lines anyway, 
#        usually to denote a specific thing. In my case, they denote globals, 
#        and global access, just to once again make it easier to parse my code
#        and see what it is doing and accessing.
#
#==============================================================================

#"header" file imports
from imports import *
from checkImages import *
from getMetaData import *
from saveJson import *
from grayScaleImage import *
from saveImage import *
from operators import *

#================================================================
#
# NOTES: THE OUTPATH WILL HAVE THE LAST / REMOVED IF IT EXISTS
#        THE imageType WILL HAVE A . APPLIED TO THE FRONT AFTER
#        CHECKING VALIDITY
#
#================================================================

rect_selector = None
fequency_representation_shifted = None
fig = None
filename = None
image = None
magnitude_spectrum = None
freq_filt_img = None
reset = False

#================================================================
#
#
#Function to add salt and pepper noise
#
#
#================================================================
def SaltAndPepper(image, percent):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (random.randint(0, 100) < percent):
                if (random.randint(0, 100) < 50):
                    image[i][j] = 0
                else:
                    image[i][j] = 255
    return image

#================================================================
#
#
#Calc the Euclidean distance between images
#
#
#================================================================
def EuclideanDistance(image, image2):

    return cv2.norm(image, image2)

#================================================================
#
#
#Function to apply the adaptive mean filter
#
#
#================================================================
def adaptiveMean(image, original_image, maximum, chanceSalt, chancePepper, windowSize):

    paddedImage = np.pad(image, pad_width=maximum, mode='reflect')

    constraints = windowSize

    corruption_variance = np.var(np.int32(original_image) - np.int32(image))

    for i in range(maximum, image.shape[0] + maximum):
        for j in range(maximum, image.shape[1] + maximum):
            zxy = int(paddedImage[i][j])
            currentNeighborHood = paddedImage[i-constraints:i+constraints+1, j-constraints:j+constraints+1]
            local_variance = np.var(currentNeighborHood)
            local_mean = np.mean(currentNeighborHood)

            #adaptive mean
            image[i-maximum][j-maximum] = (zxy - ((corruption_variance/local_variance)*(zxy - local_mean))) 


    return image

#================================================================
#
#
#Function to apply the adaptive median filter
#
#
#================================================================
def adaptiveMedian(image, maximum):

    paddedImage = np.pad(image, pad_width=maximum, mode='reflect')

    for i in range(maximum, image.shape[0] + maximum):
        for j in range(maximum, image.shape[1] + maximum):

            continueFlag = True
            constraints = 1
            zxy = int(paddedImage[i][j])

            while (continueFlag):
                    
                currentNeighborHood = paddedImage[i-constraints:i+constraints+1, j-constraints:j+constraints+1]
                zmed = int(np.median(currentNeighborHood))
                zmin = int(np.min(currentNeighborHood))
                zmax = int(np.max(currentNeighborHood))

                A_1 = zmed - zmin
                A_2 = zmed - zmax

                #start of procedure given in notes
                if A_1 > 0 and A_2 < 0:
                    B_1 = zxy - zmin
                    B_2 = zxy - zmax

                    if B_1 > 0 and B_2 < 0:
                        zxy = zxy
                        continueFlag = False
                    else:
                        zxy = zmed
                        continueFlag = False
                
                else:
                    constraints += 1
                
                if constraints > maximum:
                    zxy = zmed
                    continueFlag = False

            #replace the pixel
            image[i-maximum][j-maximum] = zxy

    return image

#================================================================
#
# Function: __main__
#
# Description: This function is the python equivalent to a main
#              function in C/C++ (added just for ease of your
#              reading, it has no practical purpose)
#
#================================================================

def __main__(argv):

    #globals
    global rect_selector
    global fequency_representation_shifted
    global fig
    global filename
    global image
    global magnitude_spectrum

    #variables that contain the command line switch
    #information
    inPath = "nothing"
    depth = 1
    mode = 1
    intensity = 1
    primary = "nothing"
    filename = "outImage"
    filenameTwo = "outImage"
    direction = 0
    percent = 10
    windowSize = 6

    # get arguments and parse
    try:
      opts, args = getopt.getopt(argv,"h:t:s:n:w:m:")

    except getopt.GetoptError:
            print("adaptive [-h] -n [percent of corrupted pixels] -t input_image -s [output_image] -m [output_image]")
            print("===========================================================================================================")
            print("-t : Target Image (t)")
            print("-s : Output Median Filtered Image")
            print("-m : Output Mean Filtered Image")
            print("-n : percent of corrupted pixels")
            print("-w : mean filter window size")
            sys.exit(2)
    for opt, arg in opts:

        if opt == ("-h"):
            print("adaptive [-h] -n [percent of corrupted pixels] -t input_image -s [output_image] -m [output_image]")
            print("===========================================================================================================")
            print("-t : Target Image (t)")
            print("-s : Output Median Filtered Image")
            print("-m : Output Mean Filtered Image")
            print("-n : percent of corrupted pixels")
            print("-w : mean filter window size")
            
        elif opt == ("-t"):
            primary = arg
        elif opt == ("-s"):
            filename = arg
        elif opt == ("-m"):
            filenameTwo = arg
        elif opt == ("-n"):
            percent = arg
        elif opt == ("-w"):
            windowSize = int(arg)

    #demand images if we are not supplied any
    if (primary == "nothing"):
        print("adaptive [-h] -n [percent of corrupted pixels] -t input_image -s [output_image] -m [output_image]")
        print("===========================================================================================================")
        print("-t : Target Image (t)")
        print("-s : Output Median Filtered Image")
        print("-m : Output Mean Filtered Image")
        print("-n : percent of corrupted pixels")
        print("-w : mean filter window size")
        sys.exit(2)

    

    #open the image
    image = SaltAndPepper(grayScaleImage(checkImages(primary)), int(percent))
    original_image = grayScaleImage(checkImages(primary))
    print("euclidean distance between original image and noisy image: ", EuclideanDistance(original_image, image))
    cv2.imshow("Original Image With Noise", image)
    cv2.waitKey(0)

    #apply median filter
    median_image = adaptiveMedian(np.copy(image), 6)
    print("euclidean distance between original image and median filtered image: ", EuclideanDistance(original_image, median_image))
    cv2.imshow("Median Filtered Image", median_image)
    cv2.waitKey(0)

    #apply median filter
    mean_image = adaptiveMean(np.copy(image), original_image, 6, (int(percent)/2)/100, (int(percent)/2)/100, windowSize)
    print("euclidean distance between original image and mean filtered image: ", EuclideanDistance(original_image, mean_image))
    cv2.imshow("Mean Filtered Image", mean_image)
    cv2.waitKey(0)

    #write out if requested
    if (filename != "outImage"):
        cv2.imwrite(filename, median_image)
    if (filenameTwo != "outImage"):
        cv2.imwrite(filenameTwo, mean_image)

#start main
argv = ""
__main__(sys.argv[1:])
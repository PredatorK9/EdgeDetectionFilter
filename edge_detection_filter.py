# importing libraries
import matplotlib.image as img
import numpy as np
import argparse

# A function to accept command line arguments
def getArguments():

    # specifying our parser for command line argument parsing
    parser = argparse.ArgumentParser()

    # adding arguments for our program
    # the parameters will be the source image and the final processed image
    parser.add_argument("--image", dest="source_image", help="Specify the input image")
    parser.add_argument("--save", dest="final_image", help="Specify the save image name (OPTIONAL)")

    # storing the argument in a variable
    options = parser.parse_args()

    # checking for the arguments
    if not options.source_image:
        parser.error("[-] Source image not specified")
    if not options.final_image:
        options.final_image = "Edge extracted image.png"
    return options

# Function for reading the image using matplotlib
def readImage(srcImage):

    # reading the matrix and storing it in a matrix
    image = img.imread(srcImage)

    # Getting Image parameters
    w, h = image.shape[:2]

    # returning the image matrix and it's parameters
    return image, w, h

def greyscaleImage(image, w, h):
    # Getting Image parameters
    w, h = image.shape[:2]

    # creating the envelope for the greyscale image
    grey_image = np.zeros([w, h, 3])

    # greyscaling the image
    for i in range(w-1):
        for j in range(h-1):

            # the luminous greyscaling is:
            # 0.3 * R + 0.59 * G + 0.11 * B
            # R, G and B are Red, Blue and Green components of the image
            avg = (0.3 * image[i][j][0])+(0.59 * image[i][j][1])+(0.11* image[i][j][2])
            for z in range(3):
                grey_image[i][j][z] = avg

    return grey_image

# function where our kernel is defined and is convolved over the whole image
def detectEdges(image, w, h):

    # Using a point kernel
    # Chaning the values in the kernel can have various effects on the image
    # SUM OF ALL THE ELEMENTS OF THE KERNEL SHOULD BE ZERO
    # IF NOT ZERO THEN IT WILL HAVE EITHER BRIGHTENING EFFECT OR DARKENING EFFECT DEPENDING ON THE WEIGHTEDNESS
    kernel = np.array([ [0, -1, 0],
                        [-1, 4, -1],
                        [0, -1, 0]])

    # creating the envelope for the nwe image
    new_image =  np.zeros([w, h, 3])

    # performing convolution with our kernel over the image
    for i in range (w-3):
        for j in range (h-3):
            new_image[i+1][j+1] = (kernel[0][0] * image[i+1][j+1] + kernel[0][1] * image[i+1][j+2] + kernel[0][2] * image[i+1][j+3] +
                                   kernel[1][0] * image[i+2][j+1] + kernel[1][1] * image[i+2][j+2] + kernel[1][2] * image[i+1][j+3] + 
                                   kernel[2][0] * image[i+3][j+1] + kernel[2][1] * image[i+3][j+2] + kernel[2][2] * image[i+3][j+3])

    # returning our image from the function
    return new_image

# Function for truncating the pixel intensity values
def truncateIntesity(new_image, w, h):

    # matplotlib.image normalizes the image
    # this means that instead of having intensity range between 0 and 255
    # the intensity of each pixel ranges between 0 and 1

    # to make sure that the pixel values doesn't break the limits
    # we are truncating the values
    for i in range(w-1):
        for j in range(h-1):
            for z in range(3):
                if(new_image[i][j][z] < 0):
                    new_image[i][j][z] = 0
                elif(new_image[i][j][z] > 1):
                    new_image[i][j][z] = 1
    return new_image


if __name__ == '__main__':
    arguments = getArguments()
    image, w, h = readImage(arguments.source_image)
    grey_image = greyscaleImage(image, w, h)
    new_image = detectEdges(grey_image, w, h)
    new_image = truncateIntesity(new_image, w, h)
    
    # saving the image
    img.imsave(arguments.final_image, new_image)
    print("[+] Processing finised")
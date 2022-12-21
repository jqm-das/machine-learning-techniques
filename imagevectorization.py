import urllib.request
import io
import random
import math 
import time 
from PIL import Image
import sys 
URL = "https://cdn.factcheck.org/UploadedFiles/ThomasJefferson_thumb_101419-200x200.jpg"
f = io.BytesIO(urllib.request.urlopen(URL).read()) # Download the picture at the url as a file object
img = Image.open(f) # You can also use this on a local file; just put the local filename in quotes in place of f.
# img.show() # Send the image to your OS to be displayed as a temporary file
# print(img.size) # A tuple. Note: width first THEN height. PIL goes [x, y] with y counting from the top of the frame.
# pix = img.load() # Pix is a pixel manipulation object; we can assign pixel values and img will change as we do so.
# print(pix[2,5]) # Access the color at a specific location; note [x, y] NOT [row, column].
# pix[2,5] = (255, 255, 255) # Set the pixel to white. Note this is called on “pix”, but it modifies “img”.
# img.show() # Now, you should see a single white pixel near the upper left corner
# img.save("my_image.png") # Save the resulting image. Alter your filename as necessary.



def twentysevencolor(image):
    pixel = image.load() 
    width,height = image.size
    for i in range (0,width):
        for j in range (0,height):
            r,g,b = pixel[i,j]
            if ( r < 63):
                r = 0
            elif (r < 190):
                r = 127
            else:
                r = 255
            if ( b < 63):
                b = 0
            elif (b < 190):
                b = 127
            else:
                b = 255
            if ( g < 63):
                g = 0
            elif (g < 190):
                g = 127
            else:
                g = 255
            pixel[i,j] = (r,g,b)
    return image

# newimage = twentysevencolor(img)
# newimage.show()

def eightcolor(image):
    pixel = image.load() 
    width,height = image.size
    for i in range (0,width):
        for j in range (0,height):
            r,g,b = pixel[i,j]
            if ( r < 128):
                r = 0
            else:
                r = 255
            if ( b < 128):
                b = 0
            else:
                b = 255
            if ( g < 128):
                g = 0
            else:
                g = 255
            pixel[i,j] = (r,g,b)
    return image


# newimage = eightcolor(img)
# newimage.show()

def initial(k,image):
    ls = []
    colors = [] 
    pixel = image.load() 
    width,height = image.size 
    for i in range (0,k):
        w = int(random.random() * width)
        h = int(random.random() * height)
        rand = (w,h)
        color = pixel[w,h] 
        while rand in ls or color in colors:
            w = int(random.random() * width)
            h = int(random.random() * height)
            rand = (w,h,color)
            color = pixel[w,h] 
        ls.append([(rand,color)])
        colors.append(color) 
    return ls 

def avg(setinfo):
    h,w,c = 0,0,(0,0,0)
    r,g,b = c 
    for i in setinfo: 
        measurements,color = i
        red,green,blue = color
        r = r + red 
        g = g + green
        b = b + blue 
    r = r / len(setinfo)
    g = g/ len(setinfo)
    b = b/ len(setinfo) 
    return r,g,b 

def mean(individual,setinfo):
    r,g,b = individual
    red,green,blue = setinfo
    error = math.pow(red-r,2) + math.pow(green-g,2) + math.pow(blue-b,2) 
    return error


def findvector(image,k):
    start = initial(k,image)
    width,height = image.size 
    pixel = image.load()

    vector = [] 
    finalvector = start
    count = 0 

    while vector != finalvector: 
        colorcode = []
        finalvector = vector 
        vector = [] 

        for i in range(0,k):
            vector.append([])
            if count == 0:
                colorcode.append(avg(start[i]))
            else:
                colorcode.append(avg(finalvector[i]))
    
        for i in range (0,width):
            for j in range (0,height):
                minerror = 100000
                bestset = 0 
                for x in range (0,k):
                    error = mean(pixel[i,j],colorcode[x])
                    if error < minerror:
                        minerror = error
                        bestset = x 
                vector[bestset].append(((i,j),pixel[i,j])) 
        count = count + 1
        #print(count) 

    return finalvector 

def vectorize(r,g,b,vector):
    minerror = 100000
    bestset = 0 
    for x in range (0,len(vector)):
        error = mean((r,g,b),vector[x])
        if error < minerror:
            minerror = error
            bestset = x 
    return avg(vector[bestset])

k = 27
def nvector(image):
    pixel = image.load() 
    vector = findvector(image,k)   
    for i in vector:
        colorcode = avg(i)
        for j in i:
            cords,colors = j 
            x,y = cords
            r,g,b = colorcode
            pixel[x,y] = (int(r),int(g),int(b))
    return image

newimage = nvector(img)
newimage.save("kmeansout.png")
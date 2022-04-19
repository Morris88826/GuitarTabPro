import math
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def find_line(img, threshold=30, plot=False):
    height, width = img.shape[:2]

    if len(img.shape)==3:
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    edges = cv2.Canny(gray,50,150,apertureSize = 3)

    lines = cv2.HoughLines(edges,1,np.pi/180,threshold)

    if lines is None:
        return None, None, None

    my_lines = []
    horizontal_lines = []
    vertical_lines = []
    for i, line in enumerate(lines):
        for rho,theta in line:
            a = np.cos(theta)
            b = np.sin(theta)
            

            
            x0 = a*rho
            y0 = b*rho
            x1 = np.clip(int(x0 + width*(-b)), 0, width)
            y1 = np.clip(int(y0 + width*(a)), 0, height)
            x2 = np.clip(int(x0 - width*(-b)), 0, width)
            y2 = np.clip(int(y0 - width*(a)), 0,height)

            my_theta = math.atan2(y2-y1, x2-x1)


            if abs(np.sin(my_theta)-np.sin(0))<0.01 or abs(np.sin(my_theta)-np.sin(np.pi/2))<0.01 or  abs(np.sin(my_theta)-np.sin((3*np.pi)/2))<0.01:
                # print(my_theta)
                l_start = [x1, y1]
                l_end = [x2, y2]

                if abs(np.sin(my_theta)-np.sin(0))<0.01:
                    repeated = False
                    for l in horizontal_lines:
                        _l_start = l[0]
                        _l_end = l[1]


                        d1 = abs(l_start[1]-_l_start[1])
                        d2 = abs(l_end[1]-_l_end[1])
                        d = d1 + d2
                        if d < 10:
                            repeated = True
                            break
                    if not repeated:
                        horizontal_lines.append([l_start, l_end])
                else:
                    repeated = False
                    for l in vertical_lines:
                        _l_start = l[0]
                        _l_end = l[1]


                        d1 = abs(l_start[0]-_l_start[0])
                        d2 = abs(l_end[0]-_l_end[0])
                        d = d1 + d2
                        if d < 10:
                            repeated = True
                            break
                    if not repeated:
                        vertical_lines.append([l_start, l_end])


    my_lines = horizontal_lines + vertical_lines

    # print("Number of strings detected: {}".format(len(my_lines)))
    if plot:
        plt.imshow(img, cmap="gray")
        for l in my_lines:
            l_start = l[0]
            l_end = l[1]
            plt.plot([l_start[0], l_end[0]], [l_start[1], l_end[1]])
        plt.show()

    return my_lines, horizontal_lines, vertical_lines


if __name__ == "__main__":
    # img_path = '/Users/morris88826/Desktop/projects/GuitarTabExtractor/code/annotation_tool/test.png'
    img_path = './result/frame_0.png'
    img = np.array(Image.open(img_path))
    # find_string(img, plot=True)
    # find_section(img, plot=True)

    # img = cv2.imread(img_path)
    print(img.shape)
    find_line(img, plot=True, threshold=int(img.shape[0]*0.4))

    # locsDoG, gaussian_pyramid = DoGdetector(img)

    # for i in range(locsDoG.shape[0]):
    #     cv2.circle(img, (locsDoG[i, 0], locsDoG[i, 1]), 1, (0, 255, 0), -1)
    # cv2.imshow('Pyramid of image', img)
    # cv2.waitKey(0) # press any key to exit
    # cv2.destroyAllWindows()
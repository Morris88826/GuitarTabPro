import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

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


def generate_sheet(output, width=1000, paddings=20, cut=False):
    row_height = output.shape[0]
    num_rows = (output.shape[1]//width) + 1
    sheet = np.ones(((num_rows*row_height+(num_rows-1)*paddings), width))*255
    

    lines = []
    start_w = 0
    while start_w<output.shape[1]:
        end_w = min(start_w+width, output.shape[1])
        line = output[:, start_w:end_w]
        
        if cut:
            _, _, vertical_lines = find_line(line, threshold=int(line.shape[0]*0.4), plot=False)
            
            if vertical_lines is None or len(vertical_lines)==0 or np.amax(np.array(vertical_lines)[:, :, 0])==0:
                # end_w = min(start_w + width, output.shape[1])
                break
            else:
                line_separate = np.amax(np.array(vertical_lines)[:, :, 0])
                end_w = start_w+line_separate
            new_line = output[:, max(start_w-5,0): min(output.shape[1], end_w+5)]

            lines.append(new_line)
            start_w = end_w
    
        else:
            start_w = end_w
            lines.append(line)
    num_rows = len(lines)
    
    sheet = np.ones(((num_rows*row_height+(num_rows-1)*paddings), width))*255

    for r, line in enumerate(lines):
        start_h = (row_height+paddings)*r
        sheet[start_h:(start_h+row_height), :min(line.shape[1], width)] = line[:, :min(line.shape[1], width)]

    return sheet
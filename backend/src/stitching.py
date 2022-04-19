from re import I
import cv2
import numpy as np
import matplotlib.pyplot as plt
from utils import rgb_to_gray
import glob
from PIL import Image
from find_line import find_line
from generator import generate_sheet

def stitch_image(im1, im2):

    output = np.zeros((im1.shape[0], im1.shape[1]+im2.shape[1]), dtype=im1.dtype)
    output[:, :im1.shape[1]] = im1

    new_diff = 1e6
    new_d = None

    best_match = []

    _, _, vl = find_line(im2.astype(np.uint8))

    if len(vl) == 0:
        start = 0
    else:
        start = np.amin(np.array(vl)[:, 0, 0])

    for d in range(start+20, min(im1.shape[1], im2.shape[1])):
        _diff = np.sqrt(np.sum(np.square(im1[:,-d:].astype(np.float64)-im2[:, :d].astype(np.float64))))/(np.prod(im2[:, :d].shape))

        if _diff < new_diff:
            new_diff = _diff
            new_d = d
            best_match.append([new_d, new_diff])

    best_d = []
    for i, (d, score) in enumerate(best_match[::-1]):
        if i == (len(best_match)-1):
            break
        else:
            _, pre_score = best_match[::-1][i+1]
            if (pre_score-score)/score > 0.5:
                best_d.append(d)
    
    if len(best_d) == 0:
        return im1
    best_d = best_d[-1]
    output[:, im1.shape[1]:-best_d] = im2[:, best_d:]
    return output[:, :-best_d].astype(np.uint8)

def stitch_images(images):

    if len(images)==0:
        return

    output = images[0]
    output = rgb_to_gray(output)

    for i in range(1, len(images)):
        im = images[i]
        im = rgb_to_gray(im)
        output = stitch_image(output, im)
    
    return output

if __name__ == '__main__':
    folder_dir = './result'
    images_path = sorted(glob.glob(folder_dir+'/*'), key=lambda p: int(p.split('/')[-1].split('.')[0].split('_')[1]))
    images = []
    for image_path in images_path:
        images.append(np.array(Image.open(image_path)))

    output = stitch_images(images[8:10])

    sheet = generate_sheet(output, width=1500, cut=False)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(sheet, cmap='gray')
    ax.axis('off')
    ax.set(title="My Sheet")
    plt.show()
    # fig.savefig('output.png')


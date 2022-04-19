from tkinter import image_names
import cv2
import os
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import shutil
import glob


def video_to_images(path, out_dir):
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()

    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.mkdir(out_dir)

    count = 0
    while success:
        cv2.imwrite(out_dir+"/frame_%d.png" % count, image)
        success, image = vidcap.read()
        count += 1


def load_images(folder_dir):
    images_path = sorted(glob.glob(folder_dir+'/*'),
                         key=lambda p: int(p.split('/')[-1].split('.')[0].split('_')[1]))
    images = []
    for image_path in images_path:
        images.append(np.array(Image.open(image_path)))
    return images


def rgb_to_gray(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    return 0.299*R + 0.587*G + 0.114*B


def select_frames(images_path, ROI):
    imgs = []
    imgs_path = []
    previous_img = None
    step = 10
    for i, image_path in enumerate(images_path):

        if i % step != 0:
            continue

        if (i+step) >= len(images_path):
            break

        img = np.array(Image.open(image_path))

        img = img[ROI[0, 1]:ROI[1, 1], ROI[0, 0]:ROI[1, 0]]

        if previous_img is not None:
            diff = 1 - ssim(rgb_to_gray(img), rgb_to_gray(previous_img))

            if diff > 0.4:

                ver = np.array(Image.open(images_path[i+step]))
                ver = ver[ROI[0, 1]:ROI[1, 1], ROI[0, 0]:ROI[1, 0]]
                diff2 = (1 - ssim(rgb_to_gray(img), rgb_to_gray(ver)))
                if diff2 > 0.2:
                    continue

                imgs.append(img)
                imgs_path.append(image_path)
                previous_img = img

        else:
            imgs.append(img)
            imgs_path.append(image_path)
            previous_img = img

    return imgs, imgs_path

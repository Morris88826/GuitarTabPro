import ui
import argparse
import json
from utils import video_to_images, load_images, select_frames
from ui import MainView
from stitching import stitch_images
from generator import generate_sheet
from PIL import Image
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', help="path to the video")
    parser.add_argument('--save_frames', type=bool,
                        default=True, help="save the selected frames")
    args = parser.parse_args()

    video_to_images(args.path)

    images, images_path = load_images('../assets/tmp')
    if len(images) == 0:
        print("No image!")
    else:
        main = MainView('../assets/tmp/frame_0.png')
        main.mainloop()

        if ui.ROI is not None:
            d = {
                "start_x": int(min(ui.ROI[0][0], ui.ROI[1][0])),
                "start_y": int(min(ui.ROI[0][1], ui.ROI[1][1])),
                "end_x": int(max(ui.ROI[0][0], ui.ROI[1][0])),
                "end_y": int(max(ui.ROI[0][1], ui.ROI[1][1]))
            }
            with open("../assets/roi.json", 'w') as jsonfile:
                json.dump(d, jsonfile, indent=4)
            roi = np.array([[d["start_x"], d["start_y"]],
                        [d["end_x"], d["end_y"]]])

            frames, frames_path = select_frames(images_path, roi)

            with open('../assets/selectedFrames.json', 'w') as jsonfile:
                json.dump({
                    "files": frames_path
                }, jsonfile)

            output = stitch_images(frames)

            sheet = generate_sheet(output, cut=False, width=2000).astype(np.uint8)
            Image.fromarray(sheet).save('../assets/tab.png')

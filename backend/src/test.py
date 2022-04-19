import json
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def test_roi():
    if not os.path.exists('../assets/roi.json') or not os.path.exists('../assets/tmp/frame_0.png'):
        return False

    with open('../assets/roi.json', 'r') as jsonfile:
        data = json.load(jsonfile)
    image = np.array(Image.open('../assets/tmp/frame_0.png'))

    # Create a Rectangle patch
    rect = patches.Rectangle((data["start_x"], data["start_y"]), data["end_x"]-data["start_x"], data["end_y"]-data["start_y"], linewidth=1,
                             edgecolor='r', facecolor='none')

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(image)
    ax.add_patch(rect)
    plt.show()

    return True


if __name__ == "__main__":
    test_roi()

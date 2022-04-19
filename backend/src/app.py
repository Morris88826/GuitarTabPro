from flask import Flask, request, jsonify
from pytube import YouTube
from flask_cors import CORS
import os
import json
from io import BytesIO
import ffmpeg
import base64
from utils import video_to_images, select_frames
import numpy as np
import glob
from stitching import stitch_images
from generator import generate_sheet
from PIL import Image
import matplotlib.pyplot as plt

app = Flask(__name__)
cors = CORS(app, expose_headers=["Content-Disposition"])


@app.route("/searchytvideo", methods=["GET", "POST"])
def searchytvideo():
    if request.method == "POST":
        try:
            url = YouTube(request.json['url'])
            url.check_availability()

            available_videos = []

            for i in url.streams.filter(progressive=True).filter(mime_type="video/mp4"):
                available_videos.append({
                    "itag": i.itag,
                    "resolution": i.resolution
                })
            return jsonify({
                "success": True,
                "data": available_videos,
                "message": "Video found."
            })
        except:
            return jsonify({
                "success": False,
                "message": "The URL is not valid."
            })
    return {"sucess": False}


@app.route("/downloadytvideo", methods=["POST"])
def downloadytvideo():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(request.json['url'])
        itag = request.json['itag']
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        video_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        video_prefix = "data:video/mp4;base64"
        return {
            "success": True,
            "video": video_prefix + "," + video_base64
        }
    return {"sucess": False}


@app.route("/trimvideo", methods=["POST"])
def trimvideo():
    start_t = request.json['start_t']
    end_t = request.json['end_t']
    video = request.json['video']
    video_base64 = video.split(',')[-1]
    video_prefix = video.split(',')[0]

    formatted_start_t = format_time(start_t)
    formatted_end_t = format_time(end_t)

    # decode base64 to video
    fh = open("../assets/video.mp4", "wb")
    fh.write(base64.b64decode(video_base64))
    fh.close()

    if os.path.exists('../assets/trimmed_video.mp4'):
        os.remove('../assets/trimmed_video.mp4')

    ffmpeg.input('../assets/video.mp4', ss=(
        formatted_start_t), t=(formatted_end_t)).output('../assets/trimmed_video.mp4').run()

    # encode video to base64
    with open("../assets/trimmed_video.mp4", "rb") as videoFile:
        trimmed_video_base64 = base64.b64encode(videoFile.read())
        trimmed_video_base64 = trimmed_video_base64.decode("utf-8")

    return {
        "success": True,
        "start_time": start_t,
        "end_time": end_t,
        "video":  video_prefix+','+trimmed_video_base64
    }


@app.route("/getthumbnail", methods=["GET"])
def getthumbnail():
    video_path = '../assets/trimmed_video.mp4'
    if os.path.exists(video_path):
        video_to_images(video_path, out_dir='../assets/tmp', save=True)

        with open("../assets/tmp/frame_0.png", "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode("utf-8")
            # debug_base64(encoded_string)
        return {
            "success": True,
            "image": encoded_string
        }
    else:
        return {
            "success": False
        }


@app.route("/saveroi", methods=["POST"])
def saveroi():
    roi = request.json['roi']

    if roi is not None:

        with open("../assets/roi.json", 'w') as jsonfile:
            json.dump(roi, jsonfile, indent=4)

        return {
            "success": True,
        }
    return {
        "success": False
    }


@app.route("/getindependentframes", methods=["GET"])
def getindependentframes():

    if os.path.exists("../assets/roi.json") and os.path.exists("../assets/tmp"):
        with open("../assets/roi.json", 'r') as jsonfile:
            d = json.load(jsonfile)
        roi = np.array([[d["start_x"], d["start_y"]],
                       [d["end_x"], d["end_y"]]])

        images_path = sorted(glob.glob('../assets/tmp/*'),
                             key=lambda p: int(p.split('/')[-1].split('.')[0].split('_')[1]))
        _, frames_path = select_frames(images_path, roi)

        image_header = "data:image/png;base64,"

        images = []
        for i, frame_path in enumerate(frames_path):
            with open(frame_path, "rb") as image_file:
                encoded_string = base64.b64encode(
                    image_file.read()).decode("utf-8")

            images.append({
                "id": i,
                "path": frame_path,
                "src": image_header+encoded_string
            })

        with open('../assets/selectedFrames.json', 'w') as jsonfile:
            json.dump({
                "files": frames_path
            }, jsonfile)
        return {
            "success": True,
            "selected_frames": images
        }

    return {
        "success": False
    }


@app.route("/generatetab", methods=["GET", "POST"])
def generatetab():
    if request.method == "POST":
        return {
            "success": True
        }
    else:
        with open("../assets/selectedFrames.json", 'r') as jsonfile:
            frames_path = json.load(jsonfile)['files']

        with open("../assets/roi.json", 'r') as jsonfile:
            d = json.load(jsonfile)

        frames = []
        for frame_path in frames_path:
            frames.append(np.array(Image.open(frame_path))[
                          d["start_y"]:d["end_y"], d["start_x"]:d["end_x"]])

        output = stitch_images(frames)
        sheet = generate_sheet(output, cut=False, width=2000).astype(np.uint8)
        Image.fromarray(sheet).save('../assets/tab.png')

        image_header = "data:image/png;base64,"
        with open('../assets/tab.png', "rb") as image_file:
            encoded_string = base64.b64encode(
                image_file.read()).decode("utf-8")

        return {
            "success": True,
            "tab": image_header+encoded_string
        }


def debug_base64(base64_file):
    with open('../assets/debug_base64.txt', 'w') as myFile:
        myFile.write(base64_file)


def format_time(time):
    hrs = time // 3600
    time = time % 3600
    minutes = time // 60
    seconds = time % 60
    milliseconds = round((seconds - int(seconds))*100)

    if milliseconds != 0:
        return "{:02d}:{:02d}:{:02d}.{}".format(int(hrs), int(minutes), int(seconds), milliseconds)
    else:
        return "{:02d}:{:02d}:{:02d}".format(int(hrs), int(minutes), int(seconds))


if __name__ == "__main__":

    if not os.path.exists("../assets"):
        os.mkdir("../assets")
    app.run(debug=True)

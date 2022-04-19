# GuitarTabPro

## Get Started
1. Setup the environment
```
conda create -n GuitarTabPro python=3.8
conda activate GuitarTabPro
```
2. Get the repo
```
git clone https://github.com/Morris88826/GuitarTabPro.git
cd GuitarTabPro/backend
pip install -r requirements.txt
```
3. Hosting the backend

Make sure that the backend is running on http://127.0.0.1:5000.
```
cd src
python app.py
 * Serving Flask app 'app' (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 760-970-399

```

## Project Website

Project Website: https://morris88826.github.io/GuitarTabPro/

* Host the backend before using the website.
* The results are stored in /backend/assets

## Alternatives

In /backend/src we provide main.py that can generate the guitar TAB without hosting the website.
```
cd src
python main.py -p "path_to_the_video"
```

## Demo
The demo video can be found in /backend/assets/video.mp4

## Functionalities
- [x] Trim the video
- [x] Extract the guitar TAB from video
- [ ] Download video via YouTube link
- [ ] Cut the guitar TAB to end with a complete section in each line

## Questions
For any problem or bugs, please contact morris88826@gmail.com.

from tkinter.messagebox import NO
from flask import Flask, render_template, request, session
from werkzeug.utils import secure_filename
import folium
import os
from GPX_read import *
from map import *


app = Flask(__name__)
app.secret_key = 'You will never guess'

VIDEO_UPLOAD_FOLDER = os.path.join('static','video')
GPX_UPLOAD_FOLDER = os.path.join('static','gpx')
OUTPUT_FOLDER = os.path.join('static','result')

app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER
app.config['GPX_UPLOAD_FOLDER'] = GPX_UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET","POST"])
def upload():
    return render_template("public/upload.html")


@app.route("/upload2", methods=["GET","POST"])
def upload2():
    if request.method == 'POST':
        uploaded_vid = request.files['uploaded-file']
        vid_filename = secure_filename(uploaded_vid.filename)
        uploaded_vid.save(os.path.join(app.config['VIDEO_UPLOAD_FOLDER'],vid_filename))

        session['uploaded_vid_file_path'] = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'],vid_filename)

    return render_template('public/upload2.html')    


@app.route('/upload_gpx',methods=["GET","POST"])
def upload_gpx():
    if request.method == 'POST':
        uploaded_gpx = request.files['uploaded-gpxfile']
        gpx_filename = secure_filename(uploaded_gpx.filename)
        uploaded_gpx.save(os.path.join(app.config['GPX_UPLOAD_FOLDER'],gpx_filename))

    vid_file_path = session.get('uploaded_vid_file_path',None)

    path = ""
    new_path = path+gpx_filename
    read_gpx(new_path)

    csv_path = ''
    read_csv(csv_path)
    
    #frame divide
    frame_path = ''
    frame(frame_path)
    
    detect_path = ''
    files = os.listdir(detect_path)
    jpg_img = []
    for file in files:
        if '.jpg' in file:
            f = cv2.imread(detect_path+"/"+file)
            jpg_img.append(f)
    
    result = model(jpg_img)
    os.chdir("../")
    result.save(save_dir = 'result')

    return render_template('public/display_vid.html', upload_vid=vid_file_path, path = frame_path)

@app.route('/map')
def map():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)

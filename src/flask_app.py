from video_handling.highlight_cup import higlight_cup

from flask import Flask, redirect, url_for, jsonify, request
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        file_path = 'static/tmp/' + f.filename
        f.save(file_path)

        outfile_path = "static/tmp/handled_" + f.filename + ".avi"

        app.logger.info(file_path)
        app.logger.info(outfile_path)
        app.logger.info("Video handling is starting...")
        higlight_cup(file_path, "/application/"+outfile_path)
        app.logger.info("higlight finished")
        return  jsonify({"target": "/" + outfile_path})

    return  jsonify({"target": "/static/tmp/handled_2018-02-2715_03_24.ogv.avi"})



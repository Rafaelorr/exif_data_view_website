from flask import Flask, request, render_template
import os
from functions import *
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('image')
    if not file:
        return "No file uploaded", 400

    # Save file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name

    # Read EXIF data
    exif_data = read_exif_data(tmp_path)

    # make GPS data human readable
    try:
        lat, lon = extract_gps_location(exif_data["GPSInfo"])
        exif_data["GPSInfo"] = {"lat":lat, "lon":lon}
    except TypeError:
        pass

    # Clean up the temporary file
    os.remove(tmp_path)

    return render_template("result.html", exif=exif_data)

@app.route("/docs")
def documentation():
    return render_template("exif_tags.html")

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

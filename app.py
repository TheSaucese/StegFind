from flask import Flask, render_template, request,redirect, url_for
from werkzeug.utils import secure_filename
import magic
from PIL import Image
import base64
from io import BytesIO
from my_utils import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files["file"] 
    file_type = magic.from_buffer(file.read(1024), mime=True)

    ext = file_type.split('/')[1]

    file_path = hashAndUpload(file,ext)

    print(file_path)

    response = handleFileType(file_path,file_type)

    if response is None:
        response = "An error occurred"

    return response

if __name__ == '__main__':
    app.run(debug=True)


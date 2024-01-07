from flask import Flask, render_template, request,url_for,send_file,jsonify
import magic
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

@app.route('/passphrase', methods=["POST"])
def passphrase():
    passphrase = request.form['pass']
    img = request.form['img']
    result = extract_with_optional_passphrase(img, passphrase=passphrase)
    path,error = result
    if path is None:
        return jsonify(error=error)
    return jsonify(fileUrl=url_for('download_file', path=path, _external=True))
  
@app.route('/download/<path>')
def download_file(path):
    # Logic to send the file at 'path' to the client
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)


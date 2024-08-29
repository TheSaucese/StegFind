import shutil
from backend.modules.embed import abort_extraction, extract_with_wordlist
from backend.modules.matroch import extract_file_from_file
from flask import Flask, render_template, request,url_for,send_file,jsonify
import magic
from my_utils import *
import zipfile

app = Flask(__name__)

# Clears the upload folder by deleting all files and directories within it
def clear_upload_folder():
    if os.path.exists('data.zip'):
        os.remove('data.zip')
    if os.path.exists('data'):
       shutil.rmtree('data')
    folder = 'static/uploads'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# Route to serve the main index page
@app.route('/')
def index():
    return render_template('index.html')

# Route to serve the database page
@app.route('/database')
def database():
    return render_template('database.html')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    clear_upload_folder()
    file = request.files["file"] 
    file_type = magic.from_buffer(file.read(1024), mime=True)

    ext = file_type.split('/')[1]

    file_path,isUploaded = hashAndUpload(file,ext)

    print(file_path)

    if isUploaded:
        print("File already exists")
        return 

    response = handleFileType(file_path,file_type)

    if response is None:
        response = "An error occurred"

    return response

# Route to handle extraction of data from an image using a passphrase
@app.route('/passphrase', methods=["POST"])
def passphrase():
    passphrase = request.form['pass']
    img = request.form['img']
    result = extract_with_optional_passphrase(img, passphrase=passphrase)
    path,error = result
    if path is None:
        return jsonify(error=error)
    return jsonify(fileUrl=url_for('download_file', path=path, _external=True))


# Route to handle automatic extraction of hidden data from an image
@app.route('/magic', methods=["POST"])
def magical():
    img = request.form['img']
    print(img)
    path = extract_file_from_file(img)
    print(path)
    if path is None:
        result = extract_with_wordlist(img)
        path,error = result
    if path is None:
        return jsonify(error=error)
    return jsonify(fileUrl=url_for('download_file', path=path, _external=True))


# Route to allow downloading of a file
@app.route('/download/<path>')
def download_file(path):
    # Logic to send the file at 'path' to the client
    return send_file(path, as_attachment=True)

# Route to abort the ongoing extraction process
@app.route('/killmagic', methods=['GET'])
def abort_extraction_route():
    abort_extraction()
    return jsonify({'message': 'Extraction aborted'})

# Route to export and download collected data as a ZIP file
@app.route('/export', methods=['POST'])
def download_data():
    # Retrieve the data parameters from the POST request
    CHANNELS = request.form.get('CHANNELS')
    EXIF = request.form.get('EXIF').replace('\\n', '\n')
    HEXDUMP = request.form.get('HEXDUMP')
    STRING = request.form.get('STRING')
    LSB = request.form.get('LSB')
    SPECTRO = request.form.get('SPECTRO')
    BINWALK = request.form.get('BINWALK')
    
    # Check if the returned values are 'undefined'
    if CHANNELS == 'undefined':
        CHANNELS = None
    if EXIF == 'undefined':
        EXIF = None
    else:
        EXIF = EXIF.replace('\\n', '\n')
    if HEXDUMP == 'undefined':
        HEXDUMP = None
    if STRING == 'undefined':
        STRING = None
    if LSB == 'undefined':
        LSB = None
    if SPECTRO == 'undefined':
        SPECTRO = None
    if BINWALK == 'undefined':
        BINWALK = None

    # Create a directory to store the data files
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)

    # Write each data parameter to a separate file in the directory
    data_files = []
    for param_name, param_data in [
                                   ('EXIF.txt', EXIF),
                                   ('HEXDUMP.txt', HEXDUMP),
                                   ('STRING.txt', STRING),
                                   ('BINWALK.txt', BINWALK),
                                   ('LSB.txt', LSB)]:
        if param_data is not None:  # Check if the data is defined
            file_path = os.path.join(data_dir, param_name)
            with open(file_path, 'w') as file:
                file.write(param_data)
            data_files.append(file_path)

    if SPECTRO is not None:
        data_files.append(SPECTRO)

    # Create a ZIP archive containing the data files
    zip_file_path = 'data.zip'
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in data_files:
            zipf.write(file_path, os.path.basename(file_path))
        if CHANNELS is not None:
            for root, dirs, files in os.walk(CHANNELS):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), CHANNELS))

    print("ZIP archive created:", zip_file_path)

    # Send the ZIP archive for download
    return jsonify(fileUrl=url_for('download_file', path=zip_file_path, _external=True))

# Main entry point for running the Flask application
if __name__ == '__main__':
    app.run(debug=True)


import hashlib
import os
from backend.modules.channel import process_image
from backend.modules.embed import extract_with_optional_passphrase
from backend.modules.hexdump import hexdump
from backend.modules.lsb import findLSB
from backend.modules.spectro import create_spectrogram
from backend.modules.strings import strings
from backend.modules.exif import exif
from flask import jsonify


def getFolder(original_string):
    # Find the index of the substring
    index = original_string.find('file')

    # If the substring is found, cut the string up to the start of the substring
    if index != -1:
        return original_string[:index]
    else:
        # If the substring is not found, return the original string
        return original_string

def handleFileType(file_path,ext):
    Type = ext.split('/')[0]
    if(Type == 'image'):
        return handleImage(file_path)

    elif(Type == 'audio'):
        return handleAudio(file_path)
    
    elif(Type == 'video'):
        return handleVideo(file_path)
    else:
        print(Type)
        print("Unknown")
        return None

def hashAndUpload(file,ext):

    hash_file = str(hashlib.md5(file.read()).hexdigest())
    file.seek(0)   
    folder = f"static/uploads/{hash_file}"
    if(ext == 'x-wav'):
        ext = 'wav'
    file_path = os.path.join(folder, f"file.{ext}")
    if not os.path.isdir(folder): 
        os.mkdir(folder)
        file.save(file_path)

    return file_path

def handleImage(file_path):

    view_data = process_image(file_path)
    exif_data = exif(file_path)  
    hex_data = hexdump(file_path, bytes_per_line=16)
    string_data = strings(file_path)
    lsb_data = findLSB(file_path)
    embed_data = extract_with_optional_passphrase(file_path)

    return jsonify(viewOutput=view_data,exifOutput=exif_data,contentOutput=hex_data,stringOutput=string_data,lsbOutput=lsb_data,embedOutput=embed_data,file_path=file_path)

def handleAudio(file_path):

    exif_data = exif(file_path)  
    hex_data = hexdump(file_path, bytes_per_line=16)
    string_data = strings(file_path)

    output_path = getFolder(file_path)
    spectrogram = create_spectrogram(file_path,output_path+"spectrogram.png")

    return jsonify(exifOutput=exif_data,contentOutput=hex_data,stringOutput=string_data,img_data=spectrogram)

def handleVideo(file_path):

    exif_data = exif(file_path)  
    hex_data = hexdump(file_path, bytes_per_line=16)
    string_data = strings(file_path)

    return jsonify(exifOutput=exif_data,contentOutput=hex_data,stringOutput=string_data)



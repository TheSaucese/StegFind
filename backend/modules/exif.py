from exiftool import ExifToolHelper

def exif(path):
    exif_data = ""
    with ExifToolHelper() as et:
        for d in et.get_metadata(path):
            for k, v in d.items():
                k = k.replace("File:", "") 
                exif_data += f"{k} = {v}/n" 
    return exif_data
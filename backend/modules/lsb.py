import numpy as np
from PIL import Image
import string

def findLSB(path):
    try:
        img = Image.open(path)
        img_array = np.array(img)

        decoded_bits = []
        for row in img_array:
            for pixel in row:
                r, g, b = pixel
                decoded_bits.extend([bin(r)[-1], bin(g)[-1], bin(b)[-1]])

        message = ''
        for i in range(0, len(decoded_bits), 8):
            byte = decoded_bits[i:i+8]
            ascii_val = int(''.join(byte), 2)
        
            if chr(ascii_val) in string.printable:
                message += chr(ascii_val)

        return message
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
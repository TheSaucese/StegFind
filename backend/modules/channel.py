import numpy as np
import os
from PIL import Image

def compute_layers(arr, mode, folder, filename):
    """Compute each bits visual image for a given layer `arr`."""
    for i in range(8):  # 8 bits layer
        newdata = (arr >> i) % 2 * 255  # Highlighting the layer bit `i`
        if mode == 'RGBA':  # Force alpha layer (4th) to 255 if exist
            newdata[:, :, 3] = 255
        Image.fromarray(newdata, mode).save(
            f"{folder}/view/{filename}_{i+1}.png")

def process_image(image_path):
    """Apply compute_layers() on each `img` layers and save images."""
    img_pil = Image.open(image_path)
    folder = os.path.dirname(image_path)
    # Convert all in RGBA except RGB images
    if img_pil.mode not in ["RGB", "RGBA"]:
        img_pil = img_pil.convert('RGBA')

    # Get numpy array
    npimg = np.array(img_pil)  # rgb

    # Create view folder
    os.makedirs(f"{folder}/view", exist_ok=True)

    # Generate images from numpy array and save
    compute_layers(npimg, img_pil.mode, folder, "image_rgb")  # rgb
    compute_layers(npimg[:, :, 0], 'L', folder, "image_r")  # r
    compute_layers(npimg[:, :, 1], 'L', folder, "image_g")  # g
    compute_layers(npimg[:, :, 2], 'L', folder, "image_b")  # b

    if img_pil.mode == "RGBA":  # Should be RGB or RGBA
        compute_layers(npimg[:, :, 3], 'L', folder, "image_a")  # alpha

    return folder + "/view"

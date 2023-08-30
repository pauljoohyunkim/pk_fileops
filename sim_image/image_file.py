from PIL import Image

def image_with_pil(path : str):
    try:
        return Image.open(path)
    except:
        return None
    
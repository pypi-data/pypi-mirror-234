import numpy as np
from PIL import Image
import torch


def is_tensor(img):
    """Check if the input image is torch format."""
    return isinstance(img, torch.Tensor)

def is_pil(img):
    """Check if the input image is PIL format."""
    return isinstance(img, Image.Image)


def is_numpy(img):
    """Check if the input image is Numpy format."""
    return isinstance(img, np.ndarray)

def is_gray_image(image):
    return (len(image.shape) == 2) or (len(image.shape) == 3 and image.shape[-1] == 1)

def is_rgb_image(image):
    return len(image.shape) == 3 and image.shape[-1] == 3

def not_rgb_warning(image):
    if not is_rgb_image(image):
        message = "This transformation expects 3-channel images"
        if is_gray_image(image):
            message += "\nYou can convert your gray image to RGB using cv2.cvtColor(image, cv2.COLOR_GRAY2RGB))"
        raise ValueError(message)

def get_num_channels(image):
    return image.shape[2] if len(image.shape) == 3 else 1

def colorstr(*input):
    # https://en.wikipedia.org/wiki/ANSI_escape_code, i.e.  colorstr('blue', 'hello world')
    *args, string = input if len(input) > 1 else ('blue', 'bold', input[0])
    colors = {
        'black': '\033[30m',  # basic colors
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',  # bright colors
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'end': '\033[0m',  # misc
        'bold': '\033[1m',
        'underline': '\033[4m'}
    return ''.join(colors[x] for x in args) + f'{string}' + colors['end']


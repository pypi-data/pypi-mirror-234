from .augment import random_apply, random_order, random_choice
import numpy as np
import torch
import cv2

class Compose():
    def __init__(self, transforms):
        self.transforms = transforms
        if all(hasattr(transform, "random") and not transform.random for transform in self.transforms):
            self.random = False
    def __call__(self, *args):
        return compose(self.transforms, *args)

class ToTensor:
    def __init__(self, half=False):
        super().__init__()
        self.half = half

    def __call__(self, img):  # im = np.array HWC in BGR order
        img = np.ascontiguousarray(img.transpose((2, 0, 1))[::-1])  # HWC to CHW -> BGR to RGB -> contiguous
        img = torch.from_numpy(img)  # to torch
        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0-255 to 0.0-1.0
        return img

class ToNumpy(object):
    def __call__(self, pil_img):
        np_img = np.array(pil_img, dtype=np.uint8)
        if np_img.ndim < 3:
            np_img = np.expand_dims(np_img, axis=-1)
        np_img = np.rollaxis(np_img, 2)  # HWC to CHW
        return np_img

class CenterCrop:
    # T.Compose([CenterCrop(size), ToTensor()])
    def __init__(self, size=640):
        super().__init__()
        self.h, self.w = (size, size) if isinstance(size, int) else size

    def __call__(self, im):  # im = np.array HWC
        imh, imw = im.shape[:2]
        m = min(imh, imw)  # min dimension
        top, left = (imh - m) // 2, (imw - m) // 2
        return cv2.resize(im[top:top + m, left:left + m], (self.w, self.h), interpolation=cv2.INTER_LINEAR)

class RandomApply():
    def __init__(self, transforms, prob=0.5):
        self.prob = prob
        self.transforms = transforms

    def __call__(self, img):
        return random_apply(img, self.transforms, self.prob)


class RandomChoice():
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, img):

        return random_choice(img, self.transforms)


class RandomOrder():
    def __init__(self, transforms):
        self.transforms = transforms

    def __call__(self, img):
        return random_order(img, self.transforms)


def compose(transforms, *args):
    """
    创建一个transforms列表
    Args:
        img (numpy.ndarray): An image in NumPy ndarray.
        transforms (list): A list of transform Class objects to be composed.

    Returns:
        img (numpy.ndarray), An augmented image in NumPy ndarray.
    """
    for transform in transforms:
        args = transform(*args)
        args = (args,) if not isinstance(args, tuple) else args
    return args


import cv2


def resize_image(image, height=0, width=0):
    (h, w) = image.shape[:2]

    if height == 0 and width == 0:
        return image
    elif height != 0:
        r = height / float(h)
        dim = (int(w * r), height)
        resized = cv2.resize(image, dim)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
        resized = cv2.resize(image, dim)
    return resized


def convert_to_binary(img, block_size, c):
    th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c)
    return th

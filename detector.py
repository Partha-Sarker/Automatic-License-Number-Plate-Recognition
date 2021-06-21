import cv2
import os
import pytesseract
import utils
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
lic_data = cv2.CascadeClassifier('number_plate_cascade.xml')
NUMBER_HEIGHT = 150
block_size, c = 255, 1
low_w, high_w, low_h, high_h = 14, 75, 42, 90
blur_h, blur_v, sigma_x = 95, 11, 20
blur_block_size, blur_c = 215, 0


def get_license_number(image):
    try:
        car = cv2.imread(os.path.join('car', image))
        gray_car = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)
    except:
        print('can not convert', image)
        return 'Error'

    number = lic_data.detectMultiScale(gray_car, 1.1, 4)
    if len(number) == 0:
        print('no plate found', image)
        return 'Error'
    biggest_region = number[0]
    for numbers in number[1:]:
        if biggest_region[2] * biggest_region[3] < numbers[2] * numbers[3]:
            biggest_region = numbers

    a, b = (int(0.03 * car.shape[0]), int(0.03 * car.shape[1]))
    (x, y, w, h) = biggest_region
    number_plate = car[y + a: y + h - a, x + b: x + w - b]
    number_plate = utils.resize_image(number_plate, height=NUMBER_HEIGHT)
    number_plate_gray = cv2.cvtColor(number_plate, cv2.COLOR_BGR2GRAY)

    number_plate_th = utils.convert_to_binary(number_plate_gray, 255, 1)
    edged = cv2.Canny(number_plate_th, 0, 0)
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask = np.full_like(number_plate_th, 0)
    for contour in contours:
        (c_x, c_y, c_w, c_h) = cv2.boundingRect(contour)
        if c_w < low_w or c_w > high_w:
            continue
        if c_h < low_h or c_h > high_h:
            continue
        cv2.rectangle(mask, (c_x, c_y), (c_x + c_w, c_y + c_h), 255, -1)
    content = np.full_like(mask, 255)
    inverse_th = np.full_like(content, 0)
    cv2.bitwise_not(number_plate_th, inverse_th)
    cv2.bitwise_and(mask, inverse_th, content)

    text = pytesseract.image_to_string(content, config='--psm 11')
    char_list = list(text)
    char_list = [c if c.isalnum() else '' for c in char_list]
    license_number = ''.join(char_list)
    return license_number

#     cv2.rectangle(car, (x, y), (x + w, y + h), (0, 255, 0), 3)
#     cv2.imshow(image, car)
#     cv2.imshow(f'{image} plate', number_plate_gray)
#     cv2.imshow(f'{image} edged plate', edged)
#     cv2.imshow(f'{image} mask', mask)
#     cv2.imshow(f'{image} content', content)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# images = os.listdir('car')
# for image in images:
#     get_license_number(image)


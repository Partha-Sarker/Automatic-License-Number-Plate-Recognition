import cv2
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
lic_data = cv2.CascadeClassifier('number_plate_cascade.xml')
images = os.listdir('car')

for image in images:
    try:
        car = cv2.imread(os.path.join('car', image))
        gray_car = cv2.cvtColor(car, cv2.COLOR_BGR2GRAY)
    except:
        print('can not convert', image)
        continue

    number = lic_data.detectMultiScale(gray_car)
    if len(number) == 0:
        print('no plate found', image)
        continue
    biggest_region = number[0]
    for numbers in number[1:]:
        if biggest_region[2] * biggest_region[3] < numbers[2] * numbers[3]:
            biggest_region = numbers

    (x, y, w, h) = biggest_region
    number_plate = gray_car[y:y + h, x:x + w]
    cv2.rectangle(car, (x, y), (x + w, y + h), (0, 255, 0), 3)
    cv2.imshow(image, car)
    # cv2.imshow('plate', number_plate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    text = pytesseract.image_to_string(number_plate, config='--psm 11')
    print(text)

from tkinter import *
from tkinter.filedialog import askopenfilename
import tkinter.font as font
from PIL import ImageTk, Image
import main
forget_list = []


def get_car_from_files():
    global forget_list
    for widget in forget_list:
        widget.pack_forget()
    forget_list = []

    car_location = askopenfilename()
    if car_location == '' or car_location is None:
        return

    base_height = 400
    img = Image.open(car_location)
    ratio = (base_height / float(img.size[1]))
    width = int((float(img.size[0]) * float(ratio)))
    img = img.resize((width, base_height), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.pack()

    space = Label(root)
    space.pack()

    license_number = main.get_license_number(car_location)
    license_label = Label(root, text=f'License Plate Number: {license_number}')
    license_font = font.Font(size=15)
    license_label['font'] = license_font
    license_label.pack()
    forget_list.extend([panel, space, license_label])


root = Tk()
root.geometry("800x600")
space = Label(root)
space.pack()
file_chooser_button = Button(root, text='Choose Car', command=get_car_from_files)
button_font = font.Font(size=15)
file_chooser_button['font'] = button_font
file_chooser_button.pack()
space = Label(root)
space.pack()
root.mainloop()

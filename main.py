#!/usr/bin/env python
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
from pyzbar import pyzbar
import cv2
from tkinter.filedialog import askopenfilename
import sys


class Window:

    def zbar(self, file_path):

        """
        Fields to be parsed:
        Brand
        Code no

        Part no
        Customer part no
        Lot no
        Quantity
        Date
        """
        image = cv2.imread(file_path)
        barcodes = pyzbar.decode(image)

        result = []

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            result.append(barcode_data)

            text = "{} ({})".format(barcode_data, barcode_type)
            cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        output = "\n".join(result)
        return output.split("\n")

    def parser(self):

        # writer file path in text label
        file_path = self.browse_file()

        list_of_codes = ["30P", "1T", "Q", "1P", "9D", "P", "K", "21L", "S", "4L", "10D"]
        zbar_output = self.zbar(file_path)

        print(zbar_output)

        fine_result = {}

        for code in list_of_codes:
            for barcode in zbar_output:
                if barcode.startswith(code):
                    barcode_ = barcode[len(code):]
                    fine_result['{}'.format(code.lower())] = barcode_
                    # print("CODE: {0} --> BARCODE: {1}".format(code, barcodes))
                    break
                else:
                    pass
                    # print('{} = Not Found!'.format(code.lower()))

        self.text_label['text'] = file_path
        self.results1['text'] = fine_result['1p']
        self.results2['text'] = fine_result['p']
        self.results3['text'] = fine_result['q']
        self.results4['text'] = fine_result['1t']
        self.results5['text'] = fine_result['10d']

    def browse_file(self):
        tk.Tk().withdraw()
        file_path = askopenfilename()
        return file_path

    def clear_widget_text(self, widget):
        widget['text'] = ""

    def __init__(self, master):
        height = 400
        width = 500
        bg_color = '#485885'

        C = tk.Canvas(boss, height=height, width=width)
        self.background_image = tk.PhotoImage(file='./t2.png')
        background_label = tk.Label(boss, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        C.pack()

        frame = tk.LabelFrame(boss, bg=bg_color, bd=10)
        frame.place(relx=0.5, rely=0.07, relwidth=0.75, relheight=0.2, anchor='n')

        # frame1 = tk.Frame(boss, bg='#3d4142', bd=5)
        # frame1.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor='n')
        # frame_window = C.create_window(100, 40, window=frame)

        # self.textbox = tk.Entry(self.frame, font=40, bg='#b8c3c8')
        # self.textbox.place(relwidth=0.65, relheight=1)

        self.text_label = tk.Label(frame, anchor='sw', justify='left', bd=10)
        self.text_label.config(font=40, bg='#ffffff', fg=bg_color)
        self.text_label.place(relx=0.25, rely=0.47, relwidth=0.74, relheight=0.4)

        path_text = tk.Label(frame, text="File Path: ", anchor='sw', justify='left', bg=bg_color,
                             fg="white")
        path_text.place(relx=0.04, rely=0.47, relwidth=0.19, relheight=0.4)

        submit = tk.Button(frame, text='Browse', font=40, bg=bg_color, fg=bg_color, command=lambda: self.parser())
        submit.place(relx=0.02, rely=0.06, relwidth=0.3, relheight=0.3)
        clear = tk.Button(frame, text="Clear", fg=bg_color, command=lambda: [
            self.clear_widget_text(self.text_label), self.clear_widget_text(self.results1),
            self.clear_widget_text(self.results2), self.clear_widget_text(self.results3),
            self.clear_widget_text(self.results4), self.clear_widget_text(self.results5)])

        clear.place(relx=0.355, rely=0.06, relwidth=0.3, relheight=0.3)
        quit = tk.Button(frame, text="Quit", fg=bg_color, command=lambda: sys.exit(1))
        quit.place(relx=0.69, rely=0.06, relwidth=0.3, relheight=0.3)

        # self.bbutton = tk.Button(self.frame1, text="Read", command=lambda: self.zbar())
        # self.bbutton.place(relx=0.7, relheight=1, relwidth=0.3)

        # lower_frame = tk.Frame(boss, bg='#3d4142', bd=10)
        # lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.5, anchor='')

        lower_frame = tk.LabelFrame(boss, fg="white", font=14, text="  Results  ", bg=bg_color, bd=15)
        lower_frame.pack(fill="both", expand="yes")
        lower_frame.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.6, anchor='n')

        results1_text = tk.Label(lower_frame, text="Part No: ", anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results1_text.place(relx=0.04, rely=0.04, relwidth=0.4, relheight=0.15)

        results2_text = tk.Label(lower_frame, text="Customer Part No: ", anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results2_text.place(relx=0.04, rely=0.23, relwidth=0.4, relheight=0.15)

        results3_text = tk.Label(lower_frame, text="Quantity: ", anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results3_text.place(relx=0.04, rely=0.42, relwidth=0.4, relheight=0.15)

        results4_text = tk.Label(lower_frame, text="Lot No: ", anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results4_text.place(relx=0.04, rely=0.61, relwidth=0.4, relheight=0.15)

        results5_text = tk.Label(lower_frame, text="Date: ", anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results5_text.place(relx=0.04, rely=0.80, relwidth=0.4, relheight=0.15)

        self.results1 = tk.Label(lower_frame, anchor='sw', justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results1.place(relx=0.49, rely=0.04, relwidth=0.5, relheight=0.15)

        self.results2 = tk.Label(lower_frame, anchor='sw', justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results2.place(relx=0.49, rely=0.23, relwidth=0.5, relheight=0.15)

        self.results3 = tk.Label(lower_frame, anchor='sw', justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results3.place(relx=0.49, rely=0.42, relwidth=0.5, relheight=0.15)

        self.results4 = tk.Label(lower_frame, anchor='sw', justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results4.place(relx=0.49, rely=0.61, relwidth=0.5, relheight=0.15)

        self.results5 = tk.Label(lower_frame, anchor='sw', justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results5.place(relx=0.49, rely=0.80, relwidth=0.5, relheight=0.15)


boss = tk.Tk()
boss.title("B-OSS")
window = Window(boss)
boss.protocol("WM_DELETE_WINDOW", lambda: sys.exit(1))
boss.mainloop()

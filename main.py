#!/usr/bin/env python
import sys
try:
    from Tkinter import *
except ImportError:
    try:
        from Tkinter import Tk
    except:
        # If no versions of tkinter exist (most likely linux) provide a message
        if sys.version_info.major < 3:
            print("Error: Tkinter not found")
            print('For linux, you can install Tkinter by executing: "sudo apt-get install python-tk"')
            sys.exit(1)
        else:
            print("Error: tkinter not found")
            print('For linux, you can install tkinter by executing: "sudo apt-get install python3-tk"')
            sys.exit(1)
try:
    from tkinter.filedialog import askopenfilename, askdirectory, askopenfilenames
except ImportError:
    from tkFileDialog import askopenfilename, askdirectory, askopenfilenames

from pyzbar import pyzbar
import cv2
import os


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
        self.text_label['text'] = file_path

        list_of_codes = ["30P", "1T", "Q", "1P", "9D", "P", "K", "21L", "S", "4L", "10D", "D"]
        zbar_output = self.zbar(file_path)

        self.fine_result = {}

        for code in list_of_codes:
            for barcode in zbar_output:
                if barcode.startswith(code):
                    barcode_ = barcode[len(code):]
                    self.fine_result['{}'.format(code.lower())] = barcode_
                    # print("CODE: {0} --> BARCODE: {1}".format(code, barcodes))
                    break
                else:
                    pass
                    # print('{} = Not Found!'.format(code.lower()))

        # part no parse
        part_no_codes = ['1p']
        part_no_code = ''.join(filter(lambda x: x in part_no_codes, self.fine_result.keys()))
        part_no = self.not_found(part_no_code)

        # customer part no parse
        cus_part_no_codes = ['p']
        cus_part_no_code = ''.join(filter(lambda x: x in cus_part_no_codes, self.fine_result.keys()))
        cus_part_no = self.not_found(cus_part_no_code)

        # quantity parse
        quantity_codes = ['q']
        quantity_code = ''.join(filter(lambda x: x in quantity_codes, self.fine_result.keys()))
        quantity = self.not_found(quantity_code)

        # lot no parse
        lot_no_codes = ['1t']
        lot_no_code = ''.join(filter(lambda x: x in lot_no_codes, self.fine_result.keys()))
        lot_no = self.not_found(lot_no_code)

        # parse date
        date_of_codes = ['9d', '10d', 'd']
        date_code = ''.join(filter(lambda x: x in date_of_codes, self.fine_result.keys()))
        date = self.not_found(date_code)

        self.results1['text'] = part_no
        self.results2['text'] = cus_part_no
        self.results3['text'] = quantity
        self.results4['text'] = lot_no
        self.results5['text'] = date

    def not_found(self, code):
        if code == '':
            return 'Not Found'
        else:
            return self.fine_result[code]

    def browse_file(self):
        Tk().withdraw()
        file_path = askopenfilename()
        return file_path

    def clear_widget_text(self, widget):
        widget['text'] = ""

    def __init__(self, master):

        boss.minsize(width=700, height=600)
        boss.maxsize(width=700, height=600)
        bg_color = '#485885'

        C = Canvas(boss)
        #self.background_image = PhotoImage(file='./t2.png')
        background_label = Label(boss, bg=bg_color)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        C.pack()

        frame = LabelFrame(boss, bg=bg_color, bd=10)
        frame.place(relx=0.5, rely=0.07, relwidth=0.75, relheight=0.2, anchor='n')

        # frame1 = Frame(boss, bg='#3d4142', bd=5)
        # frame1.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor='n')
        # frame_window = C.create_window(100, 40, window=frame)

        # self.textbox = Entry(self.frame, font=40, bg='#b8c3c8')
        # self.textbox.place(relwidth=0.65, relheight=1)

        self.text_label = Label(frame, anchor='sw', justify='left', bd=10)
        self.text_label.config(font=40, bg='#ffffff', fg=bg_color)
        self.text_label.place(relx=0.25, rely=0.47, relwidth=0.74, relheight=0.4)

        path_text = Label(frame, text="File Path: ", anchor='sw', justify='left', bg=bg_color,
                             fg="white")
        path_text.place(relx=0.04, rely=0.47, relwidth=0.19, relheight=0.4)

        submit = Button(frame, text='Browse', font=40, fg=bg_color, command=lambda: self.parser())
        submit.place(relx=0.02, rely=0.06, relwidth=0.3, relheight=0.3)
        clear = Button(frame, text="Clear", font=40, fg=bg_color, bg=bg_color, command=lambda: [
            self.clear_widget_text(self.text_label), self.clear_widget_text(self.results1),
            self.clear_widget_text(self.results2), self.clear_widget_text(self.results3),
            self.clear_widget_text(self.results4), self.clear_widget_text(self.results5)])

        clear.place(relx=0.355, rely=0.06, relwidth=0.3, relheight=0.3)
        quit = Button(frame, text="Quit", font=40, fg=bg_color, command=lambda: sys.exit(1))
        quit.place(relx=0.69, rely=0.06, relwidth=0.3, relheight=0.3)

        # self.bbutton = Button(self.frame1, text="Read", command=lambda: self.zbar())
        # self.bbutton.place(relx=0.7, relheight=1, relwidth=0.3)

        # lower_frame = Frame(boss, bg='#3d4142', bd=10)
        # lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.5, anchor='')

        lower_frame = LabelFrame(boss, fg="white", font=14, text="  Results  ", bg=bg_color, bd=15)
        lower_frame.pack(fill="both", expand="yes")
        lower_frame.place(relx=0.5, rely=0.32, relwidth=0.75, relheight=0.6, anchor='n')

        results1_text = Label(lower_frame, text="Part No: ", font=40, anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results1_text.place(relx=0.04, rely=0.04, relwidth=0.4, relheight=0.15)

        results2_text = Label(lower_frame, text="Customer Part No: ", font=40, anchor='sw', justify='left',
                                 bg=bg_color, fg="white")
        results2_text.place(relx=0.04, rely=0.23, relwidth=0.4, relheight=0.15)

        results3_text = Label(lower_frame, text="Quantity: ", font=40, anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results3_text.place(relx=0.04, rely=0.42, relwidth=0.4, relheight=0.15)

        results4_text = Label(lower_frame, text="Lot No: ", font=40, anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results4_text.place(relx=0.04, rely=0.61, relwidth=0.4, relheight=0.15)

        results5_text = Label(lower_frame, text="Date: ", font=40, anchor='sw', justify='left', bg=bg_color,
                                 fg="white")
        results5_text.place(relx=0.04, rely=0.80, relwidth=0.4, relheight=0.15)

        self.results1 = Label(lower_frame, anchor='sw', font=40, justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results1.place(relx=0.49, rely=0.04, relwidth=0.5, relheight=0.15)

        self.results2 = Label(lower_frame, anchor='sw', font=40, justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results2.place(relx=0.49, rely=0.23, relwidth=0.5, relheight=0.15)

        self.results3 = Label(lower_frame, anchor='sw', font=40, justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results3.place(relx=0.49, rely=0.42, relwidth=0.5, relheight=0.15)

        self.results4 = Label(lower_frame, anchor='sw', font=40, justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results4.place(relx=0.49, rely=0.61, relwidth=0.5, relheight=0.15)

        self.results5 = Label(lower_frame, anchor='sw', font=40, justify='left', fg=bg_color, bd=10)
        # self.results.config(font=40, bg=bg_color)
        self.results5.place(relx=0.49, rely=0.80, relwidth=0.5, relheight=0.15)


boss = Tk()
boss.title("B-OSS")
window = Window(boss)
boss.protocol("WM_DELETE_WINDOW", lambda: sys.exit(1))
boss.mainloop()

import tkinter as tk
from pyzbar import pyzbar
import cv2
from tkinter.filedialog import askopenfilename


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
        file_path = self.browsefile()

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
        self.results['text'] = 'Part No: {0} \nCustomer Part No: {1} \nQuantity: {2} \nLot No: {3} \nDate: {4}' \
            .format(fine_result['1p'], fine_result['p'], fine_result['q'], fine_result['1t'], fine_result['10d'])

    def browsefile(self):
        tk.Tk().withdraw()
        file_path = askopenfilename()
        return file_path

    def __init__(self, master):
        height = 500
        width = 500

        C = tk.Canvas(boss, height=height, width=width)
        self.background_image = tk.PhotoImage(file='./t2.png')
        background_label = tk.Label(boss, image=self.background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        C.pack()

        frame = tk.Frame(boss, bg='#3d4142', bd=5)
        frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

        frame1 = tk.Frame(boss, bg='#3d4142', bd=5)
        frame1.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.1, anchor='n')
        # frame_window = C.create_window(100, 40, window=frame)

        # self.textbox = tk.Entry(self.frame, font=40, bg='#b8c3c8')
        # self.textbox.place(relwidth=0.65, relheight=1)

        self.text_label = tk.Label(frame, anchor='nw', justify='left', bd=10)
        self.text_label.config(font=40, bg='#ffffff')
        self.text_label.place(relwidth=0.65, relheight=1)

        submit = tk.Button(frame, text='Browse', font=40, bg='#b8c3c8', command=lambda: self.parser())
        # submit.config(font=)
        submit.place(relx=0.7, relheight=1, relwidth=0.3)

        # self.bbutton = tk.Button(self.frame1, text="Read", command=lambda: self.zbar())
        # self.bbutton.place(relx=0.7, relheight=1, relwidth=0.3)

        lower_frame = tk.Frame(boss, bg='#3d4142', bd=3)
        lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

        bg_color = '#ffffff'
        self.results = tk.Label(lower_frame, anchor='nw', justify='left', bd=10)
        self.results.config(font=40, bg=bg_color)
        self.results.place(relwidth=1, relheight=1)

        weather_icon = tk.Canvas(self.results, bg=bg_color, bd=20, highlightthickness=20)
        weather_icon.place(relx=0.75, rely=0, relwidth=1, relheight=0.5)


boss = tk.Tk()
boss.title("B-OSS")
window = Window(boss)
boss.mainloop()

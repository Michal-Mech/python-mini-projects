import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import Image, ImageTk
import qrcode

# Import Windows-specific module for title bar customization
# On Linux/Mac this import will fail and the default title bar will be used.
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass

# Constants
# Window settings
WINDOW_SIZE = '450x450'
QR_SIZE = 400

# Colors used in the app
PRIMARY_COLOR = '#021FB3'
SECONDARY_COLOR = '#2E54E8'
HOVER_COLOR = '#4266f1'
BG_COLOR = 'white'
TEXT_COLOR = 'white'
TITLE_BAR_COLOR = 0x00FFFFFF

class App(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode('light')
        super().__init__(fg_color=BG_COLOR)
        self.title_bar_color()

        self.geometry(WINDOW_SIZE)
        self.title('')

        # raw_image - PIL image (used for saving to file)
        # tk_image - Tkinter image (used for displaying on canvas)
        self.raw_image = None
        self.tk_image = None

        # Text input - generates QR on every change
        self.entry_string = ctk.StringVar()
        self.entry_string.trace_add('write', self.create_qr)

        # UI
        EntryFiled(self,self.entry_string,self.save)
        self.qr_image = QrImage(self)

        # Enter key shortcut for saving
        self.bind('<Return>', self.save)

    #run
    def run(self):
        self.mainloop()

    # Generate and display QR code when text changes
    def create_qr(self,*args):
        current_text = self.entry_string.get()
        if current_text:
            self.raw_image = qrcode.make(current_text).resize((QR_SIZE, QR_SIZE))
            self.tk_image = ImageTk.PhotoImage(self.raw_image)
            self.qr_image.update_image(self.tk_image)
        else:
            self.qr_image.clear()
            self.raw_image = None
            self.tk_image = None

    # Open save dialog and write QR to chosen file
    def save(self, event=''):
        if self.raw_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension='.png',
                filetypes=[
                    ('PNG image', '*.png'),
                    ('JPEG image', '*.jpg'),
                    ('All files', '*.*'),
                ]
            )
            if file_path:
                self.raw_image.save(file_path)

    # Set white title bar
    def title_bar_color(self):
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 35, byref(c_int(TITLE_BAR_COLOR)), sizeof(c_int)
            )
        except Exception as e:
            print(f"Title bar color error: {e}")

class EntryFiled(ctk.CTkFrame):
    def __init__(self,parent,entry_string,save_function):
        super().__init__(master=parent, corner_radius=20, fg_color=PRIMARY_COLOR)
        self.place(relx=0.5, rely=1.0, relwidth=1, relheight=0.4, anchor='center')

        # Layout
        self.rowconfigure((0,1),weight=1,uniform="a")
        self.columnconfigure(0,weight=1,uniform="a")

        # Widgets
        self.frame = ctk.CTkFrame(self,fg_color= 'transparent')
        self.frame.columnconfigure(0,weight=1,uniform="b")
        self.frame.columnconfigure(1,weight=4,uniform="b")
        self.frame.columnconfigure(2,weight=2,uniform="b")
        self.frame.columnconfigure(3,weight=1,uniform="b")
        self.frame.grid(row=0,column=0)

        entry = ctk.CTkEntry(
            self.frame,
            textvariable=entry_string,
            fg_color=SECONDARY_COLOR,
            border_width=0,
            text_color=TEXT_COLOR,
        )
        entry.grid(row=0, column=1, sticky='nsew')

        button = ctk.CTkButton(
            self.frame,
            text='Save',
            fg_color=SECONDARY_COLOR,
            hover_color=HOVER_COLOR,
            command=save_function,
        )
        button.grid(row=0, column=2, sticky='nsew', padx=10)

class QrImage(tk.Canvas):
    def __init__(self,parent):
        super().__init__(
            master=parent,
            background=BG_COLOR,
            bd=0,
            highlightthickness=0,
            relief='ridge',
        )
        self.place(relx=0.5, rely=0.4, width=QR_SIZE, height=QR_SIZE, anchor='center')

    def update_image(self,image_tk):
        self.clear()
        self.create_image(0,0,image=image_tk,anchor='nw')

    def clear(self):
        self.delete('all')

if __name__ == '__main__':
    app = App()
    app.run()
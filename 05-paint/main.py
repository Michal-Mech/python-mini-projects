import customtkinter as ctk
from drawing_area import DrawingArea


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title(' ')
        self.iconbitmap('images/empty.ico')
        ctk.set_appearance_mode('light')

        #widgets
        DrawingArea(self)


    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()
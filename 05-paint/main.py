import customtkinter as ctk
from drawing_area import DrawingArea


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x600')
        self.title(' ')
        self.iconbitmap('images/empty.ico')
        ctk.set_appearance_mode('light')

        # data
        self.color_string = ctk.StringVar(value='000')
        self.brush_float = ctk.DoubleVar(value = 0.2)


        #widgets
        DrawingArea(self,self.color_string,self.brush_float)


    def run(self):
        self.mainloop()

if __name__ == '__main__':
    app = App()
    app.run()
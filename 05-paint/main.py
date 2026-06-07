import customtkinter as ctk
from drawing_area import DrawingArea
from tools import ToolPanel


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
        ToolPanel(self,self.brush_float,self.color_string)

        # mousewheel event
        self.bind('<MouseWheel>',self.adjust_brush_size)

    def run(self):
        self.mainloop()

    def adjust_brush_size(self,event):
        direction =  int(event.delta / abs(event.delta))
        new_brush_size = self.brush_float.get() + 0.05 * direction

        new_brush_size = max(0.2,min(1,new_brush_size))
        self.brush_float.set(new_brush_size)

if __name__ == '__main__':
    app = App()
    app.run()
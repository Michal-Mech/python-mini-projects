import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageGrab
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
        self.erase_bool = ctk.BooleanVar()


        #widgets
        self.draw_area = DrawingArea(self,self.color_string,self.brush_float,self.erase_bool)
        self.tool_panel = ToolPanel(self, self.brush_float, self.color_string, self.erase_bool,self.clear_canvas, self.save_canvas)
        self.erase_bool.set(False)

        # mousewheel event
        self.bind('<MouseWheel>',self.adjust_brush_size)

    def run(self):
        self.mainloop()

    def adjust_brush_size(self,event):
        direction =  int(event.delta / abs(event.delta))
        new_brush_size = self.brush_float.get() + 0.05 * direction

        new_brush_size = max(0.2,min(1,new_brush_size))
        self.brush_float.set(new_brush_size)

    def clear_canvas(self):
        self.draw_area.delete('all')

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension='.png',
            filetypes=[
                ('PNG image', '*.png'),
                ('JPEG image', '*.jpg'),
                ('All files', '*.*'),
            ]
        )

        if not file_path:
            return

        self.tool_panel.withdraw()
        self.update()
        self.after(500)

        x = self.draw_area.winfo_rootx()
        y = self.draw_area.winfo_rooty()
        width = self.draw_area.winfo_width()
        height = self.draw_area.winfo_height()

        image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        self.tool_panel.deiconify()
        image.save(file_path)

if __name__ == '__main__':
    app = App()
    app.run()
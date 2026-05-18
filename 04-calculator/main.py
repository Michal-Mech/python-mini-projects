import customtkinter as ctk
import darkdetect
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        super().__init__(fg_color= (WHITE,BLACK))
        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')
        self.iconbitmap('empty.ico')
        self.title_bar_color(is_dark)

        self.mainloop()

    def title_bar_color(self,is_dark):
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            color = TITLE_BAR_HEX_COLORS['dark' if is_dark else TITLE_BAR_HEX_COLORS['light']]
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 35, byref(c_int(color)), sizeof(c_int)
            )
        except Exception as e:
            print(f"Title bar color error: {e}")

if __name__ == '__main__':
    Calculator(darkdetect.isDark())
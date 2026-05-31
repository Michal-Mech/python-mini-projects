import customtkinter as ctk
from buttons import Button, ImageButton, NumButton,MathButton,MathImageButton
import darkdetect
from PIL import Image
from settings import *
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass

class Calculator(ctk.CTk):
    def __init__(self, is_dark):
        # Window setup, colors adapt to system theme - light or dark
        super().__init__(fg_color= (WHITE,BLACK))
        ctk.set_appearance_mode(f'{"dark" if is_dark else "light"}')
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
        self.resizable(False, False)
        self.title('')
        self.iconbitmap('empty.ico')
        self.title_bar_color(is_dark)

        # Layout: 4 columns x 7 rows
        self.rowconfigure(list(range(MAIN_ROWS)), weight=1,uniform='a')
        self.columnconfigure(list(range(MAIN_COLUMNS)), weight=1,uniform='a')

        # Calculator state
        self.result_string = ctk.StringVar(value = '0')
        self.formula_string = ctk.StringVar(value = '')
        self.display_nums = []
        self.full_operation = []

        #widgets
        self.create_widgets()

    # Build all buttons and labels
    def create_widgets(self):
        # Fonts
        main_font = ctk.CTkFont(family= FONT, size= NORMAL_FONT_SIZE)
        result_font = ctk.CTkFont(family= FONT, size= OUTPUT_FONT_SIZE)

        # Two displays: formula on top and current result below
        OutputLabel(self, 0,"SE",main_font,self.formula_string)
        OutputLabel(self, 1,"E",result_font,self.result_string)

        # AC button
        Button(parent= self,
               func= self.clear,
               text =OPERATORS['clear']['text'],
               col=OPERATORS['clear']['col'],
               row=OPERATORS['clear']['row'],
               font =main_font,
               )

        # Percentage button
        Button(parent=self,
               func=self.percent,
               text=OPERATORS['percent']['text'],
               col=OPERATORS['percent']['col'],
               row=OPERATORS['percent']['row'],
               font=main_font,
               )

        # Invert button
        invert_image = ctk.CTkImage(
            light_image= Image.open(OPERATORS['invert']['image path']['dark']),
            dark_image= Image.open(OPERATORS['invert']['image path']['light'])
        )
        ImageButton(parent=self,
                    func = self.invert,
                    col = OPERATORS['invert']['col'],
                    row = OPERATORS['invert']['row'],
                    image = invert_image
                    )

        # Number Buttons
        for num, data in NUM_POSITIONS.items():
            NumButton(parent=self,
                      text = num,
                      func = self.num_press,
                      col = data['col'],
                      row= data['row'],
                      font = main_font,
                      span= data['span']
                      )

        # Math operator buttons (+, -, *, /, =)
        for operator, data in MATH_POSITIONS.items():
            if data['image path']:
                divide_image = ctk.CTkImage(
                    light_image= Image.open(data['image path']['dark']),
                    dark_image= Image.open(data['image path']['light']),
                )

                MathImageButton(parent=self,
                           operator = operator,
                           func = self.math_press,
                           col = data['col'],
                           row = data['row'],
                           image = divide_image
                           )
            else:
                MathButton(parent=self,
                       text = data['character'],
                       operator = operator,
                       func = self.math_press,
                       col = data['col'],
                       row= data['row'],
                       font = main_font,
                       )
    # operator press logic (+, -, *, /, =)
    def math_press(self,value):
        current_number = ''.join(self.display_nums)
        if current_number:
            self.full_operation.append(current_number)

            if value != '=':
                # Add operator to formula, prepare for next number
                self.full_operation.append(value)
                self.display_nums.clear()

                # update output
                self.result_string.set('')
                self.formula_string.set(' '.join(self.full_operation))

            else:
                # Calculate result on '='
                formula = ' '.join(self.full_operation)

                try:
                    result = eval(formula)  # albo twoja własna implementacja
                except ZeroDivisionError:
                    self.result_string.set('Error')
                    self.full_operation.clear()
                    self.display_nums.clear()
                    return

                # Format: remove .0 from integers, round long decimals
                if isinstance(result, float):
                    if result.is_integer():
                        result = int(result)
                    else:
                        result = round(result, 8)

                # Save result as new starting number for next operation
                self.full_operation.clear()
                self.display_nums = [str(result)]

                # Output update
                self.result_string.set(result)
                self.formula_string.set(formula)

    # Handle numbers and '.' press (0-9, .)
    def num_press(self,value):
        self.display_nums.append(str(value))
        full_number = ''.join(self.display_nums)
        self.result_string.set(full_number)

    # Clear everything (AC button)
    def clear(self):
        self.result_string.set(0)
        self.formula_string.set('')

        self.display_nums.clear()
        self.full_operation.clear()

    # Convert current number to percentage
    def percent(self):
        if self.display_nums:
            current_number = float(''.join(self.display_nums))
            percent_number = current_number / 100

            self.display_nums = list(str(percent_number))
            self.result_string.set(''.join(self.display_nums))

    # Toggle sign of current number ('+' or '-')
    def invert(self):
        current_number = ''.join(self.display_nums)
        if current_number:
            if float(current_number) > 0:
                self.display_nums.insert(0,'-')
            else:
                del self.display_nums[0]

            self.result_string.set(''.join(self.display_nums))

    # Set title bar color (Windows 11 only)
    def title_bar_color(self, is_dark):
        try:
            hwnd = windll.user32.GetParent(self.winfo_id())
            color = TITLE_BAR_HEX_COLORS['dark' if is_dark else 'light']
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 35, byref(c_int(color)), sizeof(c_int)
            )
        except Exception as e:
            print(f"Title bar color error: {e}")

    def run(self):
        self.mainloop()

class OutputLabel(ctk.CTkLabel):
    def __init__(self, parent,row,anchor,font,string_var):
        super().__init__(master = parent, font=font,textvariable = string_var)
        self.grid(column=0,columnspan = 4,row=row,sticky=anchor, padx = 10)

if __name__ == '__main__':
    app = Calculator(darkdetect.isDark())
    app.run()
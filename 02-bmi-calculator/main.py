import customtkinter as ctk
from settings import *
# Import Windows-specific module for title bar customization
# On Linux/Mac this import will fail and the default title bar will be used.
try:
    from ctypes import windll, byref, sizeof, c_int
except ImportError:
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=GREEN)
        self.title('')
        self.iconbitmap('empty.ico')
        self.geometry('400x400')
        self.resizable(False, False)
        self.change_title_bar_color()

        # Grid layout: 1 column, 5 rows
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1, uniform='a')  # reset/metric buttons
        self.rowconfigure(1, weight=3, uniform='a')  # BMI value
        self.rowconfigure(2, weight=1, uniform='a')  # Category
        self.rowconfigure(3, weight=2, uniform='a')  # Weight input
        self.rowconfigure(4, weight=2, uniform='a')  # Height input

        # Data
        self.metric_bool = ctk.BooleanVar(value=True)
        self.height_int = ctk.IntVar(value=170)
        self.weight_float = ctk.DoubleVar(value=65)
        self.bmi_string = ctk.StringVar()
        self.category_string = ctk.StringVar()
        self.update_bmi()

        # Tracing, trigger updates when values change
        self.height_int.trace_add('write', self.update_bmi)
        self.weight_float.trace_add('write', self.update_bmi)
        self.metric_bool.trace_add('write', self.change_units)

        # widgets/UI components
        ResultText(self,self.bmi_string)
        CategoryText(self, self.category_string)
        self.weight_input = WeightInput(self,self.weight_float,self.metric_bool)
        self.height_input = HeightInput(self,self.height_int,self.metric_bool)
        UnitSwitch(self,self.metric_bool)
        ResetButton(self, self.reset)

    # Return (name, color) for given BMI value
    def get_bmi_category(self, bmi_value):
        for max_bmi, name, color in BMI_CATEGORIES:
            if bmi_value < max_bmi:
                return name, color
        return None

    # Refresh displayed weight and height when units change
    def change_units(self, *args):
        self.height_input.update_text(self.height_int.get())
        self.weight_input.update_weight()

    # Calculate BMI and update all related UI (text, color, title bar)
    def update_bmi(self, *args):
        height_meter = self.height_int.get() / 100
        weight_kg = self.weight_float.get()
        bmi_result = round(weight_kg / height_meter ** 2,2)
        self.bmi_string.set(str(bmi_result))

        category_name, color = self.get_bmi_category(bmi_result)
        self.category_string.set(category_name)
        self.configure(fg_color=color)
        self.change_title_bar_color(color)

    # Set title bar color (Windows 11 only)
    def change_title_bar_color(self,hex_color=GREEN):
        try:
            dwm_color = hex_to_dwm(hex_color)
            hwnd = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                hwnd, 35, byref(c_int(dwm_color)), sizeof(c_int)
            )
        except Exception as e:
            print(f"Title bar color error: {e}")

    # Reset all values to defaults
    def reset(self):
        self.height_int.set(DEFAULT_HEIGHT_CM)
        self.weight_float.set(DEFAULT_WEIGHT_KG)
        self.metric_bool.set(DEFAULT_METRIC)

    def run(self):
        self.mainloop()

# Big BMI value label
class ResultText(ctk.CTkLabel):
    def __init__(self, parent, bmi_string):
        font = ctk.CTkFont(family=FONT,size=MAIN_TEXT_SIZE,weight='bold')
        super().__init__(master=parent,font = font,text_color=WHITE,textvariable = bmi_string)
        self.grid(column=0, row=1, sticky='sew')

# Weight controls (label + plus/minus buttons)
class WeightInput(ctk.CTkFrame):
    def __init__(self, parent,weight_float,metric_bool):
        super().__init__(master = parent, fg_color=WHITE)
        self.grid(column=0, row=3, sticky='nsew', padx=10, pady=10)
        self.weight_float = weight_float
        self.metric_bool = metric_bool

        # Displayed weight (with unit)
        self.output_string = ctk.StringVar()
        self.update_weight()

        # Layout: 5 columns (big minus, small minus, label, small plus, big plus)
        self.rowconfigure(0, weight=1,uniform='b')
        self.columnconfigure(0, weight=2,uniform='b')
        self.columnconfigure(1, weight=1,uniform='b')
        self.columnconfigure(2, weight=3,uniform='b')
        self.columnconfigure(3, weight=1,uniform='b')
        self.columnconfigure(4, weight=2,uniform='b')

        # Weight display label
        font = ctk.CTkFont(family=FONT,size=INPUT_FONT_SIZE)
        label = ctk.CTkLabel(self,textvariable = self.output_string,text_color=BLACK,font=font)
        label.grid(row=0, column=2)

        # Buttons - large = 1 kg / 1 lb, small = 0.1 kg / 1 oz
        minus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('minus','large')) ,text='-',font=font, text_color=BLACK,fg_color=LIGHT_GRAY,hover_color=GRAY,corner_radius=BUTTON_CORNER_RADIUS)
        minus_button.grid(row=0, column=0,sticky='ns',padx=8,pady=8)

        plus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('plus','large')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY,corner_radius=BUTTON_CORNER_RADIUS)
        plus_button.grid(row=0, column=4, sticky='ns', padx=8, pady=8)

        small_plus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('plus','small')), text='+', font=font, text_color=BLACK, fg_color=LIGHT_GRAY, hover_color=GRAY,corner_radius=BUTTON_CORNER_RADIUS)
        small_plus_button.grid(row=0, column=3, padx=4, pady=4)

        small_minus_button = ctk.CTkButton(self, command= lambda: self.update_weight(('minus','small')), text='-', font=font, text_color=BLACK, fg_color=LIGHT_GRAY,hover_color=GRAY, corner_radius=BUTTON_CORNER_RADIUS)
        small_minus_button.grid(row=0, column=1, padx=4, pady=4)

    # Update weight value and refresh display
    def update_weight(self,info = None):
        if info:

            if self.metric_bool.get():
                amount = 1 if info[1] == 'large' else 0.1
            else:
                amount = KG_PER_POUND  if info[1] == 'large' else KG_PER_POUND /OUNCES_PER_POUND

            if info[0] == 'plus':
                new_weight = self.weight_float.get() + amount
            else:
                new_weight = self.weight_float.get() - amount

            # weight limit
            new_weight = max(MIN_WEIGHT_KG, min(MAX_WEIGHT_KG, new_weight))
            self.weight_float.set(new_weight)

        # Display in chosen unit
        if self.metric_bool.get():
            self.output_string.set(f'{round(self.weight_float.get(),2)} kg')
        else:
            raw_ounces = self.weight_float.get() * POUNDS_PER_KG * OUNCES_PER_POUND
            pounds, ounces = divmod(raw_ounces,OUNCES_PER_POUND )
            self.output_string.set(f'{int(pounds)}lb {int(ounces)}oz')

# Height controls (slider + label)
class HeightInput(ctk.CTkFrame):
    def __init__(self, parent,height_int,metric_bool):
        super().__init__(master = parent,fg_color=WHITE)
        self.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
        self.metric_bool =metric_bool

        # Slider for height (100-250 cm)
        slider = ctk.CTkSlider(
            master = self,
            command= self.update_text,
            button_color=GREEN,
            button_hover_color=GRAY,
            progress_color= GREEN,
            fg_color=LIGHT_GRAY,
            variable = height_int,
            from_=100,
            to=250,
        )
        slider.pack(side='left',fill="x", expand=True, padx=10, pady=10)

        # Displayed height with unit
        self.output_string = ctk.StringVar()
        self.update_text(height_int.get())

        output_text = ctk.CTkLabel(self,textvariable =self.output_string,text_color=BLACK,font = ctk.CTkFont(family=FONT,size=INPUT_FONT_SIZE))
        output_text.pack(side='left', padx=20)

    # Format height as 1.70m or 5'7" depending on units
    def update_text(self,amount):
        if self.metric_bool.get():
            text_string = str(int(amount))
            meter = text_string[0]
            cm = text_string[1:]
            self.output_string.set(f'{meter}.{cm}m')
        else:
            feet, inches = divmod(amount / CM_PER_INCH, INCHES_PER_FOOT )
            self.output_string.set(f'{int(feet)}\'{int(inches)}"')

# BMI category text below the BMI value
class CategoryText(ctk.CTkLabel):
    def __init__(self, parent, category_string):
        font = ctk.CTkFont(family=FONT, size=CATEGORY_FONT_SIZE, weight='bold')
        super().__init__(
            master=parent,
            font=font,
            text_color=WHITE,
            textvariable=category_string
        )
        self.grid(column=0, row=2, sticky='new', pady=(0, 20))

# Clickable "reset" label in top-left corner
class ResetButton(ctk.CTkLabel):
    def __init__(self, parent, reset_function):
        font = ctk.CTkFont(family=FONT, size=SWITCH_FONT_SIZE, weight='bold')
        super().__init__(
            master=parent,
            text='reset',
            text_color=DARK_GREEN,
            font=font
        )
        self.place(relx=0.02, rely=0.01, anchor='nw')

        self.bind('<Button>', lambda event: reset_function())

# Clickable "metric" or "imperial" label in top-right corner
class UnitSwitch(ctk.CTkLabel):
    def __init__(self, parent,metric_bool):
        super().__init__(
            master = parent,
            text='metric',
            text_color=DARK_GREEN,
            font = ctk.CTkFont(family=FONT,size=SWITCH_FONT_SIZE,weight='bold'))
        self.place(relx=0.98, rely=0.01, anchor='ne')

        self.metric_bool = metric_bool
        self.bind('<Button>', self.change_units)

    # Toggle between metric and imperial units
    def change_units(self,event):
        self.metric_bool.set(not self.metric_bool.get())

        if self.metric_bool.get():
            self.configure(text='metric')
        else:
            self.configure(text='imperial')

if __name__ == '__main__':
    app = App()
    app.run()
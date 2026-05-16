# text sizes
FONT = 'Calibri'
MAIN_TEXT_SIZE = 150
INPUT_FONT_SIZE = 26
SWITCH_FONT_SIZE = 18
CATEGORY_FONT_SIZE = 22
BUTTON_CORNER_RADIUS = 6

# BMI category colors
COLOR_UNDERWEIGHT = '#4A90E2'
COLOR_NORMAL = '#50BFAB'
COLOR_OVERWEIGHT = '#F5A623'
COLOR_OBESE = '#D0021B'

# UI colors
GREEN = '#50BFAB'
DARK_GREEN = '#3A8A7B'
WHITE = '#F2F2F2'
BLACK = '#1F1F1F'
LIGHT_GRAY = '#E8E8E8'
GRAY = '#D9D9D9'


# BMI category labels and ranges
BMI_CATEGORIES = [
    (18.5, 'Underweight', COLOR_UNDERWEIGHT),
    (25.0, 'Normal weight', COLOR_NORMAL),
    (30.0, 'Overweight', COLOR_OVERWEIGHT),
    (float('inf'), 'Obese', COLOR_OBESE),
]

# Default values for reset
DEFAULT_HEIGHT_CM = 170
DEFAULT_WEIGHT_KG = 65
DEFAULT_METRIC = True

# Units conversion
KG_PER_POUND = 0.453592
OUNCES_PER_POUND = 16
POUNDS_PER_KG = 2.20462
INCHES_PER_FOOT = 12
CM_PER_INCH = 2.54

# Weight limits
MIN_WEIGHT_KG = 30
MAX_WEIGHT_KG = 300

# Convert '#RRGGBB' to 0x00BBGGRR format used by Windows DWM API
def hex_to_dwm(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return (b << 16) | (g << 8) | r
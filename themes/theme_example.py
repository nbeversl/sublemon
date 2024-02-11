from sublemon.themes.colors import colors
from sublemon.themes.fonts import fonts

# example theme

theme_light = {   
    'name': 'Basic',
    'background_color' : colors['paper'],
    'foreground_color' : colors['grey6'],
    'font' : {
        'regular' : fonts['Courier New'],
        'bold' :    fonts['Courier New Bold'],
    },
    'autocompleter': {
        'background_color' : "#ffffff",
        'foreground_color' : "#000000",
        'search_field_background_color': colors['white'],
        'search_field_border_color': 'black',
    }
}
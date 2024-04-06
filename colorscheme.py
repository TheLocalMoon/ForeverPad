# colorscheme.py #
# color schemes for ForeverPad
import os
import json
import pylog

# logging
logging = pylog.log()

def get_color_scheme(bg, tab_bg, tab_fg, status_bar_bg, status_bar_fg, line_label_bg, line_label_fg):
    return {
        'root_bg': bg,
        'tab_bg': tab_bg,
        'tab_fg': tab_fg,
        'status_bar_bg': status_bar_bg,
        'status_bar_fg': status_bar_fg,
        'line_label_bg': line_label_bg,
        'line_label_fg': line_label_fg
    }

class ColorSchemes:
    SCHEMES = sorted([
        ('desert', '#3f3f3f', '#3f3f3f', 'white', '#202020', 'white', '#202020', 'white'),
        ('heaven', 'white', 'white', 'black', 'white', 'black', 'white', 'black'),
        ('sky', '#aaffff', '#aaffff', 'black', '#5f9ea0', 'white', '#5f9ea0', 'white'),
        ('forest', '#556B2F', '#556B2F', 'white', '#8FBC8F', 'black', '#8FBC8F', 'black'),
        ('ocean', '#1E90FF', '#1E90FF', 'white', '#4682B4', 'white', '#4682B4', 'white'),
        ('sunset', '#FF4500', '#FF4500', 'white', '#FF6347', 'white', '#FF6347', 'white'),
        ('night', '#191970', '#191970', 'white', '#000080', 'white', '#000080', 'white'),
        ('twilight', '#8A2BE2', '#8A2BE2', 'white', '#9932CC', 'white', '#9932CC', 'white'),
        ('dusk', '#2c3e50', '#34495e', 'white', '#2c3e50', 'white', '#34495e', 'white'),
        ('fire', '#ff5733', '#ff5733', 'white', '#c70039', 'white', '#c70039', 'white'),
        ('earth', '#8b4513', '#8b4513', 'white', '#a0522d', 'white', '#a0522d', 'white'),
        ('space', '#000000', '#000000', 'white', '#0a0a0a', 'white', '#0a0a0a', 'white'),
        ('spring', '#32cd32', '#32cd32', 'white', '#008000', 'white', '#008000', 'white'),
        ('hell', '#990000', '#990000', 'white', '#660000', 'white', '#660000', 'white'),
        ('aqua', '#00FFFF', '#00FFFF', 'black', '#00CED1', 'black', '#00CED1', 'black'),
        ('lavender', '#E6E6FA', '#E6E6FA', 'black', '#D8BFD8', 'black', '#D8BFD8', 'black'),
        ('sunrise', '#FFD700', '#FFD700', 'black', '#FFA500', 'black', '#FFA500', 'black'),
        ('moonlight', '#f0e68c', '#f0e68c', 'black', '#fffacd', 'black', '#fffacd', 'black'),
        ('leaf', '#7cfc00', '#7cfc00', 'black', '#adff2f', 'black', '#adff2f', 'black'),
        ('sand', '#deb887', '#deb887', 'black', '#f4a460', 'black', '#f4a460', 'black'),
        ('fog', '#dcdcdc', '#dcdcdc', 'black', '#f5f5f5', 'black', '#f5f5f5', 'black'),
        ('midnight', '#2F4F4F', '#2F4F4F', 'white', '#696969', 'white', '#696969', 'white'),
        ('ruby', '#E0115F', '#E0115F', 'white', '#FF69B4', 'white', '#FF69B4', 'white'),
        ('amber', '#FFBF00', '#FFBF00', 'black', '#FFD700', 'black', '#FFD700', 'black'),
        ('magenta', '#FF00FF', '#FF00FF', 'black', '#FF1493', 'black', '#FF1493', 'black'),
        ('cyan', '#00FFFF', '#00FFFF', 'black', '#00FFFF', 'black', '#00FFFF', 'black'),
        ('rose', '#FF007F', '#FF007F', 'white', '#FF007F', 'white', '#FF007F', 'white'),
        ('grass', '#7CFC00', '#7CFC00', 'black', '#7FFF00', 'black', '#7FFF00', 'black'),
        ('brick', '#8B0000', '#8B0000', 'white', '#B22222', 'white', '#B22222', 'white'),
        ('plum', '#DDA0DD', '#DDA0DD', 'black', '#DA70D6', 'black', '#DA70D6', 'black'),
        ('grey', '#808080', '#808080', 'black', '#A9A9A9', 'black', '#A9A9A9', 'black'),
        ('pink', '#FFC0CB', '#FFC0CB', 'black', '#FF69B4', 'black', '#FF69B4', 'black'),
        ('teal', '#008080', '#008080', 'white', '#008080', 'white', '#008080', 'white'),
        ('gold', '#FFD700', '#FFD700', 'black', '#FFD700', 'black', '#FFD700', 'black'),
        ('indigo', '#4B0082', '#4B0082', 'white', '#4B0082', 'white', '#4B0082', 'white'),
        ('violet', '#8A2BE2', '#8A2BE2', 'white', '#8A2BE2', 'white', '#8A2BE2', 'white'),
        ('coral', '#FF7F50', '#FF7F50', 'black', '#FF7F50', 'black', '#FF7F50', 'black'),
        ('ivory', '#FFFFF0', '#FFFFF0', 'black', '#FFFFF0', 'black', '#FFFFF0', 'black'),
        ('cyclamen', '#FF43A4', '#FF43A4', 'black', '#FF43A4', 'black', '#FF43A4', 'black'),
        ('olive', '#808000', '#808000', 'black', '#808000', 'black', '#808000', 'black'),
        ('electric', '#00FFFF', '#00FFFF', 'black', '#00CED1', 'black', '#00CED1', 'black'),
        ('sapphire', '#082567', '#082567', 'white', '#0F52BA', 'white', '#0F52BA', 'white'),
        ('ruby', '#E0115F', '#E0115F', 'white', '#FF69B4', 'white', '#FF69B4', 'white'),
        ('emerald', '#50C878', '#50C878', 'black', '#008000', 'black', '#008000', 'black'),
        ('amethyst', '#9966CC', '#9966CC', 'black', '#9932CC', 'black', '#9932CC', 'black'),
        ('topaz', '#FFD700', '#FFD700', 'black', '#4A646C', 'black', '#4A646C', 'black'),
        ('pearl', '#F0F0F0', '#F0F0F0', 'black', '#E0E0E0', 'black', '#E0E0E0', 'black'),
        ('jasper', '#D73B3E', '#D73B3E', 'white', '#A31621', 'white', '#A31621', 'white'),
        ('agate', '#B8B8B8', '#B8B8B8', 'black', '#808080', 'black', '#808080', 'black'),
        ('turquoise', '#40E0D0', '#40E0D0', 'black', '#00CED1', 'black', '#00CED1', 'black'),
        ('azure', '#F0FFFF', '#F0FFFF', 'black', '#007FFF', 'black', '#007FFF', 'black'),
        ('onyx', '#0F0F0F', '#0F0F0F', 'white', '#1A1A1A', 'white', '#1A1A1A', 'white'),
        ('opal', '#87CEEB', '#87CEEB', 'black', '#B0E0E6', 'black', '#B0E0E6', 'black'),
        ('corundum', '#FF4500', '#FF4500', 'white', '#B22222', 'white', '#B22222', 'white'),
        ('malachite', '#0BDA51', '#0BDA51', 'black', '#007200', 'black', '#007200', 'black'),
        ('tanzanite', '#0D1F2D', '#0D1F2D', 'white', '#242E38', 'white', '#242E38', 'white'),
        ('peridot', '#E6E200', '#E6E200', 'black', '#C5B358', 'black', '#C5B358', 'black'),
        ('moonstone', '#C0C0C0', '#C0C0C0', 'black', '#D3D3D3', 'black', '#D3D3D3', 'black'),
        ('jade', '#00A86B', '#00A86B', 'black', '#00FF7F', 'black', '#00FF7F', 'black'),
        ('ruby', '#E0115F', '#E0115F', 'white', '#FF69B4', 'white', '#FF69B4', 'white'),
        ('sardonyx', '#8B0000', '#8B0000', 'white', '#A52A2A', 'white', '#A52A2A', 'white'),
        ('selenite', '#F5FFFA', '#F5FFFA', 'black', '#D3D3D3', 'black', '#D3D3D3', 'black'),
        ('citrine', '#E4D00A', '#E4D00A', 'black', '#FFD700', 'black', '#FFD700', 'black'),
        ('lapis', '#007FFF', '#007FFF', 'white', '#4169E1', 'white', '#4169E1', 'white'),
        ('garnet', '#800000', '#800000', 'white', '#6B1111', 'white', '#6B1111', 'white'),
        ('quartz', '#FFFFFF', '#FFFFFF', 'black', '#F5F5F5', 'black', '#F5F5F5', 'black'),
        ('agate', '#B8B8B8', '#B8B8B8', 'black', '#808080', 'black', '#808080', 'black'),
        ('carnelian', '#B31B1B', '#B31B1B', 'white', '#FF4500', 'white', '#FF4500', 'white'),
        ('jacinth', '#FF4500', '#FF4500', 'white', '#B22222', 'white', '#B22222', 'white'),
        ('turquoise', '#40E0D0', '#40E0D0', 'black', '#00CED1', 'black', '#00CED1', 'black'),
        ('opal', '#87CEEB', '#87CEEB', 'black', '#B0E0E6', 'black', '#B0E0E6', 'black'),
        ('corundum', '#FF4500', '#FF4500', 'white', '#B22222', 'white', '#B22222', 'white'),
        ('malachite', '#0BDA51', '#0BDA51', 'black', '#007200', 'black', '#007200', 'black'),
        ('tanzanite', '#0D1F2D', '#0D1F2D', 'white', '#242E38', 'white', '#242E38', 'white'),
        ('peridot', '#E6E200', '#E6E200', 'black', '#C5B358', 'black', '#C5B358', 'black'),
        ('moonstone', '#C0C0C0', '#C0C0C0', 'black', '#D3D3D3', 'black', '#D3D3D3', 'black'),
        ('jade', '#00A86B', '#00A86B', 'black', '#00FF7F', 'black', '#00FF7F', 'black'),
        ('sardonyx', '#8B0000', '#8B0000', 'white', '#A52A2A', 'white', '#A52A2A', 'white'),
        ('selenite', '#F5FFFA', '#F5FFFA', 'black', '#D3D3D3', 'black', '#D3D3D3', 'black'),
        ('citrine', '#E4D00A', '#E4D00A', 'black', '#FFD700', 'black', '#FFD700', 'black'),
        ('lapis', '#007FFF', '#007FFF', 'white', '#4169E1', 'white', '#4169E1', 'white'),
        ('garnet', '#800000', '#800000', 'white', '#6B1111', 'white', '#6B1111', 'white'),
        ('quartz', '#FFFFFF', '#FFFFFF', 'black', '#F5F5F5', 'black', '#F5F5F5', 'black'),
        ('carnelian', '#B31B1B', '#B31B1B', 'white', '#FF4500', 'white', '#FF4500', 'white'),
        ('jacinth', '#FF4500', '#FF4500', 'white', '#B22222', 'white', '#B22222', 'white'),
    ])
    
    @classmethod
    def generate(cls):
        for name, *colors in cls.SCHEMES:
            setattr(cls, name.upper(), get_color_scheme(*colors))

    @staticmethod
    def load():
        for filename in os.listdir("colorschemes/"):
            if filename.endswith('.json'):
                variable_name = os.path.splitext(filename)[0].upper()
                with open(os.path.join("colorschemes/", filename), 'r') as file:
                    json_data = json.load(file)
                colors = tuple(json_data.values())
                setattr(ColorSchemes, variable_name, get_color_scheme(*colors))


ColorSchemes.generate()
ColorSchemes.load()
logging.info(f"loaded {len(ColorSchemes.SCHEMES)} color schemes")

delattr(ColorSchemes, 'load') # I HAVE THE POWER
delattr(ColorSchemes, 'generate') # I HAVE THE POWER
delattr(ColorSchemes, 'SCHEMES') # I HAVE THE POWER
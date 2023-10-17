"""
Function to create and write an eliptically shaped wordcloud in the Susmon colour palette
from a list of word frequencies.
"""
from wordcloud import WordCloud
import numpy as np
import random
from PIL import Image, ImageDraw
from matplotlib import colors as colours

colour_grad = ['#FFEBB0', '#FFDF91', '#FED272', '#FEC653', '#FDB934', '#FAA438', '#F88F3B', '#F57A3F', '#F36542', '#F05046']

def _hex_to_rgb(hex_string):
    rgb = colours.hex2color(hex_string)
    return tuple([int(255*x) for x in rgb])
    
    
def _susmon_colour_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """
    Funcion to return a colour from the Susmon colour palette
    removed (226,228,30) and (160,228,247) as being difficult to read, and (65,64,66)
    being too much like title text.
    """

    susmon_colours = [(109, 110, 113), (240, 80, 70), (150, 80, 150),
                      (141, 198, 63), (20, 190, 240), (35, 130, 202),
                      (0, 180, 170), (253, 185, 52)]

    return f"rgb{random.choice(susmon_colours)}"

def _susmon_alt_colour_func(word, font_size, position, orientation, random_state=None, **kwargs):
    """
    Funcion to return a colour from the Susmon colour palette
    removed (226,228,30) and (160,228,247) as being difficult to read, and (65,64,66)
    being too much like title text.
    """

    susmon_colours = []
    for colour in colour_grad:
        susmon_colours.append(_hex_to_rgb(colour))

    return f"rgb{random.choice(susmon_colours)}"


def create_and_write_wordcloud(frequencies, wcloud_file):
    # create an elliptical mask for our wordcloud
    w, h = 600, 450
    shape = [(20, 20), (w - 20, h - 20)]
    im = Image.new(mode="RGB", size=(w, h), color='white')
    im2 = ImageDraw.Draw(im)
    im2.ellipse(shape, fill='black', outline='black')
    mask = np.array(im)

    # Create the wordcloud object and write to file
    try:
        wordcloud = WordCloud(font_path="arial.ttf", background_color="white", color_func=_susmon_colour_func,
                              mask=mask, width=560, height=560, margin=0, max_words=20,
                              prefer_horizontal=1).generate_from_frequencies(frequencies)

        wordcloud.to_file(wcloud_file)
    except Exception as e:
        print(f"Unable to create wordcloud: {wcloud_file}\n" + str(e))

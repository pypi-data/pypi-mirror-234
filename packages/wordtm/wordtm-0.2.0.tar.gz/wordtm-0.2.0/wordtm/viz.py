# viz.py
#    
# WordTM: Show a wordcloud for a precribed range of Scripture
#
# Copyright (C) 2022-2023 WordTM Project
# Author: Johnny Cheng <johnnywfc@gmail.com>
# Updated: 28 June 2022
#
# URL:  nil
# For license information, see LICENSE.TXT

import numpy as np
from importlib_resources import files
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image

from wordjc import util


def plot_cloud(wordcloud):
    """Plot the prepared wordcloud"""
    plt.figure(figsize=(15, 10))
    plt.imshow(wordcloud) 
    plt.axis("off");


def show_wordcloud(text, image='heart.jpg', mask=None):
    """Prepare and show a wordcloud"""
    if image:
        img_file = files('wordjc.images').joinpath(image)
        mask = np.array(Image.open(img_file))

    wordcloud = WordCloud(background_color='black', colormap='Set2', mask=mask) \
                    .generate(text)

    plot_cloud(wordcloud)


def chi_wordcloud(df, image='heart.jpg', mask=None):
    """Prepare and show a Chinese wordcloud"""
    diction = util.get_diction(df)

    if image:
        img_file = files('wordjc.images').joinpath(image)
        mask = np.array(Image.open(img_file))

    font = 'msyh.ttc'
    wordcloud = WordCloud(background_color='black', colormap='Set2', \
	                                mask=mask, font_path=font) \
                            .generate_from_frequencies(frequencies=diction)

    plot_cloud(wordcloud)

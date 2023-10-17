import collections
import itertools
import os
import pathlib
import logging
from typing import List

import pandas as pd

from susclouds.new_cleaning import get_posts_text
from susclouds.stopword_funcs import stopwords_from_brands, get_brands, get_brand_owners
from susclouds.wordcloud_func import create_and_write_wordcloud

# configure some basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(__name__+".log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

def wordcloud_nz(source_file: os.path, phrases: pd.DataFrame, stopwords: List[str], output_dir: os.path):
    """
    generate and save ESG wordclouds
    :param source_file: path to the report file to be analysed
    :param phrases: a dataframe of phrases to be excluded [[check this]]
    :param stopwords: a list of stop words
    """

    logger.debug(f"creating wordclouds for issue for {str(source_file)}")
    wordsets = []
    brand_names = []
    issue_names = ["Emissions", "Materials", "Energy", "Waste", "Water", "Biodiversity", "T20 NZ"]

    if not output_dir.is_dir():
        os.makedirs(output_dir)

    # set output file
    output_file = str(output_dir) + "/netzero_wordcount_output.xlsx"
    
    """
    get a list of brand owners from the Followers sheet and then use the brand owner's names to
    derive additional stop words. We also need the list of brand owners to loop through
    creating word susclouds
    """
    followers = pd.read_excel(source_file, sheet_name="Followers", keep_default_na=False)
    brand_owners = get_brand_owners(followers)
    for brand_owner in brand_owners:
        stopwords.extend(stopwords_from_brands(brand_owner))

    """
    get a list of brands from the Followers sheet and then use the brand's names to
    derive additional stop words.
    """
    brands = get_brands(followers)
    for brand in brands:
        stopwords.extend(stopwords_from_brands(brand))

    # create word susclouds for the first 7 sheets
    for sheet_name in issue_names:
        print(f"working on sheet {sheet_name}")
        posts = pd.read_excel(source_file, sheet_name=sheet_name, keep_default_na=False)
        clean_text = get_posts_text(posts, "", "", phrases, stopwords)

        all_clean_words = list(itertools.chain(*clean_text))

        # Create counter
        word_counts = collections.Counter(all_clean_words)
        create_and_write_wordcloud(word_counts, str(output_dir) + f"/wc_{sheet_name}.png")

    # create top 20 word counts only for the next 20 sheets
    for sheet_num in range(1, 21):

        posts = pd.read_excel(source_file, sheet_name=f"{sheet_num} Corp", keep_default_na=False)
        # some sheets may be empty
        if not posts.empty:
            print(f"working on sheet for {posts.at[0, 'Brand']}")
            # make additional stop words from the brand names
            stopwords.extend(stopwords_from_brands(posts.at[0, 'Brand']))
            clean_text = get_posts_text(posts, "", "", phrases, stopwords)
            all_clean_words = list(itertools.chain(*clean_text))

            # Create counter
            word_counts = collections.Counter(all_clean_words)
            word_counts_df = pd.DataFrame(word_counts.most_common(20), columns=['words', 'counts'])
            wordsets.append(word_counts_df)
            brand_names.append(posts.at[0, 'Brand'])

    # write the word counts out to a new file
    with pd.ExcelWriter(output_file) as writer:
        for brand, words in zip(brand_names, wordsets):
            words.to_excel(writer, sheet_name=brand)

    return str(output_dir)

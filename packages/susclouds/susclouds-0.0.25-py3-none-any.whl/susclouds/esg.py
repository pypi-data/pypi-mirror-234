"""
This file is to produce wordclouds for ESG data
"""
import os
import pathlib
import logging
import pandas as pd
import itertools
import collections
from typing import Callable, List

from susclouds.new_cleaning import get_posts_text
from susclouds.wordcloud_func import create_and_write_wordcloud
from susclouds.stopword_funcs import stopwords_from_brands, get_brand_owners, get_brands

# configure some basic logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(__name__+".log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

def wordcloud_by_sector_and_class(source_file: os.path, phrases: pd.DataFrame, stopwords: List[str], sector: str):
    """
    generate and save ESG wordclouds
    :param dataframe: the dataframe of the Followers sheet for the posts
    :param posts: the post data
    :param stopwords: the list of stop words
    :param sector: the sector this wordcloud is for
    """
    logger.debug(f"creating wordclouds by sector and class for {str(source_file)}")
    classifications = ["Environmental", "Governance", "Social"]

    followers = pd.read_excel(source_file, sheet_name="Followers", keep_default_na=False)
    brand_owners = get_brand_owners(followers)
    brands = get_brands(followers)

    # add brand_owners to stopwords
    for brand_owner in brand_owners:
        stopwords.extend(stopwords_from_brands(brand_owner))

    # add brands to stopwords
    for brand in brands:
        stopwords.extend(stopwords_from_brands(brand))

    """
    Read all the brand owner posts from a report data file and then taking each ESG classification in turn
    loop through the brand owners and create a word cloud for that owners posts in that
    classification. Then create a separate cloud for all posts in that same classification and another
    for all posts in the sector irrespective of classification.
    """
    posts = pd.read_excel(source_file, sheet_name="Brand Owner Posts", keep_default_na=False)

    for classification in classifications:
        # first a wordcloud for each brand_owner
        for brand_owner in brand_owners:
            clean_text = get_posts_text(posts, classification, brand_owner, phrases, stopwords)
            all_clean_words = list(itertools.chain(*clean_text))
            # Create counter
            word_counts = collections.Counter(all_clean_words)
            create_and_write_wordcloud(word_counts, f"wc_{sector}_{classification}_{brand_owner}.png")

        # now a word cloud for all the posts, by all the brands in this classification
        clean_text = get_posts_text(posts, classification, "", phrases, stopwords)
        all_clean_words = list(itertools.chain(*clean_text))
        # Create counter
        word_counts = collections.Counter(all_clean_words)
        create_and_write_wordcloud(word_counts, f"wc_{sector}_{classification}.png")
        
    # now a word cloud for all the posts, by all the brands in this sector for all classifications
    clean_text = get_posts_text(posts, "", "", phrases, stopwords)
    all_clean_words = list(itertools.chain(*clean_text))
    # Create counter
    word_counts = collections.Counter(all_clean_words)
    create_and_write_wordcloud(word_counts, f"wc_{sector}_all.png")


def wordcloud_by_sector_and_class_no_sector(source_file: os.path, phrases: pd.DataFrame, stopwords: List[str], output_dir: os.path):
    """
    generate and save ESG wordclouds
    :param dataframe: the dataframe of the Followers sheet for the posts
    :param posts: the post data
    :param stopwords: the list of stop words
    :param sector: the sector this wordcloud is for
    """
    logger.debug(f"creating wordclouds by sector and class for {str(source_file)}")
    classifications = ["Environmental", "Governance", "Social"]

    if not output_dir.is_dir():
        os.makedirs(output_dir)

    sector = os.path.basename(source_file).split("-")[1].split("2")[0].strip()


    followers = pd.read_excel(source_file, sheet_name="Followers", keep_default_na=False)
    brand_owners = get_brand_owners(followers)
    brands = get_brands(followers)

    # add brand_owners to stopwords
    for brand_owner in brand_owners:
        stopwords.extend(stopwords_from_brands(brand_owner))

    # add brands to stopwords
    for brand in brands:
        stopwords.extend(stopwords_from_brands(brand))

    """
    Read all the brand owner posts from a report data file and then taking each ESG classification in turn
    loop through the brand owners and create a word cloud for that owners posts in that
    classification. Then create a separate cloud for all posts in that same classification and another
    for all posts in the sector irrespective of classification.
    """
    posts = pd.read_excel(source_file, sheet_name="Brand Owner Posts", keep_default_na=False)

    for classification in classifications:
        # first a wordcloud for each brand_owner
        for brand_owner in brand_owners:
            clean_text = get_posts_text(posts, classification, brand_owner, phrases, stopwords)
            all_clean_words = list(itertools.chain(*clean_text))
            # Create counter
            word_counts = collections.Counter(all_clean_words)
            create_and_write_wordcloud(word_counts, str(output_dir) + f"/wc_{sector}_{classification}_{brand_owner}.png")

        # now a word cloud for all the posts, by all the brands in this classification
        clean_text = get_posts_text(posts, classification, "", phrases, stopwords)
        all_clean_words = list(itertools.chain(*clean_text))
        # Create counter
        word_counts = collections.Counter(all_clean_words)
        create_and_write_wordcloud(word_counts, str(output_dir) + f"/wc_{sector}_{classification}.png")

    # now a word cloud for all the posts, by all the brands in this sector for all classifications
    clean_text = get_posts_text(posts, "", "", phrases, stopwords)
    all_clean_words = list(itertools.chain(*clean_text))
    # Create counter
    word_counts = collections.Counter(all_clean_words)
    create_and_write_wordcloud(word_counts, str(output_dir) + f"/wc_{sector}_all.png")
    return str(output_dir)

def wordcloud_all_sectors_by_class(source_file: os.path, phrases: pd.DataFrame, stopwords: List[str], classification: str, output_dir: os.path):
    """
        generate and save wordcloud for all sectors and a single classification
        :param dataframe: the dataframe of the Followers sheet for the posts
        :param posts: the post data
        :param stopwords: the list of stop words
        :param sector: the sector this wordcloud is for
        :param classification: the classification(E,S or G) for the cloud to be generated for
        """
    logger.debug(f"creating wordclouds for all sectors by class for {str(source_file)}")

    posts = pd.read_excel(source_file, sheet_name="Corporate Posts", keep_default_na=False)

    if not output_dir.is_dir():
        os.makedirs(output_dir)

    brand_owners = get_brand_owners(posts)

    # add brand_owners to stopwords
    for brand_owner in brand_owners:
        stopwords.extend(stopwords_from_brands(brand_owner))

    clean_text = get_posts_text(posts, classification, "", phrases, stopwords)

    all_clean_words = list(itertools.chain(*clean_text))

    # Create counter
    word_counts = collections.Counter(all_clean_words)
    create_and_write_wordcloud(word_counts, str(output_dir) + f"/wc_CG_{classification}.png")
    return str(output_dir)

def wordcloud_all_sectors_all_class(source_file: os.path, phrases: pd.DataFrame, stopwords: List[str], output_dir: os.path):
    """
        generate and save wordclouds for all classifications and all sectors
        :param dataframe: the dataframe of the Followers sheet for the posts
        :param posts: the post data
        :param stopwords: the list of stop words
        :param sector: the sector this wordcloud is for
        """
    logger.debug(f"creating wordclouds for all sectors and all classes for {str(source_file)}")
    posts = pd.read_excel(source_file, sheet_name="Corporate Posts", keep_default_na=False)

    if not output_dir.is_dir():
        os.makedirs(output_dir)

    brand_owners = get_brand_owners(posts)

    # add brand_owners to stopwords
    for brand_owner in brand_owners:
        stopwords.extend(stopwords_from_brands(brand_owner))

    clean_text = get_posts_text(posts, "", "", phrases, stopwords)

    all_clean_words = list(itertools.chain(*clean_text))

    # Create counter
    word_counts = collections.Counter(all_clean_words)
    create_and_write_wordcloud(word_counts, str(output_dir) + f"/wc_CG_esg.png")

    return str(output_dir)

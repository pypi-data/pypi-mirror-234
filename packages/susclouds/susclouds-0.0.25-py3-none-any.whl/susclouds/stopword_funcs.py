"""
Collection of functions to read and create stop words to be eliminated when creating
word susclouds.

Most of the functions relate to the manipulation of brand names avoid them appearing in
word susclouds.
"""

import string
import re
import pandas as pd
from typing import List
from susclouds.new_cleaning import clean_post

def _combine(string):
    """
    Remove spaces from a string and return it as a single word
    """
    return(re.sub('[\W_]+','',string,flags=re.ASCII))


def _depossess(word):
    """
    If a brand name is already a possessive, e.g. Kellogg's, Hellmann's etc., remove the 's
    """
    return (word.split("'", 1)[0])


def _combine_and_hashtag(string):
    """
    Turn a brand name into a possible hashtag and mention that may appear in that brand's posts
    """
    words = []
    new_word = _combine(string)
    words.append(new_word)
    words.append(f"#{new_word}")
    words.append(f"@{new_word}")
    return(words)


def _separate(string):
    """
    Split a string (brand name) into separate words, but also keep original and the string
    separated only by spaces
    """
    new_word = ""
    words = re.split('-| - |&| & | ', string)

    if len(words) > 1:
        for word in words:
            new_word = new_word + word + " "

        words.append(new_word.rstrip())
        words.append(string)

    return (words)


def _possessive(words):
    """
    Create a possessive version of a brand name (adding an 's' with no apostrophe as
    apotrophes will have already been cleaned from the source text).
    """
    new_words = []
    for word in words:
        new_words.append(word)
        new_words.append(f"{word}s")
    return(new_words)


def stopwords_from_brands(brand):
    """
    Use the functions above to create a list of stop words
    """
    stopwords = []
    stopwords.extend(_combine_and_hashtag(brand.lower()))
    stopwords.extend(_possessive(_separate(brand.lower())))
    """
    need to apply the same cleaning to brand names as we do to posts to ensure
    stopword matching is correct
    """
    stopwords.extend(_combine_and_hashtag(clean_post(brand.lower())))
    stopwords.extend(_possessive(_separate(clean_post(brand.lower()))))
    """
    have to use append rather than extend as extend would treat each indvidual character
    as a separate entity
    """
    stopwords.append(_depossess(brand.lower()))

    return (stopwords)


def stopwords_from_file(df: pd.DataFrame) -> List[str]:
    """
    Extract and return a list of words from Stopwords column of datafram
    """
    return df['Stopwords'].astype(str).tolist()


def get_brand_owners(df: pd.DataFrame) -> List[str]:
    """
    Extract and return a list of unique brand owner names from dataframe
    :param df: the dataframe to get brand owners from must have a "Brand Owner" col
    :return: a list of unique brand owners
    """

    return list(set(df['Brand Owner'].values.tolist()))


def get_brands(df: pd.DataFrame) -> List[str]:
    """
    Extract and return a list of brands from dataframe
    """
    return df['Brand'].values.tolist()


def update_stopwords(file_name: str):
    """
    Update the new standard stop word file with one provided by the user
    """
    stopwords_df = pd.read_excel(file_name, sheet_name='Stop Words')
    stopwords = stopwords_from_file(stopwords_df)
    stopwords.extend([str(i) for i in range(1, 2024)])
    stopwords.extend(["", "x000d"])
    stopwords_df = pd.DataFrame(stopwords, columns=['Stopwords'])
    stopwords_df.to_csv("stopwords.csv", index=False)

def update_phrases(file_name: str):
    """
    Update the standard phrases file with a new one provided by the user
    """
    phrases_df = pd.read_excel(file_name, sheet_name='Phrase List')
    phrases_df.to_csv("phrases.csv", index=False)
    
    




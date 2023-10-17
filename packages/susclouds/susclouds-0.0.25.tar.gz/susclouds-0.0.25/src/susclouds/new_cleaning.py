"""
Text cleaning fuction... gets rid of all URLs and non-aphanumeric except for @, #, - and ~, and
replace all whitespace and _ with spaces
"""
import pandas as pd
import re
from functools import reduce
from html import unescape
from typing import List
from string import ascii_lowercase, digits, whitespace


def _append_if_alphanum(acc, char):
    """
    appends char to given string if alphanumeric or whitespace
    :param acc: string to be appended to
    :param char: char to append
    """
    alphanums = ascii_lowercase + digits + "@#-~"
    if char in alphanums:
        return acc + char
    elif char in whitespace + "_":  # replace all whitespace with spaces
        return acc + " "
    return acc


def clean_post(text: str) -> str:
    """
    remove all html elements from text
    :param text: string to have html removed from
    """
    decoded = unescape(text)
    dumped = re.sub("\n|\r", " ", decoded)
    decluttered = re.sub(r"https*://\S+", "", dumped)
    return reduce(_append_if_alphanum, decluttered, "").strip()


def _really_clean(words: List[str], stopwords: List[str]):
    """
    Remove stopwords from text
    :param words: a list of strings (words) to be cleaned
    :param stopwords: a list of strings to be removed from words
    :return: a list of words without stopwords
    """
    new_words = []

    words = [w for w in words if not w in stopwords]

    # get rid of ~s added to keep phrases together and -s so that phrases separated by space or - are
    # counted as the same phrase
    for word in words:
        new_words.append(re.sub("[~-]", " ", word))

    return (new_words)

def _substitute_post_text(text: str, phrases: pd.DataFrame) -> str:
    """
    make multi-word phrases recognisable by separating by ~ (we'll get rid of it again later)
    """
    for phrase in phrases.itertuples(index=False):
        text = text.replace(phrase[phrases.columns.get_loc('Phrase List')],
                            phrase[phrases.columns.get_loc('Subst List')])

    return (text)


def _post_check(post_category, post_brand_owner, classification: str, brand_owner: str) -> bool:
    if classification != "" and brand_owner != "":
        # true if the post matches the classification (E, S, or G) and brand
        return post_brand_owner == brand_owner and post_category == classification
    elif classification != "" and brand_owner == "":
        # true if the post matches the classification (E, S, or G)
        return post_category == classification
    elif classification == "":
        # true if the post is sustainability related, i.e. not None or NonEnglish
        return post_category not in ["None", "NonEnglish"]

def get_posts_text(posts: pd.DataFrame, classification: str, brand_owner: str, phrases: List[str], stopwords: List[str]) -> List[str]:
    clean_text = []
    for post in posts.itertuples(index=False):
        if _post_check(post[posts.columns.get_loc('Category')],post[posts.columns.get_loc('Brand Owner')],
                        classification, brand_owner):
            post_text = str(post[posts.columns.get_loc('Full Text')]).lower()
            if not pd.isnull(post_text):
                clean_post_text = clean_post(post_text)
                substituted_post_text = _substitute_post_text(clean_post_text, phrases)
                clean_text.append(_really_clean(substituted_post_text.split(" "), stopwords))

    return clean_text

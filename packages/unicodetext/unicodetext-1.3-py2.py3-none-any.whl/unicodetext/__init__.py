#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Author  huang22
Date    ：2023/9/28 18:25
"""
import re

from unicodetext.unicode_categories import UnicodeCategories
from unicodetext.unicode_blocks import UnicodeBlocks


def extract_chr(text, chrs=None):
    """
    extract characters in chrs
    :param text: input text
    :param chrs: characters
    :return: list
    """
    if chrs is None:
        chrs = []
    return re.findall(r"[{}]".format("".join([re.escape(i) for i in chrs])), text)


def remove_chr(text, chrs=None, replace_str=None):
    """
    remove characters in chrs
    :param text: input text
    :param chrs: characters
    :return: the left text string
    """
    if chrs is None:
        chrs = []
    return text.translate({ord(i): replace_str for i in chrs})


def extract_punctuation(text):
    return extract_chr(text, chrs=UnicodeCategories.Punctuation)


def remove_punctuation(text, replace_str=None):
    return remove_chr(text, chrs=UnicodeCategories.Punctuation, replace_str=replace_str)


def extract_mark(text):
    return extract_chr(text, chrs=UnicodeCategories.Mark)


def remove_mark(text, replace_str=None):
    return remove_chr(text, chrs=UnicodeCategories.Mark, replace_str=replace_str)


def extract_letter(text):
    return extract_chr(text, chrs=UnicodeCategories.Letter)


def remove_letter(text, replace_str=None):
    return remove_chr(text, chrs=UnicodeCategories.Letter, replace_str=replace_str)


def extract_cased_letter(text):
    return extract_chr(text, chrs=UnicodeCategories.Cased_Letter)


def remove_cased_letter(text, replace_str=None):
    return remove_chr(
        text, chrs=UnicodeCategories.Cased_Letter, replace_str=replace_str
    )


def extract_number(text):
    return extract_chr(text, chrs=UnicodeCategories.Number)


def remove_number(text, replace_str=None):
    return remove_chr(text, chrs=UnicodeCategories.Number, replace_str=replace_str)


def extract_symbol(text):
    return extract_chr(text, chrs=UnicodeCategories.Symbol)


def remove_symbol(text, replace_str=None):
    return remove_chr(text, chrs=UnicodeCategories.Symbol, replace_str=replace_str)


def extract_separator(text):
    return extract_chr(text, chrs=UnicodeCategories.Separator)


def remove_separator(text, replace_str=None):
    return remove_chr(text, chrs=UnicodeCategories.Separator, replace_str=replace_str)


def extract_emoticon(text):
    return extract_chr(text, chrs=UnicodeBlocks.Emoticons)


def remove_emoticon(text, replace_str=None):
    return remove_chr(text, chrs=UnicodeBlocks.Emoticons, replace_str=replace_str)

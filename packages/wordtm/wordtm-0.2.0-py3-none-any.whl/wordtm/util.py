# util.py
#   Some utility functions including loading Scriptue, setting Scripture language,
#     extracting a specifc range of Scripture
#   By Johnny Cheng
#   Updated: 30 June 2022


import re
import pandas as pd
from importlib_resources import files

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import jieba
from collections import Counter


glang = 'en'
stops = set()


def load_word(ver='web.csv'):
    scfile = files('wordjc.data').joinpath(ver)
    return pd.read_csv(scfile)


def get_list(df, column='book'):
    if column in list(df.columns):
        return list(df[column].unique())
    else:
        return "No such column!"


def get_text(df):
    return ''.join(list(df.text)).replace('\u3000', '')


def get_text_list(df):
    return df.text.apply(lambda x: x.replace('\u3000', '')).tolist()


def clean_text(df):
    df.text = [re.sub(r'\d+', '', str(v).replace('\n', ' ')) for v in df.text]
    for sw in stopwords.words('english'):
        df.text = [v.replace(' ' + sw + ' ', ' ') for v in df.text]

    df.text = df.text.apply(lambda v: " ".join(w.lower() for w in v.split()))
    df.text = df.text.str.replace('[^\w\s]', '', regex=True)
    return df


## Functions for Chinese Text

def add_chi_vocab():
    vocab_file = files('wordjc.data').joinpath('bible_vocab.txt')
    with open(vocab_file, 'r', encoding='utf8') as f:
        vocab_list = f.readlines()
        for vocab in vocab_list:
            jieba.add_word(vocab.replace('\n', ''))


def chi_stops():
    dict_file = files('wordjc.dictionary').joinpath('dict.txt.big.txt')
    cloud_file = files('wordjc.dictionary').joinpath('stopWord_cloudmod.txt')
    jieba.set_dictionary(dict_file)
    with open(cloud_file, 'r', encoding='utf-8-sig') as f:
        return f.read().split('\n')


def set_lang(lang='en'):
    global glang, stops
    glang = lang
    if glang == 'en':  # English
        stops = set(stopwords.words("english"))
    else:  # Chinese
        add_chi_vocab()
        stops = chi_stops()


def get_diction_en(df):
    words = word_tokenize(' '.join(list(df.text)))
    stem = PorterStemmer()
    
    terms = []
    for t in words:
        t = stem.stem(t)
        if t not in stops:
            terms.append(t)

    diction = Counter(terms)
    return diction


def get_diction_chi(df):
    text = ''.join(list(df.text)).replace('\u3000', '')
    text = re.sub("[、．。，！？『』「」〔〕]", "", text)

    terms = []
    for t in jieba.cut(text, cut_all=False):
        if t not in stops:
            terms.append(t)

    diction = Counter(terms)
    return diction


def get_diction(df):
    if glang == 'en':
        return get_diction_en(df)
    else:
        return get_diction_chi(df)


def chi_sent_terms(text):
    text = re.sub("[、．。，！？『』「」〔〕]", "", text)
    terms = []
    for t in jieba.cut(text, cut_all=False):
        if t not in stops:
            terms.append(t)
    return terms


def get_sent_terms(text):
    if glang == 'en':
        return word_tokenize(text)
    else:
        return chi_sent_terms(text)


## Extract Scripture by Various Levels of Filtering

# Extract Scripture by testament, category, book or chapter or verse
def extract(df, testament=-1, category='', book=0, chapter=0, verse=0):
    no_ret = "No scripture is extracted!"
    sub_df = pd.DataFrame()  # Empty DataFrame
    isbook = ischapter = False

    if (testament > -1) & (testament < 2):
        sub_df = df[df.testament==int(testament)]
    elif category != '':
        if category in get_list(df, column='category'):
            sub_df = df[df.category==category]
        elif category in get_list(df, column='cat'):
            sub_df = df[df.cat==category]
    elif book in get_list(df, column='book'):
        sub_df = df[df.book==book]
        isbook = True
    elif isinstance(book, int):
        if book > 0 & book < 67:
            sub_df = df[df.book_no==book]
            isbook = True
    elif isinstance(book, tuple):
        if (book[0] <= book[1]) & (book[0] > 0) & (book[1] < 67):
            sub_df = df[(df.book_no >= book[0]) & (df.book_no <= book[1])]
            isbook = True

    if isbook & (len(sub_df) > 0) & (chapter != 0):
        if isinstance(chapter, int):
            sub_df = sub_df[sub_df.chapter==chapter]
            ischapter = True
        elif isinstance(chapter, tuple):
            if chapter[0] <= chapter[1]:
                sub_df = sub_df[(sub_df.chapter >= chapter[0]) & (sub_df.chapter <= chapter[1])]
                ischapter = True

        if ischapter & (len(sub_df) > 0) & (verse != 0):
            if isinstance(verse, int):
                sub_df = sub_df[sub_df.verse==verse]
            elif isinstance(verse, tuple):
                if verse[0] <= verse[1]:
                    sub_df = sub_df[(sub_df.verse >= verse[0]) & (sub_df.verse <= verse[1])]

    if len(sub_df) > 0:
        return sub_df.copy()
    else:
        return no_ret


# Extract Scipture by a Filter String
def extract2(df, filter=''):
    chapter = verse = 0

    if filter == '':
        return df
    else:
        parts = filter.split()
        book = parts[0]
        if len(parts) > 1:
            parts = parts[1].split(':')
            if parts[0] == '':
                chapter = 0
            else:
                chapter = int(parts[0])

            if (len(parts) > 1):
                if (parts[1] != ''):
                    parts = parts[1].split('-')
                    if parts[0] == '':
                        verse = 1
                    else:
                        verse = int(parts[0])

                    if (len(parts) > 1):
                        if (parts[1] == ''):
                            verse = (verse, 999)
                        else:
                            verse = (verse, int(parts[1]))

        return extract(df, book=book, chapter=chapter, verse=verse)

# ta.py
#    Extractive text summarization of a prescribed range of Scripture
#    By Johnny Cheng
#    Updated: 28 June 2022


import numpy as np
from importlib_resources import files
from nltk.tokenize import sent_tokenize

from wordjc import util


# Tokenize text into sentences
def get_sentences(df, lang):
    text = util.get_text(df)
    if lang == 'chi':
        sentences = text.split('。')
        if sentences[-1] == '':
            sentences = np.delete(sentences, -1)
    else:
        sentences = sent_tokenize(text)

    return sentences


# Score a sentence by its words
def get_sent_scores(sentences, diction, sent_len) -> dict:   
    sent_weight = dict()

    for sentence in sentences:
        # sent_wordcount = (len(util.get_sent_terms(sentence)))
        sent_wordcount_net = 0
        for word_weight in diction:
            if word_weight in sentence.lower():
                sent_wordcount_net += 1
                if sentence[:sent_len] in sent_weight:
                    sent_weight[sentence[:sent_len]] += diction[word_weight]
                else:
                    sent_weight[sentence[:sent_len]] = diction[word_weight]

        if sent_weight != dict() and sent_weight.get(sentence[:sent_len], '') != '':
            sent_weight[sentence[:sent_len]] = sent_weight[sentence[:sent_len]] / \
                                                sent_wordcount_net

    return sent_weight


# Extract summary from sentences
def get_summary(sentences, sent_weight, threshold, sent_len):
    sent_counter = 0
    summary = ''
    sep ='~'

    for sentence in sentences:
        if sentence[:sent_len] in sent_weight and \
           sent_weight[sentence[:sent_len]] >= (threshold):
            summary += sentence + sep
            sent_counter += 1

    return summary


def summary(df, lang='en', weight=1.5, sent_len=8):
    if type(df) == str: return

    util.set_lang(lang)
    diction = util.get_diction(df)
    sentences = get_sentences(df, lang)

    sent_scores = get_sent_scores(sentences, diction, sent_len)
    threshold = np.mean(list(sent_scores.values()))
    return get_summary(sentences, sent_scores, weight * threshold, sent_len)

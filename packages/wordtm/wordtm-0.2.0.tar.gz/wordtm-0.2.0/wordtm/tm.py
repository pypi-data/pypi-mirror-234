# tm.py
#    Topic modeling through LDA for a prescribed range of Scripture
#    By Johnny Cheng
#    Updated: 30 June 2022


import warnings
warnings.filterwarnings("ignore")

import os
from pprint import pprint

import gensim
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
import gensim.corpora as corpora

import pyLDAvis.gensim_models
import pickle 
import pyLDAvis

from wordjc import util

import nltk
nltk.download('punkt')


def sent_to_words(sentences):
    for sentence in sentences:
        # deacc=True removes punctuations
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))


def build_lda(diction, num_topics):
    data = list(diction)
    data_words = list(sent_to_words(data))
    # print(data_words[:1][0][:30])

    # Create Dictionary
    id2word = corpora.Dictionary(data_words)

    # Create Corpus
    texts = data_words

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View
    # print(corpus[:1][0][:30])

    # Build LDA Model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=num_topics)

    # Print the Keywords in the topics
    print("Keywords of the %d topics:" %(num_topics))
    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    # Compute Coherence Score
    coherence_model_lda = CoherenceModel(model=lda_model, texts=data_words, \
                                         dictionary=id2word, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print("\nCoherence Score: ", coherence_lda, "\n")
    
    return lda_model, corpus, id2word


def lda_vis(lda_model, corpus, id2word, num_topics):
    LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_'+str(num_topics))

    LDAvis_prepared = pyLDAvis.gensim_models.prepare(lda_model, corpus, id2word)
    with open(LDAvis_data_filepath, 'wb') as f:
        pickle.dump(LDAvis_prepared, f)

    # load the pre-prepared pyLDAvis data
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)

    pyLDAvis.save_html(LDAvis_prepared, './results/ldavis_prepared_'+ str(num_topics) +'.html')
    return LDAvis_prepared


def lda(df, lang='en', num_topics=10):
    util.set_lang(lang)
    diction = util.get_diction(df)
    lda_model, corpus, id2word = build_lda(diction, num_topics)
    LDAvis_prepared = lda_vis(lda_model, corpus, id2word, num_topics)
    # pyLDAvis.display(LDAvis_prepared)
    return LDAvis_prepared

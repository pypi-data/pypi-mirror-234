from setuptools import setup, find_packages

VERSION = '0.2.0' 
DESCRIPTION = 'Scripture NLP Package'
LONG_DESCRIPTION = 'An NLP package for topic modeling on the Holy Scripture from low-code to pro-code'

# Setting up
setup(
        name="wordtm", 
        version=VERSION,
        author="Johnny CHENG",
        author_email="<drjohnny@email.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['numpy', 'pandas', 'importlib_resources', 'regex', 'nltk', \
                    'matplotlib', 'wordcloud', 'pillow', 'jieba', 'gensim', 'pyLDAvis',  \
                    'bertopic',  'transformers', 'gensim', 'spacy', 'seaborn', \
                    'importlib'],
        
        keywords=['word', 'scripture', 'topic modeling', 'visualization', \
                  'low-code', 'pro-code', 'network analysis', 'BERTopic', \
                                 'LDA', 'NFM'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Intended Audience :: Science/Research",
            "Intended Audience :: Religion",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: MacOS :: MacOS X",
        ]
)

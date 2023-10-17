# wordtm

An NLP package for topic modeling on the Holy Scripture from low-code to pro-code

## Installation

```shell
$ pip install wordtm
```

## Usage

`wordtm` can be used to perform some NLP pre-processing tasks, text exploration, including Chinese one, text visualization (word cloud), and topic modeling (BERTopic, LDA and NMF) as follows:

```python
from wordtm import meta, util, ta, tm, viz, pivot, quot

from importlib_metadata import version
print(version('wordtm'))

print(meta.get_module_info())

df = util.load_word()
cdf = util.load_word('cuv.csv')

df.head()

cdf.head()

rom = util.extract2(df, 'Rom 8')
crom = util.extract2(cdf, 'Rom 8')

ta.summary(rom, code=True)

viz.chi_wordcloud(cdf)

pivot.stat(cdf, chi=True)
```

## Contributing

Interested in contributing? Check out the contributing guidelines. 
Please note that this project is released with a Code of Conduct. 
By contributing to this project, you agree to abide by its terms.

## License

`wordtm` was created by Johnny Cheng. It is licensed under the terms
of the MIT license.

## Credits

`wordtm` was created with 
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and 
the `py-pkgs-cookiecutter` 
[template](https://github.com/py-pkgs/py-pkgs-cookiecutter).

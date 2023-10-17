# fuck

<p align="center">
    <img src="assets/logo.png"/>
</p>

**F**uck: an **u**ltimate **c**ensorship **k**iller - a tiny program for uncensoring russian texts

## Usage

To uncensor a particular text use command like this:

```sh
python -m fuck uncensor 'Нах**я до%@я нах%ярил??? Расх*%яривай нах@й - не дох*ярим. Них*я, не дох@я дох%ярим - пох*ярили'
```

The command will emit an uncensored text:

```sh
Нахуя дохуя нахуярил??? Расхуяривай нахуй - не дохуярим. Нихуя, не дохуя дохуярим - похуярили
```

To get the same result in a python command see [the example](./examples/main.py):

```py
from fuck import ProfanityHandler

text, censored, unhandled_matches = ProfanityHandler(
    path = 'assets/profane-words.txt'
).uncensor(
    'Нах**я до%@я нах%ярил??? Расх*%яривай нах@й - не д0х*ярим. Них*я, не дох@я дох%ярим - пох*ярили'
)

print(text)
print(censored)
print(unhandled_matches)
```

The script generates the following output upon execution:

```sh
Нахуя дохуя нахуярил??? Расхуяривай нахуй - не д0х*ярим. Нихуя, не дохуя дохуярим - похуярили
True
['д0х*ярим']
```

To uncensor texts from a `.tsv` file with anecdotes using default settings run the following command:

```sh
python -m fuck stats
```

## Installation

To create environment and install all dependencies execute the following command:

```sh
conda env create -f environment.yml
```

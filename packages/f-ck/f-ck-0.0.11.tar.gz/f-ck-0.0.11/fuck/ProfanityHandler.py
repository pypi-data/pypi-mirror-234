import re
import os

from pymorphy3 import MorphAnalyzer
from tqdm import tqdm

from .util import make_forms, restore_shape, CENSORED_TOKEN_TEMPLATE, to_template

EXCEPTION_MARK = '*'
SPACE = ' '


class ProfanityHandler:
    def __init__(self, path: str = None, verbose: bool = False):
        if path is None:
            # path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'assets', 'profane-words.txt')
            path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'profane-words.txt')

        self.path = path
        self.morph = morph = MorphAnalyzer(lang = 'ru')

        with open(path, 'r', encoding = 'utf-8') as file:
            words = []
            replacements = {}

            lines = file.read().split('\n')
            pbar = tqdm(total = len(lines), desc = 'Loading profane words dictionary') if verbose else None

            for word in lines:
                if word and not word.startswith('#'):
                    replacement = None

                    parts = word.split(SPACE, maxsplit = 1)

                    if len(parts) > 1:
                        word = parts[0]
                        replacement = parts[1]

                    parts = word.split(EXCEPTION_MARK, maxsplit = 1)
                    word = parts[0]

                    if len(parts) > 1:
                        for form in make_forms(word):
                            words.append(form)

                            replacements[form] = word if replacement is None else replacement
                    else:
                        entries = morph.parse(word)

                        if len(entries) > 0:
                            # replacement_entries = None if replacement is None else morph.parse(replacement)

                            # assert replacement_entries is None or len(replacement_entries) > 0, 'Replacement cannot have fewer associated entries than the base word'

                            # lexeme = entries[0].lexeme
                            # replacement_lexeme = None if replacement_entries is None else replacement_entries[0].lexeme

                            # print([item.word for item in replacement_lexeme], [item.word for item in lexeme])

                            # if replacement_lexeme is not None and len(replacement_lexeme) == len(lexeme):
                            #     for lexeme_entry, replacement_lexeme_entry in zip(lexeme, replacement_lexeme):
                            #         for form in make_forms(lexeme_entry.word):
                            #             words.append(form)
                            #             replacements[form] = replacement_lexeme_entry.word
                            # else:

                            for lexeme in entries[0].lexeme:
                                for form in make_forms(word := lexeme.word):
                                    words.append(form)

                                    replacements[form] = word if replacement is None else replacement

                if verbose:
                    pbar.update()

        self.words = words
        self.replacements = replacements

        if verbose:
            pbar.desc = f'Loaded {len(words)} word forms'

    def _match(self, template: str, normalized_template: str):
        for word in self.words:
            if re.fullmatch(normalized_template, word) is not None:
                return restore_shape(template, word)

        return None

    def _replace(self, text: str, word: str):
        template = to_template(word)
        normalized_template = to_template(word.lower())

        match = self._match(template, normalized_template)

        if match is None:
            return text, False

        return text.replace(word, self.replacements.get(match, match)), True

    def uncensor(self, text: str):
        # found_replacements = False
        censored = False
        unhandled_matches = []

        for match in CENSORED_TOKEN_TEMPLATE.findall(text):
            text, found_replacement = self._replace(text, match)

            # found_replacements = found_replacements or found_replacement

            if not found_replacement:
                unhandled_matches.append(match)

            if censored is False:
                censored = True

        return text, censored, unhandled_matches  # found_replacements, censored

    @property
    def length(self):
        return len(self.words)

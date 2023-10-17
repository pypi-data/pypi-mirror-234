from click import group, argument, option
from pandas import read_csv
from tqdm import tqdm

from .ProfanityHandler import ProfanityHandler


@group()
def main():
    pass


@main.command()
@argument('path', type = str, default = 'assets/anecdotes.tsv')
@option('--dictionary', '-d', type = str, default = 'assets/profane-words.txt')
@option('--verbose', '-v', is_flag = True)
@option('--output', '-o', type = str, help = 'path to the output file with uncensored texts')
def stats(path: str, dictionary: str, verbose: bool, output: str):
    ph = ProfanityHandler(path = dictionary, verbose = verbose)
    df = read_csv(path, sep = '\t')

    n_censored_texts = 0
    unhandled_matches = []

    pbar = tqdm(total = len(df.index), desc = 'Handling documents') if verbose else None

    uncensored_texts = None if output is None else []

    for text in df['text']:
        uncensored_text, censored, matches = ph.uncensor(text)

        unhandled_matches.extend(matches)

        if output is not None:
            uncensored_texts.append(uncensored_text)

        if censored:
            n_censored_texts += 1

        if verbose:
            pbar.update()

    if output is not None:
        df['text'] = uncensored_texts
        df.to_csv(output, sep = '\t', index = False)

    print(f'Found {n_censored_texts} censored texts')
    print(f'Found {len(unhandled_matches)} unhandled matches: {", ".join(unhandled_matches)}')


@main.command()
@argument('text', type = str)
@option('--dictionary', '-d', type = str, default = 'assets/profane-words.txt')
@option('--verbose', '-v', is_flag = True)
def uncensor(text: str, dictionary: str, verbose: bool):
    text, _, _ = ProfanityHandler(path = dictionary, verbose = verbose).uncensor(text)

    print(text)


if __name__ == '__main__':
    main()

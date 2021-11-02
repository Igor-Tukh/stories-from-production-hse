import argparse

from src.spell_checker import SpellChecker

HELP_STR = 'Type text to apply the spell checker or type \'exit\' to exit.'


def runCLI(args):
    checker = SpellChecker(args.language, args.n_suggestions)
    print(HELP_STR)
    while True:
        print('> ', end='')
        text = input()
        if text == 'exit':
            return
        checker(text)


def validate_CLI_args(args):
    if args.language not in {'english'}:
        raise ValueError(f'Invalid language option: {args.language}.')
    if args.n_suggestions < 0:
        return ValueError(f'Invalid number of suggestions: {args.n_suggestions}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--language', type=str, help='Language of input text. Currently supported options:'
                                                     'english (default).', required=False, default='EN.')
    parser.add_argument('--n_suggestions', type=int, help='Maximum number of corrections to suggest', default=10)
    CLI_args = parser.parse_args()
    try:
        validate_CLI_args(CLI_args)
    except ValueError as e:
        print(e)
        exit(1)
    runCLI(CLI_args)

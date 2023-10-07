import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subcommand')

    parser_history = subparsers.add_parser('history')
    parser_history.add_argument('')
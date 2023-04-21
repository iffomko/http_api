import sys

from cli_parser.Parser import Parser


def main():
    parser = Parser()

    parser.parse(sys.argv)


if __name__ == '__main__':
    main()
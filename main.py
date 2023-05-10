import sys

from cli_parser.Parser import Parser
from vk_api import VKApi


def main():
    parser = Parser()
    params = None

    try:
        params = parser.parse(sys.argv)
    except ValueError as e:
        print(f'Error: {e}')
        return

    if params.get('help'):
        print(params.get('help_text'))
        return

    vk = VKApi()

    print(vk.get_friends(params))


if __name__ == '__main__':
    main()
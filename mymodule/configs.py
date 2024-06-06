import argparse


def configure_argument_parser():
    parser = argparse.ArgumentParser(description='Парсер пакетов')
    parser.add_argument(
        'branch1',
        help='Первая ветка пакетов'
    )
    parser.add_argument(
        'branch2',
        help='Вторая ветка пакетов'
    )
    parser.add_argument(
        'arch',
        help='Тип архитектуры'
    )
    return parser

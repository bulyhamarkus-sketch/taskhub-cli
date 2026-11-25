#!/usr/bin/env python3
"""TaskHub CLI - консольний застосунок для керування списком завдань.

Структура проєкту:
    core.py     - ядро: уся логіка роботи із завданнями
    storage.py  - збереження та читання JSON-файлу
    cli.py      - командний рядок (argparse) і виведення
    taskhub.py  - точка входу (цей файл)

Запуск:
    python taskhub.py add "Купити молоко"
    python taskhub.py show
    python taskhub.py -h        (список усіх команд)
"""

import sys

from cli import build_parser
from core import TaskError


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except TaskError as e:
        print(f"Помилка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

"""Інтерфейс командного рядка (argparse).

Тут уся взаємодія з користувачем: print, аргументи, файли.
Логіка береться з core.py, збереження - зі storage.py.
"""

import argparse
import os

import core
from storage import load_tasks, save_tasks


# ---------- Обробники команд ----------

def cmd_add(args):
    tasks = load_tasks()
    task = core.add_task(tasks, args.text)
    save_tasks(tasks)
    print(f"Додано завдання #{task['id']}: {task['text']}")


def cmd_show(args):
    done = True if args.done else False if args.todo else None
    tasks = core.filter_tasks(load_tasks(), done)
    if not tasks:
        print("Список порожній.")
        return
    for t in tasks:
        print(core.format_task(t))


def cmd_edit(args):
    tasks = load_tasks()
    core.edit_task(tasks, args.id, args.text)
    save_tasks(tasks)
    print(f"Завдання #{args.id} змінено.")


def cmd_done(args):
    tasks = load_tasks()
    core.set_done(tasks, args.id, True)
    save_tasks(tasks)
    print(f"Завдання #{args.id} виконано.")


def cmd_undone(args):
    tasks = load_tasks()
    core.set_done(tasks, args.id, False)
    save_tasks(tasks)
    print(f"Завдання #{args.id} знову не виконане.")


def cmd_delete(args):
    tasks = load_tasks()
    core.delete_task(tasks, args.id)
    save_tasks(tasks)
    print(f"Завдання #{args.id} видалено.")


def cmd_search(args):
    found = core.search_tasks(load_tasks(), args.query)
    if not found:
        print("Нічого не знайдено.")
        return
    for t in found:
        print(core.format_task(t))


def cmd_stats(args):
    total, done, left = core.get_stats(load_tasks())
    print(f"Усього: {total}")
    print(f"Виконано: {done}")
    print(f"Залишилось: {left}")


def cmd_clear(args):
    left, removed = core.clear_done(load_tasks())
    save_tasks(left)
    print(f"Видалено виконаних завдань: {removed}")


def cmd_doneall(args):
    tasks = load_tasks()
    count = core.mark_all_done(tasks)
    save_tasks(tasks)
    print(f"Усі завдання ({count}) позначено виконаними.")


def cmd_reset(args):
    count = len(load_tasks())
    save_tasks([])
    print(f"Список очищено. Видалено завдань: {count}")


def cmd_sort(args):
    tasks = core.sort_tasks(load_tasks())
    if not tasks:
        print("Список порожній.")
        return
    for t in tasks:
        print(core.format_task(t))


def cmd_export(args):
    tasks = load_tasks()
    with open(args.filename, "w", encoding="utf-8") as f:
        for t in tasks:
            f.write(core.format_task(t).strip() + "\n")
    print(f"Експортовано {len(tasks)} завдань у файл {args.filename}")


def cmd_count(args):
    print(f"Кількість завдань: {len(load_tasks())}")


def cmd_first(args):
    tasks = load_tasks()
    print(core.format_task(tasks[0]) if tasks else "Список порожній.")


def cmd_last(args):
    tasks = load_tasks()
    print(core.format_task(tasks[-1]) if tasks else "Список порожній.")


def cmd_import(args):
    if not os.path.exists(args.filename):
        raise core.TaskError(f"файл {args.filename} не знайдено.")
    with open(args.filename, "r", encoding="utf-8") as f:
        texts = core.parse_lines(f)
    tasks = load_tasks()
    for text in texts:
        core.add_task(tasks, text)
    save_tasks(tasks)
    print(f"Імпортовано завдань: {len(texts)}")


# ---------- Налаштування argparse ----------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="taskhub", description="TaskHub CLI - список завдань у терміналі"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="додати завдання")
    p.add_argument("text", help="текст завдання")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("show", help="показати завдання")
    group = p.add_mutually_exclusive_group()
    group.add_argument("--done", action="store_true", help="лише виконані")
    group.add_argument("--todo", action="store_true", help="лише невиконані")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("edit", help="змінити текст завдання")
    p.add_argument("id", type=int, help="номер завдання")
    p.add_argument("text", help="новий текст")
    p.set_defaults(func=cmd_edit)

    p = sub.add_parser("done", help="позначити як виконане")
    p.add_argument("id", type=int, help="номер завдання")
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("delete", help="видалити завдання")
    p.add_argument("id", type=int, help="номер завдання")
    p.set_defaults(func=cmd_delete)

    p = sub.add_parser("search", help="пошук завдань за текстом")
    p.add_argument("query", help="що шукати")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("stats", help="статистика завдань")
    p.set_defaults(func=cmd_stats)

    p = sub.add_parser("clear", help="видалити всі виконані завдання")
    p.set_defaults(func=cmd_clear)

    p = sub.add_parser("undone", help="зняти позначку виконання")
    p.add_argument("id", type=int, help="номер завдання")
    p.set_defaults(func=cmd_undone)

    p = sub.add_parser("doneall", help="позначити всі завдання виконаними")
    p.set_defaults(func=cmd_doneall)

    p = sub.add_parser("reset", help="видалити всі завдання")
    p.set_defaults(func=cmd_reset)

    p = sub.add_parser("sort", help="показати завдання за алфавітом")
    p.set_defaults(func=cmd_sort)

    p = sub.add_parser("export", help="експортувати список у TXT-файл")
    p.add_argument("filename", nargs="?", default="tasks.txt", help="ім'я файлу")
    p.set_defaults(func=cmd_export)

    p = sub.add_parser("count", help="кількість завдань")
    p.set_defaults(func=cmd_count)

    p = sub.add_parser("first", help="показати перше завдання")
    p.set_defaults(func=cmd_first)

    p = sub.add_parser("last", help="показати останнє завдання")
    p.set_defaults(func=cmd_last)

    p = sub.add_parser("import", help="імпортувати завдання з TXT (рядок = завдання)")
    p.add_argument("filename", help="ім'я файлу")
    p.set_defaults(func=cmd_import)

    return parser

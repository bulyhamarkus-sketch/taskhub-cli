"""Сховище: читання та запис завдань у JSON-файл."""

import json
import os

from core import TaskError

DATA_FILE = "tasks.json"


def load_tasks():
    """Читає завдання. Якщо файлу немає - повертає порожній список."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise TaskError("файл даних пошкоджений.")


def save_tasks(tasks):
    """Записує завдання у JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

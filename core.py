"""Ядро (бізнес-логіка): робота зі списком завдань.

Тут немає print, input, sys.exit і роботи з файлами.
Лише чисті функції, які приймають і повертають дані.
Помилки сигналізуються через TaskError.
"""


class TaskError(Exception):
    """Помилка роботи із завданнями (некоректне введення, немає завдання)."""


# ---------- Перевірка ----------

def validate_text(text):
    """Текст не може бути порожнім. Повертає очищений текст."""
    text = text.strip()
    if not text:
        raise TaskError("текст завдання не може бути порожнім.")
    return text


def find_task(tasks, task_id):
    """Повертає завдання за номером або викликає TaskError."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise TaskError(f"завдання з номером {task_id} не існує.")


# ---------- Зміна даних ----------

def next_id(tasks):
    """Наступний номер = максимальний + 1."""
    return max((t["id"] for t in tasks), default=0) + 1


def add_task(tasks, text):
    task = {"id": next_id(tasks), "text": validate_text(text), "done": False}
    tasks.append(task)
    return task


def edit_task(tasks, task_id, text):
    task = find_task(tasks, task_id)
    task["text"] = validate_text(text)
    return task


def set_done(tasks, task_id, done):
    task = find_task(tasks, task_id)
    task["done"] = done
    return task


def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    tasks.remove(task)
    return task


def mark_all_done(tasks):
    for task in tasks:
        task["done"] = True
    return len(tasks)


def clear_done(tasks):
    """Повертає (список невиконаних, кількість видалених)."""
    left = [t for t in tasks if not t["done"]]
    return left, len(tasks) - len(left)


# ---------- Вибірки ----------

def filter_tasks(tasks, done=None):
    """done=True - виконані, done=False - невиконані, None - усі."""
    if done is None:
        return list(tasks)
    return [t for t in tasks if t["done"] == done]


def search_tasks(tasks, query):
    query = validate_text(query).lower()
    return [t for t in tasks if query in t["text"].lower()]


def sort_tasks(tasks):
    return sorted(tasks, key=lambda t: t["text"].lower())


def get_stats(tasks):
    """Повертає (усього, виконано, залишилось)."""
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    return total, done, total - done


# ---------- Форматування ----------

def format_task(task):
    mark = "[x]" if task["done"] else "[ ]"
    return f"{task['id']:>3}. {mark} {task['text']}"


def parse_lines(lines):
    """Рядки тексту -> список текстів завдань (порожні пропускаємо)."""
    return [line.strip() for line in lines if line.strip()]

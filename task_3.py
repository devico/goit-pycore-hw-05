"""
Простий аналізатор логів:
- Рахує кількість записів за рівнями (INFO, DEBUG, ERROR, WARNING)
- За другим аргументом виводить деталі для конкретного рівня

Використання:
    python main.py /path/to/logfile.log
    python main.py /path/to/logfile.log error
"""

import sys
from pathlib import Path

LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> dict:
    """
    Парсить рядок формату:
        YYYY-MM-DD HH:MM:SS LEVEL message...
    Повертає словник з ключами: date, time, level, message.
    Кидає ValueError для некоректного рядка.
    """
    line = line.strip()
    if not line:
        raise ValueError("Порожній рядок")

    parts = line.split(maxsplit=3)  # дата, час, рівень, повідомлення
    if len(parts) < 4:
        raise ValueError("Некоректний формат")
    date, time, level, message = parts
    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
    }


def load_logs(file_path: str) -> list:
    """
    Зчитує файл та повертає список словників-логів.
    Невалідні рядки пропускає.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не знайдено: {file_path}")
    if not path.is_file():
        raise OSError(f"Шлях не є файлом: {file_path}")

    logs = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                logs.append(parse_log_line(line))
            except ValueError:
                # пропускаємо биті рядки
                continue
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Повертає всі логи з вказаним рівнем (list comprehension).
    """
    lvl = level.upper()
    return [rec for rec in logs if rec.get("level") == lvl]


def count_logs_by_level(logs: list) -> dict:
    """
    Рахує кількість записів лише для стандартних рівнів.
    """
    counts = {lvl: 0 for lvl in LEVELS}
    for rec in logs:
        lvl = rec.get("level")
        if lvl in counts:
            counts[lvl] += 1
    return counts


def display_log_counts(counts: dict) -> None:
    """
    Друкує таблицю підрахунків у простому форматі.
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for lvl in LEVELS:
        print(f"{lvl:<16} | {counts.get(lvl, 0)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання:\n  python main.py /path/to/logfile.log [level]")
        raise SystemExit(1)

    file_path = sys.argv[1]
    level_arg = sys.argv[2] if len(sys.argv) >= 3 else None

    try:
        logs = load_logs(file_path)
        counts = count_logs_by_level(logs)
        display_log_counts(counts)

        if level_arg:
            selected = filter_logs_by_level(logs, level_arg)
            lvl = level_arg.upper()
            print(f"\nДеталі логів для рівня '{lvl}':")
            if not selected:
                print("(немає записів)")
            else:
                for rec in selected:
                    print(f"{rec['date']} {rec['time']} - {rec['message']}")

    except FileNotFoundError as e:
        print(f"Помилка: {e}")
        raise SystemExit(1)
    except OSError as e:
        print(f"Помилка доступу до файлу: {e}")
        raise SystemExit(1)
    except Exception as e:
        print(f"Неочікувана помилка: {e}")
        raise SystemExit(1)

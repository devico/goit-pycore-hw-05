import re
from typing import Callable, Iterable


def generator_numbers(text: str) -> Iterable[float]:
    """
    Повертає генератор дійсних чисел із тексту.
    Числа вважаються коректними та чітко відокремленими пробілами з обох боків.

    :param text: рядок із текстом, що містить числа
    :return: генератор чисел типу float
    """
    # Додаємо пробіли з обох боків, щоб коректно працювали перевірки меж
    padded = f" {text} "
    # Шукаємо числа зі знаком/без, з дробовою частиною/без, оточені пробілами
    pattern = r'(?<=\s)[+-]?\d+(?:\.\d+)?(?=\s)'

    for m in re.finditer(pattern, padded):
        yield float(m.group())


def sum_profit(text: str, func: Callable[[str], Iterable[float]]) -> float:
    """
    Обчислює суму всіх чисел у тексті, використовуючи наданий генератор.

    :param text: рядок із текстом, що містить числа
    :param func: функція-генератор, яка повертає ітератор чисел з тексту
    :return: загальна сума як float
    """
    return sum(func(text))


# Приклад використання:
text = (
    "Загальний дохід працівника складається з декількох частин: "
    "1000.01 як основний дохід, доповнений додатковими надходженнями "
    "27.45 і 324.00 доларів."
)
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")  # Очікувано: 1351.46

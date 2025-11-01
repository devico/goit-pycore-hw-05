def caching_fibonacci():
    """
    Повертає внутрішню функцію fibonacci(n), яка обчислює n-те число Фібоначчі
    з використанням кешу (замикання з лексичним оточенням словника cache).
    """

    cache = {}  # словник для збереження вже обчислених значень

    def fibonacci(n: int) -> int:
        """
        Обчислює n-те число Фібоначчі рекурсивно з кешуванням.

        Правила:
        - якщо n <= 0 -> повертаємо 0
        - якщо n == 1 -> повертаємо 1
        - якщо значення є у кеші -> віддаємо з cache
        - інакше рекурсивно обчислюємо, зберігаємо у cache та повертаємо
        """
        if n <= 0:
            return 0
        if n == 1:
            return 1
        if n in cache:
            return cache[n]

        # рекурсивне обчислення з кешуванням
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


# Приклад використання:
fib = caching_fibonacci()

print(fib(10))  # 55
print(fib(15))  # 610

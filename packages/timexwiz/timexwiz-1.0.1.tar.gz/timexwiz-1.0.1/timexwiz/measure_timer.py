from time import process_time_ns


class Timer:
    """
    Класс Timer предоставляет простой способ измерения времени выполнения кода в наносекундах и миллисекундах.

    Пример использования:

    with Timer() as t:
        # Ваш код здесь
    print(f"Время выполнения: {t.result_ms} мс")
    """
    def __init__(self):
        self.start = 0
        self.end = 0
        self.result_ns = 0
        self.result_ms = 0

    def __enter__(self):
        self.start = process_time_ns()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = process_time_ns()
        self.result_ns = self.end - self.start
        self.result_ms = self.result_ns / 1_000_000.0

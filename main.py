"""Description."""
import datetime as dt

FORMAT = "%H:%M:%S"
WEIGHT = 75  # Вес
HEIGHT = 175  # Рост
K_1 = 0.035  # Коэффициент для подсчета калорий
K_2 = 0.029  # Коэффициент для подсчета калорий
STEP_M = 0.65  # Длина шага в метрах


storage_data: tuple[dt.time, int] = (dt.time(0, 0), 0)


def check_correct_data(data: tuple[dt.time, int]) -> bool:
    """Проверка корректности полученного пакета."""
    if len(data) != 2 or None in data:
        return False
    return True


def check_correct_time(time: dt.time) -> bool:
    """Проверка корректности параметра времени."""
    if storage_data and time <= max(storage_data):
        return False
    return True


def get_step_day(steps: int) -> int:
    """Получить количество пройденных шагов за день."""
    day_steps = sum(value for value in storage_data.values())
    return day_steps + steps


def get_distance(steps: int) -> float:
    """Получить дистанцию пройденного пути в км."""
    return steps * STEP_M / 1000


def get_spent_calories(dist: float, current_time: dt.time) -> float:
    """Получить значения потраченных калорий."""
    time = current_time.hour + current_time.minute / 60
    mean_speed = (dist / time)
    tmp = mean_speed ** 2 // HEIGHT
    return (K_1 * WEIGHT + tmp * K_2 * WEIGHT) * time * 60


def get_achievement(dist: float) -> str:
    """Получить поздравления за пройденную дистанцию."""
    if dist < 2:
        return 'Лежать тоже полезно. Главное — участие, а не победа!'
    if dist < 3.9:
        return 'Маловато, но завтра наверстаем!'
    if dist < 6.5:
        return 'Неплохо! День был продуктивным.'
    return 'Отличный результат! Цель достигнута.'


def show_message(time: dt.time, steps: int, dist: float, calories: float,
                 achiev: str) -> None:
    """Вывести на экран результаты вычислений."""
    print(f'''
Время: {time}.
Количество шагов за сегодня: {steps}.
Дистанция составила {dist:.2f} км.
Вы сожгли {calories:.2f} ккал.
{achiev}
        ''')


def accept_package(data: tuple[dt.time, int]) -> tuple[dt.time, int]:
    """Обработать пакет данных."""
    if not check_correct_data(data):
        return 'Некорректный пакет'

    time, steps = data
    pack_time = dt.datetime.strptime(time, FORMAT).time()

    if not check_correct_time(pack_time):
        return 'Некорректное значение времени'

    day_steps = get_step_day(steps)
    dist = get_distance(day_steps)
    spent_calories = get_spent_calories(dist, pack_time)
    achievement = get_achievement(dist)
    show_message(pack_time, day_steps, dist, spent_calories, achievement)

    storage_data[pack_time] = steps

    return storage_data


if __name__ == '__main__':
    # Пример запуска
    package_0 = ('2:00:01', 505)
    package_1 = (None, 3211)
    package_2 = ('9:36:02', 15000)
    package_3 = ('9:36:02', 9000)
    package_4 = ('8:01:02', 7600)

    accept_package(package_0)
    accept_package(package_1)
    accept_package(package_2)
    accept_package(package_3)
    accept_package(package_4)

from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
    # Никак не могу понять, как вынести сообщение на уровень класса.
    # Пробовал вынести весь блок кода после return в переменную
    # MESSAGE, но тогда Python ругается на то, что переменные не
    # определены.


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,  # <- Вызывает ошибку теста
                           self.duration,            # у Яндекса.
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * Training.get_mean_speed(self)
                + self.CALORIES_MEAN_SPEED_SHIFT) \
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        """Расчёт количества калорий, израсходованных за тренировку."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + (self.get_mean_speed() * self.KMH_IN_MSEC)**2
                 / (self.height / self.CM_IN_M)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""

    CALORIES_WEIGHT_MULTIPLIER: int = 2
    CALORIES_MEAN_SPEED_SHIFT: float = 1.1
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения при плавании."""
        return self.length_pool * self.count_pool / self.M_IN_KM \
            / self.duration

    def get_spent_calories(self):
        """Расчёт количества калорий, израсходованных за тренировку."""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {'RUN': Running,
                         'WLK': SportsWalking,
                         'SWM': Swimming}
    if workout_type in workout_type_dict:
        workout: Training = workout_type_dict[workout_type](*data)
        return workout
    else:
        print('Что-то пошло не так. Мы работаем над проблемой!')

    # Или так?
    # try:
    #     workout: Training = workout_type_dict[workout_type](*data)
    #     return workout
    # except AttributeError:
    #     print('Что-то пошло не так. Мы работаем над проблемой! (ERR: AE')
    # except KeyError:
    #     print('Что-то пошло не так. Мы работаем над проблемой! (ERR: KE')
    # except TypeError:
    #     print('Что-то пошло не так. Мы работаем над проблемой! (ERR: TE')


def main(training: Training) -> None:
    """Главная функция."""
    info = Training.show_training_info(training)
    return print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

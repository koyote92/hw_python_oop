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
        total_distance = self.action * self.LEN_STEP / self.M_IN_KM
        return total_distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий при беге."""
        calories_mult = self.CALORIES_MEAN_SPEED_MULTIPLIER \
            * Training.get_mean_speed(self) \
            + self.CALORIES_MEAN_SPEED_SHIFT

        calories_spent = calories_mult * self.weight / self.M_IN_KM \
            * self.duration * self.MIN_IN_H

        return calories_spent
    # тот, кто придумал проверять результат до 14 знака, работает над ПО для
    # исследования космоса??? Он так же сидит и в формулах математиков
    # скобки раскрывает? Не дай Бог, пользователю насчитает за месяц лишнюю
    # калорию, блин...


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
        speed_in_msec = (self.get_mean_speed() * self.KMH_IN_MSEC)**2

        height_in_meters = self.height / self.CM_IN_M

        speed = speed_in_msec / height_in_meters

        weight_cal_mult = self.CALORIES_WEIGHT_MULTIPLIER * self.weight

        speed_cal_mult = self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight

        return ((weight_cal_mult + speed * speed_cal_mult) * self.duration
                * self.MIN_IN_H)
    # тот, кто придумал проверять результат до 14 знака, работает над ПО для
    # исследования космоса??? Он так же сидит и в формулах математиков
    # скобки раскрывает? Не дай Бог, пользователю насчитает за месяц лишнюю
    # калорию, блин...


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
        swimming_mean_speed = (self.length_pool * self.count_pool
                               / self.M_IN_KM / self.duration)
        return swimming_mean_speed

    def get_spent_calories(self):
        """Расчёт количества калорий, израсходованных за тренировку."""
        return ((self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)
    # а вот здесь претензий нет, программирование - точная наука!


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict = {'RUN': Running,
                         'WLK': SportsWalking,
                         'SWM': Swimming}
    workout: Training = workout_type_dict[workout_type](*data)
    return workout


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

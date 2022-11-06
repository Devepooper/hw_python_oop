class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration} ч.; '
                f'Дистанция: {self.distance} км; '
                f'Ср. скорость: {self.speed} км/ч; '
                f'Потрачено ккал: {self.calories}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
        CALORIES_MEAN_SPEED_SHIFT: float = 1.79
        return ((CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + CALORIES_MEAN_SPEED_SHIFT)
                * self.weight) / (self.M_IN_KM * self.duration)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        CALORIES_MEAN_SPEED_MULTIPLIER: float = 0.035
        CALORIES_MEAN_SPEED_SHIFT: float = 0.029
        average_speed = self.get_mean_speed()
        minute_in_hour: int = 60
        time_in_minutes = self.duration * minute_in_hour
        return ((CALORIES_MEAN_SPEED_MULTIPLIER
                * self.weight + ((average_speed**2) / self.height)
                * CALORIES_MEAN_SPEED_SHIFT
                * self.weight) * time_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool
    LEN_STEP: float = 1.38

    def get_spent_calories(self) -> float:
        return (((self.lenght_pool * self.count_pool) / self.M_IN_KM)
                / self.duration)

    def get_mean_speed(self) -> float:
        calories_consumed1: float = 1.1
        calories_consumed2: float = 2
        average_speed = self.get_mean_speed()
        return (((average_speed + calories_consumed1) * calories_consumed2)
                * self.weight * self.duration)

    def get_distance(self) -> float:
        return self.action * self.LEN_STEP / self.M_IN_KM


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_info = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking
                     }
    return training_info[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

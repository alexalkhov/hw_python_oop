class InfoMessage:
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories
    """Информационное сообщение о тренировке."""
    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MINUTES_IN_HOUR = 60

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
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info = InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        return info


class Running(Training):
    """Тренировка: бег."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_COEF = 60

    def get_spent_calories(self) -> float:
        spent_calories = (
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * self.weight / self.M_IN_KM * self.duration * self.MIN_COEF
        return spent_calories


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
    LEN_STEP = 0.65
    WEIGHT_MULTIPLIER = 0.035
    SPEED_MULTIPLIER = 2
    WEIGHT_MULTIPLIER_2 = 0.029
    SPEED_IN_SEC_MULTIPLIER = 0.278
    DURAITION_IN_MIN_COEF = 60
    HEIGHT_CONST = 100

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.WEIGHT_MULTIPLIER
             * self.weight
             + ((self.get_mean_speed() * self.SPEED_IN_SEC_MULTIPLIER)
                ** self.SPEED_MULTIPLIER / (self.height / self.HEIGHT_CONST))
             * self.WEIGHT_MULTIPLIER_2 * self.weight)
            * (self.duration * self.DURAITION_IN_MIN_COEF))
        return spent_calories


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
        self.length_pool = length_pool
        self.count_pool = count_pool
    LEN_STEP = 1.38
    M_IN_KM = 1000
    SPEED_ADD = 1.1
    FUNCTION_MILTIPLIER = 2

    def get_mean_speed(self) -> float:
        mean_speed = (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (
            self.get_mean_speed() + self.SPEED_ADD) * \
            self.FUNCTION_MILTIPLIER * self.weight * self.duration
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking}
    return training_type[workout_type](*data)


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

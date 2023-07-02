from dataclasses import dataclass, asdict
from typing import Dict, Type, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE_DICT: ClassVar[str] = (
        'Тип тренировки: {training_type}; Длительность: {duration:.3f} ч.;'
        ' Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} км/ч;'
        ' Потрачено ккал: {calories:.3f}.')

    def get_message(self):
        return self.MESSAGE_DICT.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    MINUTES_IN_HOUR: ClassVar[float] = 60

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
        raise NotImplementedError('Метод не определен')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    MIN_COEF: ClassVar[float] = 60

    def get_spent_calories(self) -> float:
        return (
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
            + self.CALORIES_MEAN_SPEED_SHIFT
        ) * self.weight / self.M_IN_KM * self.duration * self.MIN_COEF


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP: ClassVar[float] = 0.65
    WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    SPEED_MULTIPLIER: ClassVar[float] = 2
    WEIGHT_MULTIPLIER_2: ClassVar[float] = 0.029
    SPEED_IN_SEC_MULTIPLIER: ClassVar[float] = 0.278
    DURAITION_IN_MIN_COEF: ClassVar[float] = 60
    HEIGHT_CONST: ClassVar[float] = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (
            (self.WEIGHT_MULTIPLIER
             * self.weight
             + ((self.get_mean_speed() * self.SPEED_IN_SEC_MULTIPLIER)
                ** self.SPEED_MULTIPLIER / (self.height / self.HEIGHT_CONST))
             * self.WEIGHT_MULTIPLIER_2 * self.weight)
            * (self.duration * self.DURAITION_IN_MIN_COEF))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    M_IN_KM: ClassVar[float] = 1000
    ADD_SPEED: ClassVar[float] = 1.1
    FUNCTION_MILTIPLIER: ClassVar[float] = 2

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

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed()
                          + self.ADD_SPEED) * (self.FUNCTION_MILTIPLIER
                                               * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_class := training_type.get(workout_type):
        return workout_class(*data)
    raise ValueError(f"Неизвестный тип тренировки: {workout_type}")


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

from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Метод. Возврат сообщение о тренировке."""
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_IN_H = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f"Добавить get_spent calories в {self.__class__.__name__}"
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Расход калорий для бега."""
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * (self.duration * self.MIN_IN_H)
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KM_IN_HS = 0.278
    SM_IN_M = 100
    CALORIES_MEAN_SPEED_WALKING_1 = 0.035
    CALORIES_MEAN_SPEED_WALKING_2 = 0.029

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Расход калорий для ходьбы."""
        return (
            (
                self.CALORIES_MEAN_SPEED_WALKING_1
                * self.weight
                + (
                    (self.get_mean_speed() * self.KM_IN_HS) ** 2
                    / (self.height / self.SM_IN_M)
                )
                * self.CALORIES_MEAN_SPEED_WALKING_2
                * self.weight
            )
            * (self.duration * self.MIN_IN_H)
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SWIMMING_1 = 1.1
    CALORIES_MEAN_SPEED_SWIMMING_2 = 2

    action: int
    duration: float
    weight: float
    length_pool: int  # длина бассейна
    count_pool: int  # сколько раз переплыл бассейн

    def get_mean_speed(self) -> float:
        """Расчёт средней скорости при плавании."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расход калорий для плаванья."""
        return (
            (self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SWIMMING_1)
            * self.CALORIES_MEAN_SPEED_SWIMMING_2
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_workout = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    if workout_type not in type_workout:
        raise ValueError('Переданы неверные данные, '
                         'разрешенно использовать "SWM", "RUN", "WLK".')
    return type_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))

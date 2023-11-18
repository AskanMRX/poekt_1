class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type  # имя класса тренировки
        self.duration = duration  # длительность тренировки в часах
        self.distance = distance  # дистанция в кm, за время тренировки
        self.speed = speed  # средняя скорость, с которой двигался пользователь
        self.calories = calories  # количество ккал, за время тренировки

    def get_message(self) -> str:
        """Метод. Возврат сообщение о тренировке."""
        message: str = (f'Тип тренировки: {self.training_type}; '
                        f'Длительность: {self.duration:.3f} ч.; '
                        f'Дистанция: {self.distance:.3f} км; '
                        f'Ср. скорость: {self.speed:.3f} км/ч; '
                        f'Потрачено ккал: {self.calories:.3f}.')
        return message


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000  # метры в километры
    LEN_STEP = 0.65  # коэффициент шагов в метры
    MIN_IN_H = 60  # часы в минуты

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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18  # коэффициент для формулы 1
    CALORIES_MEAN_SPEED_SHIFT = 1.79  # коэффициент для формулы 2

    def get_spent_calories(self) -> float:
        """Расход калорий для бега."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    KM_IN_HS = 0.278  # км/ч в м/с
    SM_IN_M = 100  # сантисетры в метры
    MIN_IN_H = 60  # часы в минуты
    CALORIES_MEAN_SPEED_WALKING_1 = 0.035  # коэффициент для формулы 1
    CALORIES_MEAN_SPEED_WALKING_2 = 0.029  # коэффициент для формулы 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расход калорий для ходьбы."""
        return ((self.CALORIES_MEAN_SPEED_WALKING_1 * self.weight
                + ((self.get_mean_speed() * self.KM_IN_HS)**2
                   / (self.height / self.SM_IN_M))
                * self.CALORIES_MEAN_SPEED_WALKING_2 * self.weight)
                * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_MEAN_SPEED_SWIMMING_1 = 1.1
    CALORIES_MEAN_SPEED_SWIMMING_2 = 2

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
        """Расчёт средней скорости при плавании."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расход калорий для плаванья."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SWIMMING_1)
                * self.CALORIES_MEAN_SPEED_SWIMMING_2 * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_workout = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    if workout_type in type_workout:
        training_type = type_workout[workout_type]
        return training_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
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

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс, от которого наследуются другие игоровые объекты."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self, position):
        """Метод для отрисовки ячейки."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Унаследованный класс, описывающий яблоко и действия с ним."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод, случайным образом выбирающий координаты положения яблока."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)


class Snake(GameObject):
    """Унаследованный класс, описывающий змейку и ее поведение."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        """Метод, который отрисовывает змейку на экране."""
        for position in self.positions[:-1]:
            super().draw(position)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, описывающий обновление позиции змейки."""
        x_position, y_position = self.get_head_position()
        x_direction, y_direction = self.direction[0], self.direction[1]

        x_position += x_direction * GRID_SIZE
        y_position += y_direction * GRID_SIZE

        x_position %= SCREEN_WIDTH
        y_position %= SCREEN_HEIGHT

        self.positions.insert(0, (x_position, y_position))

        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Метод, возвращающий позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Возвращает змейку в исходное положение, как при начале игры."""
        self.positions = [self.position]
        self.length = 1
        self.next_direction = choice((UP, DOWN, RIGHT, LEFT))
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция, которая обрабатывает действия пользователя (нажатие клавиш)."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция логики игры."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.update_direction()
        snake.last = snake.positions[-1]
        snake.move()

        if snake.positions[0] == apple.position:
            apple.position = apple.randomize_position()
            snake.length += 1

        while True:
            if apple.position in snake.positions:
                apple.position = apple.randomize_position()
            else:
                break

        if snake.positions[0] in snake.positions[1:]:
            snake.reset()

        apple.draw(apple.position)
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()

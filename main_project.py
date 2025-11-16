import pygame
import random
import sys


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE


BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:

    def __init__(self, position, color):

        self.position = position
        self.color = color

    def draw(self, surface):

        rect = pygame.Rect(self.position[0], self.position[1], CELL_SIZE,
                           CELL_SIZE)
        pygame.draw.rect(surface, self.color, rect)


class Apple(GameObject):

    def __init__(self):

        super().__init__(self.randomize_position(), APPLE_COLOR)

    def randomize_position(self):

        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        return (x, y)

    def respawn(self, snake_positions):

        while True:
            new_pos = self.randomize_position()
            if new_pos not in snake_positions:
                self.position = new_pos
                break


class Snake:

    def __init__(self):

        center_x = (GRID_WIDTH // 2) * CELL_SIZE
        center_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.body_color = SNAKE_COLOR

    def update_direction(self):

        if (self.next_direction[0] * -1,
                self.next_direction[1] * -1) != self.direction:
            self.direction = self.next_direction

    def move(self):

        head_x, head_y = self.positions[0]
        delta_x = self.direction[0] * CELL_SIZE
        delta_y = self.direction[1] * CELL_SIZE
        new_head = ((head_x + delta_x) % SCREEN_WIDTH, (head_y + delta_y)
                    % SCREEN_HEIGHT)

        if new_head in self.positions:
            return False
        self.positions = [new_head] + self.positions[:-1]
        return True

    def grow(self):

        self.positions.append(self.positions[-1])
        self.length += 1

    def shrink(self):

        if self.length > 1:
            self.positions.pop()
            self.length -= 1
        else:
            self.reset()

    def draw(self, surface):

        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):

        return self.positions[0]

    def reset(self):

        center_x = (GRID_WIDTH // 2) * CELL_SIZE
        center_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.positions = [(center_x, center_y)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = RIGHT


def handle_keys(snake):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Змейка")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        alive = snake.move()
        if not alive:

            snake.reset()

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.respawn(snake.positions)

        screen.fill(BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()
        clock.tick(10)


if __name__ == "__main__":
    main()

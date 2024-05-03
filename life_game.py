import pygame
import numpy as np
import time

pygame.init()

# Определение размера окна и ячеек
width, height = 1000, 1000
rows, cols = 100, 100
cell_size_x = width // cols
cell_size_y = height // rows

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра Жизнь")

# Инициализация поля
field = np.zeros((rows, cols))

# Функция для создания случайного начального состояния поля
def random_initial_state():
    return np.random.choice([0, 1], size=(rows, cols))

# Функция для рисования поля
def draw_field():
    screen.fill(WHITE)
    for x in range(cols):
        for y in range(rows):
            if field[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * cell_size_x, y * cell_size_y, cell_size_x, cell_size_y))
            else:
                pygame.draw.rect(screen, WHITE, (x * cell_size_x, y * cell_size_y, cell_size_x, cell_size_y), 1)
    pygame.display.update()

# Функция для обновления состояния поля в соответствии с правилами игры
def update_field():
    global field
    new_field = np.copy(field)
    for x in range(cols):
        for y in range(rows):
            count = count_neighbors(x, y)
            if field[y][x] == 1 and (count < 2 or count > 3):
                new_field[y][x] = 0
            elif field[y][x] == 0 and count == 3:
                new_field[y][x] = 1
    field = new_field

# Функция для подсчета числа соседей клетки
def count_neighbors(x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            count += field[row][col]
    count -= field[y][x]
    return count

# Основной цикл игры
field = random_initial_state()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_field()
    update_field()
    time.sleep(0.3)

pygame.quit()

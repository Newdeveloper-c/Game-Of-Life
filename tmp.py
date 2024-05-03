import pygame
import numpy as np
import time
import math

pygame.init()

# Определение размера окна и ячеек
width, height = 780, 780
rows, cols = 70, 70
cell_size_x = math.ceil(width / cols)
cell_size_y = math.ceil(height / rows)

# Определение цветов
BLACK = (64, 100, 100)
WHITE = (255, 255, 255)
YELLOW = (255, 128, 0)
GREEN = (45, 185, 50)
YELLOW_RACE = 0
GREEN_RACE = 1
# Создание окна
screen = pygame.display.set_mode((width, height), 0, pygame.OPENGL)
pygame.display.set_caption("Игра Жизнь")

# Инициализация поля и рас
field = np.zeros((rows, cols))
races = np.full((rows, cols), -1)

# Константы для начальных точек и количества клеток для каждой расы
YELLOW_START_POINT = [25, 35]
GREEN_START_POINT = [10, 35]
#NUM_CELLS_PER_RACE = 35
CELLS_SQUARE_SIZE = 6

# Функция для рисования поля с учетом рас
def draw_field():
    screen.fill(WHITE)
    for x in range(cols):
        for y in range(rows):
            pygame.draw.rect(screen, BLACK, (x * cell_size_x, y * cell_size_y, cell_size_x, cell_size_y), 1)
            if field[y][x] == 1:
                if races[y][x] == YELLOW_RACE:
                    pygame.draw.rect(screen, YELLOW, (x * cell_size_x + 1, y * cell_size_y + 1, cell_size_x - 1, cell_size_y - 1))
                elif races[y][x] == GREEN_RACE:
                    pygame.draw.rect(screen, GREEN, (x * cell_size_x + 1, y * cell_size_y + 1, cell_size_x - 1, cell_size_y - 1))
    pygame.display.update()

# Функция для обновления состояния поля в соответствии с правилами игры
def update_field():
    global field
    global races
    new_field = np.copy(field)
    for x in range(cols):
        for y in range(rows):
            count_yellow, count_green = count_neighbors(x, y)
            if field[y][x] == 1:
                if count_yellow > count_green:
                    new_field[y][x] = 1
                    races[y][x] = YELLOW_RACE
                elif count_green > count_yellow:
                    new_field[y][x] = 1
                    races[y][x] = GREEN_RACE
                elif count_yellow < 2 or count_yellow > 3:
                    new_field[y][x] = 0
                    races[y][x] = -1
                elif count_green < 2 or count_green > 3:
                    new_field[y][x] = 0
                    races[y][x] = -1
            else:
                if count_yellow == 3:
                    new_field[y][x] = 1
                    races[y][x] = YELLOW_RACE
                elif count_green == 3:
                    new_field[y][x] = 1
                    races[y][x] = GREEN_RACE

    field = new_field

# Функция для подсчета числа соседей каждой расы для клетки
def count_neighbors(x, y):
    count_yellow = 0
    count_green = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            col = (x + i + cols) % cols
            row = (y + j + rows) % rows
            if races[row][col] == 0:
                count_yellow += field[row][col]
            elif races[row][col] == 1:
                count_green += field[row][col]
    return count_yellow, count_green

# Установка начальных точек и клеток для каждой расы
field[YELLOW_START_POINT[1]][YELLOW_START_POINT[0]] = 1
field[GREEN_START_POINT[1]][GREEN_START_POINT[0]] = 1
# for _ in range(NUM_CELLS_PER_RACE):
#     cell_x = np.random.randint(max(0, YELLOW_START_POINT[0] - 2), min(cols, YELLOW_START_POINT[0] + 3))
#     cell_y = np.random.randint(max(0, YELLOW_START_POINT[1] - 2), min(rows, YELLOW_START_POINT[1] + 3))
#     field[cell_y][cell_x] = 1
#     races[cell_y][cell_x] = 0
#
# for _ in range(NUM_CELLS_PER_RACE):
#     cell_x = np.random.randint(max(0, GREEN_START_POINT[0] - 2), min(cols, GREEN_START_POINT[0] + 3))
#     cell_y = np.random.randint(max(0, GREEN_START_POINT[1] - 2), min(rows, GREEN_START_POINT[1] + 3))
#     field[cell_y][cell_x] = 1
#     races[cell_y][cell_x] = 1


for x in range(YELLOW_START_POINT[0], YELLOW_START_POINT[0] + CELLS_SQUARE_SIZE):
    for y in range(YELLOW_START_POINT[1], YELLOW_START_POINT[1] + CELLS_SQUARE_SIZE):
        field[y][x] = 1
        races[y][x] = 0

for x in range(GREEN_START_POINT[0], GREEN_START_POINT[0] + CELLS_SQUARE_SIZE):
    for y in range(GREEN_START_POINT[1], GREEN_START_POINT[1] + CELLS_SQUARE_SIZE):
        field[y][x] = 1
        races[y][x] = 1

# Основной цикл игры
running = True
# clock = pygame.time.Clock()  # Создаем объект Clock для управления FPS
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_field()
    update_field()
    pygame.display.update()
    # clock.tick(1)  # Устанавливаем максимальное количество кадров в секунду
    time.sleep(0.1)

pygame.quit()

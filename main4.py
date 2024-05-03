import pygame
import numpy as np
import time

pygame.init()

# Определение размера окна и ячеек
width, height = 1000, 1000
rows, cols = 50, 50
cell_size_x = width // cols
cell_size_y = height // rows

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (150, 150, 0)
GREEN = (0, 150, 0)

# Создание окна
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Игра Жизнь")

# Инициализация поля и рас
field = np.zeros((rows, cols))
races = np.full((rows, cols), -1)

# Функция для рисования поля с учетом рас
def draw_field():
    screen.fill(WHITE)
    for x in range(cols):
        for y in range(rows):
            pygame.draw.rect(screen, BLACK, (x * cell_size_x, y * cell_size_y, cell_size_x, cell_size_y), 1)
            if field[y][x] == 1:
                if races[y][x] == 0:
                    pygame.draw.rect(screen, YELLOW, (x * cell_size_x + 1, y * cell_size_y + 1, cell_size_x - 1, cell_size_y - 1))
                else:
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
                if count_yellow == count_green:  # Если соседей у обеих рас одинаково
                    if races[y][x] == 0:
                        new_field[y][x] = 0
                    elif races[y][x] == 1:
                        new_field[y][x] = 1
                elif count_yellow > count_green:
                    if races[y][x] == 0:
                        new_field[y][x] = 0
                    else:
                        new_field[y][x] = 1
                else:
                    if races[y][x] == 1:
                        new_field[y][x] = 1
                    else:
                        new_field[y][x] = 0
            elif count_yellow == 1 and count_green == 0:
                new_field[y][x] = 1
                races[y][x] = 0
            elif count_yellow == 0 and count_green == 1:
                new_field[y][x] = 1
                races[y][x] = 1
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

# Основной цикл игры
running = True
clock = pygame.time.Clock()  # Создаем объект Clock для управления FPS
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_field()
    update_field()
    pygame.display.update()
    clock.tick(1)  # Устанавливаем максимальное количество кадров в секунду

pygame.quit()

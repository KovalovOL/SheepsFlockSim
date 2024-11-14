from random import randint
from math import sqrt
import pygame

# Настройки
W, H = 800, 600         # Размер экрана
FPS = 60                # Частота кадров
N_SHEEP = 20            # Количество овец
SHEEP_RADIUS = 10       # Радиус овцы
SHEEP_ATTRACT_DIST = 70 # Дистанция притяжения овец
SHEEP_REPEL_DIST = 30   # Дистанция отталкивания овец
MOUSE_REPEL_DIST = 50   # Дистанция отталкивания от мыши
FRICTION = 0.9          # Фактор трения

pygame.init()
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()


sheeps = [
    [[randint(int(W * 0.1), int(W * 0.9)), randint(int(H * 0.1), int(H * 0.9))], [0, 0]]
    for _ in range(N_SHEEP)
]

def update_sheeps(mouse_pos):
    for sheep in sheeps:
        pos, speed = sheep
        dx, dy = pos[0] - mouse_pos[0], pos[1] - mouse_pos[1]
        dist_to_mouse = sqrt(dx**2 + dy**2)

        # Collide with mouse
        if dist_to_mouse < MOUSE_REPEL_DIST:
            factor = 0.5 / dist_to_mouse
            speed[0] += dx * factor
            speed[1] += dy * factor

        # Collide with other sheeps
        for other in sheeps:
            if sheep == other: continue
            ox, oy = other[0]
            dx, dy = pos[0] - ox, pos[1] - oy
            dist_to_sheep = sqrt(dx**2 + dy**2)

            if dist_to_sheep > SHEEP_ATTRACT_DIST:
                speed[0] -= dx * 0.0001
                speed[1] -= dy * 0.0001
            elif dist_to_sheep < SHEEP_REPEL_DIST:
                factor = 0.5 / dist_to_sheep
                speed[0] += dx * factor
                speed[1] += dy * factor

        # Friction and update
        speed[0] *= FRICTION
        speed[1] *= FRICTION
        pos[0] = min(max(SHEEP_RADIUS, pos[0] + speed[0]), W - SHEEP_RADIUS)
        pos[1] = min(max(SHEEP_RADIUS, pos[1] + speed[1]), H - SHEEP_RADIUS)

def draw_sheeps():
    screen.fill((0, 161, 43))
    for i, (pos, _) in enumerate(sheeps):
        color = int(200 + 55 * i / len(sheeps))
        pygame.draw.circle(screen, (color, color, color), (int(pos[0]), int(pos[1])), SHEEP_RADIUS)

# main game cycle
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # update sheeps pos and redraw
    update_sheeps(pygame.mouse.get_pos())
    draw_sheeps()
    pygame.display.flip()
    clock.tick(FPS)

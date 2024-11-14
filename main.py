from random import randint
from math import sqrt
import pygame

# Settings
W, H = 1400, 1000       # Screen size
FPS = 60                # Frames per second
N_SHEEP = 20            # Number of sheeps
SHEEP_RADIUS = 10       # Sheep radius
SHEEP_ATTRACT_DIST = 70 # Attraction distance
SHEEP_REPEL_DIST = 30   # Repulsion distance
MOUSE_REPEL_DIST = 50   # Repulsion distance from mouse
DRONE_REPEL_DIST = 60   # Repulsion distance from drone
DRONE_RADIUS = 10       # Drone radius
DRONE_SPEED = 1         # Drone speed
FRICTION = 0.9          # Friction factor

pygame.init()
screen = pygame.display.set_mode((W, H))

# Initialize sheep positions and speeds
sheeps = [
    [[randint(int(W * 0.1), int(W * 0.9)), randint(int(H * 0.1), int(H * 0.9))], [0, 0]]
    for _ in range(N_SHEEP)
]

# Initialize drone position and speed
drone_pos = [W // 2, H // 2]
drone_speed = [0, 0]

# Update sheep behavior
def update_sheeps(mouse_pos, drone_pos):
    for sheep in sheeps:
        pos, speed = sheep
        dx, dy = pos[0] - mouse_pos[0], pos[1] - mouse_pos[1]
        dist_to_mouse = sqrt(dx**2 + dy**2)

        # Repulsion from mouse
        if dist_to_mouse < MOUSE_REPEL_DIST:
            factor = 0.5 / dist_to_mouse
            speed[0] += dx * factor
            speed[1] += dy * factor

        # Interaction with other sheeps
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

        # Repulsion from drone
        dx, dy = pos[0] - drone_pos[0], pos[1] - drone_pos[1]
        dist_to_drone = sqrt(dx**2 + dy**2)

        if dist_to_drone < DRONE_REPEL_DIST:
            factor = 0.5 / dist_to_drone
            speed[0] += dx * factor
            speed[1] += dy * factor

        # Apply friction and update position
        speed[0] *= FRICTION
        speed[1] *= FRICTION
        pos[0] = min(max(SHEEP_RADIUS, pos[0] + speed[0]), W - SHEEP_RADIUS)
        pos[1] = min(max(SHEEP_RADIUS, pos[1] + speed[1]), H - SHEEP_RADIUS)

# Update drone behavior
def update_drone():
    global drone_pos, drone_speed

    # Drone movement with arrow keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        drone_speed[0] -= DRONE_SPEED
    if keys[pygame.K_RIGHT]:
        drone_speed[0] += DRONE_SPEED
    if keys[pygame.K_UP]:
        drone_speed[1] -= DRONE_SPEED
    if keys[pygame.K_DOWN]:
        drone_speed[1] += DRONE_SPEED

    # Apply friction and update drone position
    drone_speed[0] *= FRICTION
    drone_speed[1] *= FRICTION

    drone_pos[0] += drone_speed[0]
    drone_pos[1] += drone_speed[1]

    # Keep drone within screen boundaries
    drone_pos[0] = min(max(DRONE_RADIUS, drone_pos[0]), W - DRONE_RADIUS)
    drone_pos[1] = min(max(DRONE_RADIUS, drone_pos[1]), H - DRONE_RADIUS)

# Draw sheep on screen
def draw_sheeps():
    for i, (pos, _) in enumerate(sheeps):
        color = int(200 + 55 * i / len(sheeps))
        pygame.draw.circle(screen, (color, color, color), (int(pos[0]), int(pos[1])), SHEEP_RADIUS)

# Draw drone on screen
def draw_drone():
    pygame.draw.circle(screen, (255, 0, 0), (int(drone_pos[0]), int(drone_pos[1])), DRONE_RADIUS)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Update logic
    update_sheeps(pygame.mouse.get_pos(), drone_pos)  # Sheep react to both mouse and drone
    update_drone()  # Update drone position

    # Render everything
    screen.fill((0, 161, 43))  # Green background
    draw_sheeps()              # Draw sheep
    draw_drone()               # Draw drone

    pygame.display.flip()
    pygame.time.Clock().tick(FPS)

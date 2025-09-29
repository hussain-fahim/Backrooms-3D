import pygame
import math

# Settings
WIDTH, HEIGHT = 640, 480
FOV = math.pi / 3  # 60 degrees
NUM_RAYS = WIDTH
MAX_DEPTH = 20
TILE_SIZE = 64
FPS = 60

# Colors
BLACK = (0, 0, 0)

# Initialize
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load texture
texture = pygame.image.load("bricksx64.png").convert()
texture_width, texture_height = texture.get_size()

# Map
world_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]
map_rows = len(world_map)
map_cols = len(world_map[0])

# Player
player_x = 100
player_y = 100
player_angle = 0
player_speed = 3
rotation_speed = 0.04


def cast_ray(angle):
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)

    # step sizes
    for depth in range(1, MAX_DEPTH * TILE_SIZE):
        x = player_x + cos_a * depth
        y = player_y + sin_a * depth

        i = int(x // TILE_SIZE)
        j = int(y // TILE_SIZE)

        if 0 <= i < map_cols and 0 <= j < map_rows:
            if world_map[j][i] != 0:
                # Remove fish-eye
                corrected_depth = depth * math.cos(angle - player_angle)

                # Calculate offset for texture_x
                hit_x = x % TILE_SIZE
                hit_y = y % TILE_SIZE

                # Detect if hit was on vertical wall
                is_vertical = abs(cos_a) < abs(sin_a)

                if is_vertical:
                    texture_x = int(hit_x / TILE_SIZE * texture_width)
                else:
                    texture_x = int(hit_y / TILE_SIZE * texture_width)

                # Optional: Flip texture_x for certain directions
                if (is_vertical and cos_a > 0) or (not is_vertical and sin_a < 0):
                    texture_x = texture_width - texture_x - 1

                return corrected_depth, texture_x
    return MAX_DEPTH * TILE_SIZE, 0



def draw_world():
    screen.fill(BLACK)

    ray_angle = player_angle - FOV / 2
    for ray in range(NUM_RAYS):
        depth, texture_x = cast_ray(ray_angle)

        # Remove fish-eye distortion
        depth *= math.cos(player_angle - ray_angle)

        # Calculate wall height
        if depth == 0:
            depth = 0.0001
        wall_height = (TILE_SIZE / depth) * (WIDTH / 2)

        start_y = int((HEIGHT / 2) - wall_height / 2)
        end_y = int((HEIGHT / 2) + wall_height / 2)
        if end_y > HEIGHT:
            end_y = HEIGHT
        if start_y < 0:
            start_y = 0

        for y in range(start_y, end_y):
            texture_y = int(((y - start_y) / wall_height) * texture_height)
            pixel_color = texture.get_at((texture_x, texture_y))
            screen.set_at((ray, y), pixel_color)

        ray_angle += FOV / NUM_RAYS


def move_player():
    global player_x, player_y, player_angle

    keys = pygame.key.get_pressed()
    dx = dy = 0

    if keys[pygame.K_w]:
        dx += math.cos(player_angle) * player_speed
        dy += math.sin(player_angle) * player_speed
    if keys[pygame.K_s]:
        dx -= math.cos(player_angle) * player_speed
        dy -= math.sin(player_angle) * player_speed

    next_x = player_x + dx
    next_y = player_y + dy

    if world_map[int(player_y // TILE_SIZE)][int(next_x // TILE_SIZE)] == 0:
        player_x = next_x
    if world_map[int(next_y // TILE_SIZE)][int(player_x // TILE_SIZE)] == 0:
        player_y = next_y

    if keys[pygame.K_a]:
        player_angle -= rotation_speed
    if keys[pygame.K_d]:
        player_angle += rotation_speed


def main():
    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        move_player()
        draw_world()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

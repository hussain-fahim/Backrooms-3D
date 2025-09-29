import pygame
import math
import sys
import random

pygame.init()
clock = pygame.time.Clock()

running = True
debug_mode = 0
projection_mode = 1

start_time = 0
elapsed_time = 0

map_cols = 30
map_rows = 20
tile_size = 32
screen_width = map_cols * tile_size
screen_height = map_rows * tile_size


real_colour = (0,0,0)

char = ["char1.png","char2.png","char3.png","char4.png","char5.png",]

tile_number = 0
offset = 0

# exception for a function to be here

def score_4_digit(score):
    if score % 10 == score:
        return "000"+str(score)
    elif score % 100 == score:
        return "00"+str(score)
    elif score % 1000 == score:
        return "0"+str(score)
    else:
        return str(score)

# exception for a function to be here


player_x = 150
player_y = 100
player_angle = 90

checkpoint_x = player_x
checkpoint_y = player_y
checkpoint_deg = player_angle

movement_speed = 0.0006
rotation_speed = 4

gun_shoot = False
health = 100
ammo = 999
score = 100000 - elapsed_time

HUD_font = pygame.font.Font("Jersey25-Regular.ttf",40)
ammo_text = HUD_font.render(str(ammo)+"ml", False, (0,255,255))
health_text = HUD_font.render(str((health/100) *100)+"%", False, (255, 255, 255))
score_text = HUD_font.render(score_4_digit(math.floor(score)), False, (170, 255, 0))
death_text = HUD_font.render("YOU DIED", False, (255,255,255))
no_ammo_text = HUD_font.render("NO AMMO", False, (255, 255, 255))

fov = 90
rays = 960 * (fov // 90) # beacuse we want 1 ray per vertical pixel line (screen_width)
skew = 9000

future_x = 0
future_y = 0

WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
ORANGE = (255, 165, 0)
YELLOW = (255,255,0)
WALL_COLOUR = (159, 146, 137)

screen = pygame.display.set_mode((int(screen_width), int(screen_height)))
pygame.display.set_caption("Backrooms 3D - BETA")
icon = pygame.image.load("char1.png")
pygame.display.set_icon(icon)

texture = {
    0: pygame.image.load("bricksx64.png").convert(),
    1: pygame.image.load("water_gun_green_fps_transparent-2.png"),
    2: pygame.image.load("gun_shot.png"),
    3: pygame.image.load("green_crosshair_30x30.png"),
    4: pygame.image.load("space.png"),
    5: pygame.image.load("HUD-2.png"),
    6: pygame.image.load(char[random.randint(0,4)])
}
background = pygame.transform.scale(texture[4], (screen_width, screen_height))

game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 4, 0, 0, 5, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 4, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 4, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

def draw_map():
    for col in range(map_cols):
        for row in range(map_rows):
            if game_map[row][col] == 1:
                colour = WHITE
            elif game_map[row][col] == 2: 
                colour = RED
            elif game_map[row][col] == 3:
                colour = BLUE
            elif game_map[row][col] == 4:
                colour = ORANGE
            elif game_map[row][col] == 5:
                colour = GREEN
            else:
                colour = BLACK
            rect = (col * tile_size, row * tile_size, tile_size, tile_size)
            pygame.draw.rect(screen, colour, rect)
            pygame.draw.rect(screen, BLUE, rect, 1)


def draw_line(angle, colour):

    global real_colour
    global tile_number
    global offset

    future_xz = player_x + math.cos(math.radians(angle)) * 2000
    future_yz = player_y + math.sin(math.radians(angle)) * 2000

    tex_x = future_xz - player_x # tex_x/tex_y isn't related to texture
    tex_y = future_yz - player_y

    i = 0
    while i < 1:
        ser_x = int((player_x + (tex_x * i)) / tile_size)
        ser_y = int((player_y + (tex_y * i)) / tile_size)

        
        if game_map[ser_y][ser_x] != 0: # game_map[rows = 6][cols = 8] this is wrong i chnaged it later
            temp_coor = game_map[ser_y][ser_x]
            if temp_coor == 1:
                real_colour = WALL_COLOUR
            elif temp_coor == 2:
                real_colour = RED
            elif temp_coor == 3:
                real_colour = BLUE
            elif temp_coor == 4:
                real_colour = ORANGE
            elif temp_coor == 5:
                real_colour = GREEN


            future_xz = (player_x + (tex_x * i))
            future_yz = (player_y + (tex_y * i))
            break
        i += 0.0002


        
    if debug_mode == 1:
        pygame.draw.line(screen, colour, (player_x, player_y), (future_xz, future_yz))

    x_rey = future_xz - player_x
    x_rey_2 = x_rey**2

    y_rey = future_yz - player_y
    y_rey_2 = y_rey**2

    line_length = math.sqrt((x_rey_2) + (y_rey_2))

    if future_xz % tile_size == 0:
        texture_direction = "vertical"
    else:
        texture_direction = "horizontal"

    if texture_direction == "horizontal":
        offset = int((future_xz % tile_size) * (texture[0].get_width() / tile_size))
    else:
        offset = int((future_yz % tile_size) * (texture[0].get_width() / tile_size))

    
    return line_length
    
def draw_player():
    global future_x, future_y

    # ----- draw direction lines here after school tmrw ------
    future_x = player_x + math.cos(math.radians(player_angle)) * 2000
    future_y = player_y + math.sin(math.radians(player_angle)) * 2000
    if debug_mode == 1:
        pygame.draw.circle(screen, GREEN, (player_x, player_y), 5)
        pygame.draw.line(screen, RED, (player_x, player_y), (future_x, future_y))
    # ----- draw direction lines here after school tmrw ------

def calculate_line_in_game(abc_line):
    return (screen_height/2)+(abc_line/2)

def dead_screen():
    paused = True

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((255, 0, 0))
        screen.blit(death_text, (screen_width // 2, screen_height // 2))
        pygame.display.flip()

def draw_rays():
    global health, player_x, player_y, score, player_angle

    mean = 0
    low = 1000
    high = 0
    for ray in range(rays):
        temp_angle = (player_angle - (fov/2)) + (fov/rays * ray)
        line_length = draw_line(temp_angle, YELLOW) # casts rays and return length of ray

        angle_difference = math.radians(temp_angle - player_angle)
        line_length = line_length * math.cos(angle_difference)

        try:
            line_game_height = skew / line_length
        except ZeroDivisionError:
            player_x = checkpoint_x
            player_y = checkpoint_y
            player_angle = checkpoint_deg
            health -= 20
            if health <= 0:
                dead_screen()
            score -= 12345
            line_game_height = 0
            print(health)

        scaler = int(line_game_height / texture[0].get_height())
        for k in range(tile_size):
            colour = texture[0].get_at((offset, k))
            for i in range(scaler):
                yplus = (k * scaler)
                 #draw_pixel(ray, calculate_line_in_game(-1*line_game_height)+yplus+i)
                #screen.set_at((ray, int(calculate_line_in_game(-1*line_game_height)+yplus+i)), colour)

        mean += line_game_height 
        if line_game_height < low:
            low = line_game_height
        if line_game_height > high:
            high = line_game_height

        if projection_mode == 1: 
            pygame.draw.line(screen, (max(real_colour[0]*0.6, real_colour[0] * (1 - line_length / 500)), max(real_colour[1]*0.6, real_colour[1] * (1 - line_length / 500)), max(real_colour[2]*0.6, real_colour[2] * (1 - line_length / 500))), (ray, calculate_line_in_game(line_game_height)), (ray, calculate_line_in_game(-1*line_game_height)))
            pass

    mean /= rays
    #print(f"MEAN: {mean}, LOW: {low}, HIGH:{high}")

def detect_movement():
    keys = pygame.key.get_pressed()
    
    global checkpoint_x, checkpoint_y, checkpoint_deg
    global score
    global start_time
    global player_x
    global player_y
    global player_angle
    global gun_shoot
    global ammo
    global ammo_text

    if keys[pygame.K_w]:
        new_x = player_x + (future_x - player_x) * movement_speed
        new_y = player_y + (future_y - player_y) * movement_speed
        new_x_map = int(new_x / tile_size)
        new_y_map = int(new_y / tile_size)
        if game_map[new_y_map][new_x_map] != 0:
            pass
        else:
            [player_x, player_y] = [new_x, new_y]
    if keys[pygame.K_a]:
        temp_angle = player_angle
        temp_angle -= 90
        temp_x = player_x + math.cos(math.radians(temp_angle)) * 2000
        temp_y = player_y + math.sin(math.radians(temp_angle)) * 2000
        new_x = player_x + (temp_x - player_x) * movement_speed
        new_y = player_y + (temp_y - player_y) * movement_speed
        new_x_map = int(new_x / tile_size)
        new_y_map = int(new_y / tile_size)
        if game_map[new_y_map][new_x_map] != 0:
            pass
        else:
            [player_x, player_y] = [new_x, new_y]
    if keys[pygame.K_s]:
        new_x = player_x - (future_x - player_x) * movement_speed
        new_y = player_y - (future_y - player_y) * movement_speed
        new_x_map = int(new_x / tile_size)
        new_y_map = int(new_y / tile_size)
        if game_map[new_y_map][new_x_map] != 0:
            pass
        else:
            [player_x, player_y] = [new_x, new_y]
    if keys[pygame.K_d]:
        temp_angle = player_angle
        temp_angle += 90
        temp_x = player_x + math.cos(math.radians(temp_angle)) * 2000
        temp_y = player_y + math.sin(math.radians(temp_angle)) * 2000
        new_x = player_x + (temp_x - player_x) * movement_speed
        new_y = player_y + (temp_y - player_y) * movement_speed
        new_x_map = int(new_x / tile_size)
        new_y_map = int(new_y / tile_size)
        if game_map[new_y_map][new_x_map] != 0:
            pass
        else:
            [player_x, player_y] = [new_x, new_y]
    if keys[pygame.K_SPACE] and ammo > 0:
        gun_shoot = True
        ammo -= 3
        ammo_text = HUD_font.render(str(ammo)+"ml", False, (0,255,255))
    else: 
        gun_shoot = False
    if keys[pygame.K_f]:

        start_time = elapsed_time
        if (player_x > 128 and player_x < 192) and (player_y > 96 and player_y < 224):
            game_map[5][3] = 0
        elif (player_x > 224 and player_x < 288) and (player_y > 32 and player_y < 224):
            game_map[4][9] = 0
            checkpoint_x = 352
            checkpoint_y = 192
            checkpoint_deg = 90
        elif (player_x > 128 and player_x < 224) and (player_y > 416 and player_y < 608):
            game_map[14][7] = 0
        elif (player_x > 256 and player_x < 384) and (player_y > 416 and player_y < 512):
            game_map[16][9] = 0


    if keys[pygame.K_RIGHT]:
        player_angle += rotation_speed
    if keys[pygame.K_LEFT]:
        player_angle -= rotation_speed
    
def moving_wall_1():

    row = 9
    col = (elapsed_time % 11) + 1
    if col == 1:
        game_map[9][11] = 0
    game_map[row][col] = 2
    if game_map[row][col - 1] != 1:
        game_map[row][col - 1] = 0

def moving_wall_2():

    row = 10
    col = (11 - (elapsed_time % 11))
    if col == 11:
        game_map[10][1] = 0
    game_map[row][col] = 3
    #game_map[9][11] = 0
    if game_map[row][col + 1] != 1:
        game_map[row][col + 1] = 0

def restart_wall(start_time):

    if (elapsed_time - start_time) == 15:
        game_map[5][3] = 4
        game_map[4][9] = 4
        game_map[14][7] = 4
        game_map[16][9] = 4

def draw_hud(score):
    global score_text
    global health_text
    global ammo_text

    screen.blit(ammo_text, (334, screen_height - 75))
    health_text = HUD_font.render(str((health/100) *100)+"%", False, (255, 255, 255))
    screen.blit(health_text, (50, screen_height - 75))
    screen.blit(score_text, (195, screen_height - 75))
    score_text = HUD_font.render(score_4_digit(math.floor(score)), False, (170, 255, 0))

    

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    elapsed_time = math.floor((pygame.time.get_ticks() - start_time) / 350)
    score -= 7
    restart_wall(start_time)
    detect_movement()
    screen.fill((0,0,0))
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, (139, 69, 19), (0, screen_height//2, screen_width, screen_height//2))

    if debug_mode == 1:
        draw_map()
    draw_player()
    moving_wall_1()
    moving_wall_2()
    draw_rays()
    if debug_mode != 1:
        screen.blit(texture[3], (screen_width//2 - texture[3].get_width()//2, screen_height//2 - texture[3].get_height()//2))
        if gun_shoot == False:
            screen.blit(texture[1],(screen_width//2 , screen_height - texture[1].get_height()))
        else: 
            screen.blit(texture[2],(screen_width//2 , screen_height - texture[2].get_height()))
        screen.blit(texture[5], (-30,screen_height - 270))
        draw_hud(score)
        screen.blit(texture[6], (449, screen_height - texture[6].get_height() - 30)) #draws ijaz
        if ammo == 0:
            screen.blit(no_ammo_text, (screen_width - no_ammo_text.get_width() - 10, 0))

    pygame.draw.rect(screen, (255, 0, 0), (300, 300, 300, 300), 1 )
    pygame.display.flip()   
    clock.tick(60)
    print(f"FPS: {clock.get_fps():.2f}")
pygame.quit()
print("Running = False, Game exit")

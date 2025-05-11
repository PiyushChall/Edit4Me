
import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Projectile Dodging Game")

# Player settings
player_size = 40
player_x = screen_width // 2 - player_size // 2
player_y = screen_height - player_size - 10
player_speed = 5
player_tail = []
tail_length = 10

# Projectile settings
projectile_size = 20
projectile_speed = 3
projectiles = []
projectile_tails = []
following_projectiles = [] # list to store following projectiles

# Score
score = 0
font = pygame.font.Font(None, 36)
last_score_update = pygame.time.get_ticks()

# Game loop
running = True
clock = pygame.time.Clock()

def game_over():
    game_over_text = font.render("Game Over! Score: " + str(score), True, (255, 0, 0))
    text_rect = game_over_text.get_rect(center=(screen_width/2, screen_height/2))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    quit()


def create_projectile():
    side = random.randint(0, 3)
    x, y, angle = 0, 0, 0
    if side == 0:
        x = random.randint(0, screen_width - projectile_size)
        y = 0
        angle = math.pi / 2
    elif side == 1:
        x = screen_width
        y = random.randint(0, screen_height - projectile_size)
        angle = math.pi
    elif side == 2:
        x = random.randint(0, screen_width - projectile_size)
        y = screen_height
        angle = 3 * math.pi / 2
    else:
        x = 0
        y = random.randint(0, screen_height - projectile_size)
        angle = 0

    projectiles.append([x, y, angle, projectile_speed])
    projectile_tails.append([])

def create_following_projectile():
    x = random.randint(0, screen_width - projectile_size)
    y = random.randint(0, screen_height - projectile_size)
    following_projectiles.append([x, y, pygame.time.get_ticks()]) #Store creation time


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_size:
        player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_size:
        player_y += player_speed

    # Player tail
    player_tail.append((player_x + player_size // 2, player_y + player_size // 2))
    if len(player_tail) > tail_length:
        player_tail.pop(0)

    # Score update
    current_time = pygame.time.get_ticks()
    if current_time - last_score_update >= 1000:
        score += 1
        last_score_update = current_time

    # Projectile movement and collision detection
    if random.randint(1, 60) == 1: #Reduce frequency of regular projectiles
        create_projectile()
    if random.randint(1, 200) == 1: #Lower frequency for following projectiles
        create_following_projectile()

    for i, projectile in enumerate(projectiles[:]):
        projectile[0] += projectile[3] * math.cos(projectile[2])
        projectile[1] += projectile[3] * math.sin(projectile[2])
        projectile_tails[i].append((projectile[0] + projectile_size // 2, projectile[1] + projectile_size // 2))
        if len(projectile_tails[i]) > tail_length:
            projectile_tails[i].pop(0)

        #Collision Detection
        if (
            player_x < projectile[0] + projectile_size
            and player_x + player_size > projectile[0]
            and player_y < projectile[1] + projectile_size
            and player_y + player_size > projectile[1]
        ):
            game_over()

        #Remove off-screen projectiles
        if (
            projectile[0] < -projectile_size
            or projectile[0] > screen_width + projectile_size
            or projectile[1] < -projectile_size
            or projectile[1] > screen_height + projectile_size
        ):
            projectiles.pop(i)
            projectile_tails.pop(i)
            break

    #Following projectile logic
    for i, follow_proj in enumerate(following_projectiles[:]):
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - follow_proj[2]

        if time_elapsed < 3000: # 3 seconds = 3000 milliseconds
            #Simple following behavior - moves towards player center
            dx = (player_x + player_size//2) - follow_proj[0]
            dy = (player_y + player_size//2) - follow_proj[1]
            distance = math.hypot(dx, dy)
            if distance > 0: #Avoid division by zero
                follow_proj[0] += (dx / distance) * projectile_speed
                follow_proj[1] += (dy / distance) * projectile_speed


            #Collision Detection
            if (
                player_x < follow_proj[0] + projectile_size
                and player_x + player_size > follow_proj[0]
                and player_y < follow_proj[1] + projectile_size
                and player_y + player_size > follow_proj[1]
            ):
                game_over()


        else:
            following_projectiles.pop(i)



    # Drawing
    screen.fill((0, 0, 0))

    #Draw Player Tail
    for i in range(len(player_tail)):
        pygame.draw.circle(screen,(0,255,0),player_tail[i],2)


    pygame.draw.rect(
        screen, (0, 255, 0), (player_x, player_y, player_size, player_size)
    )
    for i, projectile in enumerate(projectiles):
        #Draw Projectile Tail
        for j in range(len(projectile_tails[i])):
            pygame.draw.circle(screen,(255,0,0),projectile_tails[i][j],2)
        pygame.draw.circle(
            screen,
            (255, 0, 0),
            (projectile[0] + projectile_size // 2, projectile[1] + projectile_size // 2),
            projectile_size // 2,
        )

    # Draw Following Projectiles
    for follow_proj in following_projectiles:
        pygame.draw.circle(screen, (255, 255, 0), (follow_proj[0] + projectile_size // 2, follow_proj[1] + projectile_size // 2), projectile_size // 2)

    #Display Score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text,(10,10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

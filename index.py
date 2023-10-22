import pygame
from sys import exit
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_Y = 300

def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
  score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, 50))
  screen.blit(score_surf, score_rect)
  return current_time

def obstacle_movement(obstacle_list):
  if obstacle_list:
    for obstacle_rect in obstacle_list:
      obstacle_rect.x -= 5

      if obstacle_rect.bottom == GROUND_Y: screen.blit(snail_surf, obstacle_rect)
      else: screen.blit(fly_surf, obstacle_rect)

    
    obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
    
    return obstacle_list
  else: return []

def check_collisions(player, obstacles):
  if obstacles:
    for obstacle_rect in obstacles:
      if player.colliderect(obstacle_rect):
        return False
  return True

def player_animation():
  global player_surf, player_index

  if player_rect.bottom < GROUND_Y:
    player_surf = player_jump
  else:
    player_index += 0.1
    if player_index >= len(player_walk): player_index = 0
    player_surf = player_walk[int(player_index)]
    # walk
  # play walking animation if player is on floor
  # display jump surface when player is not on floor

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

game_active = False
start_time = 0
score = 0

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

# snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# fly 
fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(bottomright=(80, GROUND_Y))
player_gravity = 0

# intro screen
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
# player_stand = pygame.transform.scale(player_stand, (200, 400))
# player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

game_name = test_font.render("The jump game", False, (111, 196, 169))
game_name_rect = game_name.get_rect(midtop = (SCREEN_WIDTH / 2, 50))

game_message = test_font.render("Press space bar to run", True, (111, 196, 169))
game_message_rect = game_message.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()

    if game_active:
      if event.type == pygame.MOUSEBUTTONDOWN:
        if player_rect.collidepoint(event.pos) and player_rect.bottom >= GROUND_Y:
          player_gravity = -20

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE and player_rect.bottom >= GROUND_Y:
          player_gravity = -20
          
      if event.type == obstacle_timer:
        if randint(0, 2):
          obstacle_rect_list.append(snail_surf.get_rect(midbottom=(randint(900, 1100), GROUND_Y)))
        else:
          obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900, 1100), 210)))

      if event.type == snail_animation_timer:
        if snail_frame_index == 0: snail_frame_index = 1
        else: snail_frame_index = 0
        snail_surf = snail_frames[snail_frame_index]
      
      if event.type == fly_animation_timer:
        if fly_frame_index == 0: fly_frame_index = 1
        else: fly_frame_index = 0
        fly_surf = fly_frames[fly_frame_index]
    
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        # snail_rect.left = SCREEN_WIDTH
        start_time = int(pygame.time.get_ticks() / 1000)

  if game_active:
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, GROUND_Y))
    score = display_score()

    # # snail movement
    # snail_rect.x -= 4
    # if snail_rect.right <= -50: snail_rect.left = SCREEN_WIDTH
    # screen.blit(snail_surf, snail_rect)
    
    # player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= GROUND_Y: player_rect.bottom = GROUND_Y
    player_animation()
    screen.blit(player_surf, player_rect)

    # obstacle movement
    obstacle_rect_list = obstacle_movement(obstacle_rect_list)

    # collision
    game_active = check_collisions(player_rect, obstacle_rect_list)

  else:
    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)
    obstacle_rect_list.clear()
    player_rect.midbottom = (80, GROUND_Y)
    player_gravity = 0

    score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
    score_message_rect = score_message.get_rect(midbottom= (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
    screen.blit(game_name, game_name_rect)

    if score == 0: screen.blit(game_message, game_message_rect)
    else: screen.blit(score_message, score_message_rect)

  pygame.display.update()
  clock.tick(60)
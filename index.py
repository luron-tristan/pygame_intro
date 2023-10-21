import pygame
from sys import exit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_Y = 300

def display_score():
  current_time = int(pygame.time.get_ticks() / 1000) - start_time
  score_surf = test_font.render(f"Score: {current_time}", False, (64, 64, 64))
  score_rect = score_surf.get_rect(center = (SCREEN_WIDTH / 2, 50))
  screen.blit(score_surf, score_rect)
  return current_time

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

game_active = True
start_time = 0
score = 0

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(600, GROUND_Y))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
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
    
    else:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True
        snail_rect.left = SCREEN_WIDTH
        start_time = int(pygame.time.get_ticks() / 1000)

  if game_active:
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, GROUND_Y))
    score = display_score()

    snail_rect.x -= 4
    if snail_rect.right <= -50: snail_rect.left = SCREEN_WIDTH
    screen.blit(snail_surf, snail_rect)
    
    # player
    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= GROUND_Y: player_rect.bottom = GROUND_Y
    screen.blit(player_surf, player_rect)

    # collision
    if snail_rect.colliderect(player_rect):
      game_active = False

  else:

    screen.fill((94, 129, 162))
    screen.blit(player_stand, player_stand_rect)

    score_message = test_font.render(f"Your score: {score}", False, (111, 196, 169))
    score_message_rect = score_message.get_rect(midbottom= (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50))
    screen.blit(game_name, game_name_rect)

    if score == 0: screen.blit(game_message, game_message_rect)
    else: screen.blit(score_message, score_message_rect)

  pygame.display.update()
  clock.tick(60)
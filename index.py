import pygame
from sys import exit

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

score_surf = test_font.render("My game", False, "Black")
score_rect = score_surf.get_rect(center=(SCREEN_WIDTH / 2, 50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(600, 300))

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(bottomright=(80, 300))

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    # if event.type == pygame.MOUSEMOTION and player_rect.collidepoint(event.pos):
    #   print("Collision")
      
  screen.blit(sky_surf, (0, 0))
  screen.blit(ground_surf, (0, 300))
  pygame.draw.rect(screen, "Pink", score_rect)
  pygame.draw.rect(screen, "Pink", score_rect, 6)
  # pygame.draw.line(screen, "Gold", (0, 0), (pygame.mouse.get_pos()), 10)
  # pygame.draw.line(screen, "Gold", (0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), 10)
  # pygame.draw.ellipse(screen, "Brown", pygame.Rect(50, 200, 100, 100))
  screen.blit(score_surf, score_rect)

  snail_rect.x -= 4
  if snail_rect.right <= -50: snail_rect.left = SCREEN_WIDTH
  screen.blit(snail_surf, snail_rect)
  screen.blit(player_surf, player_rect)

  # if player_rect.colliderect(snail_rect):
  #   print('collision')

  # mouse_pos = pygame.mouse.get_pos()
  # if player_rect.collidepoint(mouse_pos):
  #   print(pygame.mouse.get_pressed())

  


  pygame.display.update()
  clock.tick(60)
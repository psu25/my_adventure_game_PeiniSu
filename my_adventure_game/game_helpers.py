import pygame
import random
import game_config as config

def draw_room(screen, row, col):
    w = config.WIDTH // config.GRID_COLS
    h = config.HEIGHT // config.GRID_ROWS
    x, y = col * w, row * h
    pygame.draw.rect(screen, (70, 90, 120), pygame.Rect(x, y, w, h), 2)

def draw_player(screen, x, y, r):
    pygame.draw.circle(screen, (240, 240, 255), (int(x), int(y)), r)

def draw_enemy(screen, e):
    pygame.draw.circle(screen, (255, 100, 80), (int(e["x"]), int(e["y"])), e["r"])

def is_blocked(x, y):
    return False

def show_game_over(screen):
    font = pygame.font.Font(None, 72)
    txt = font.render("GAME OVER", True, (255, 0, 0))
    rect = txt.get_rect(center=(config.WIDTH//2, config.HEIGHT//2))
    screen.blit(txt, rect)
    pygame.display.flip()
    pygame.time.wait(1200)

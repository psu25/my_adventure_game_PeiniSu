import pygame
import random
import math
import game_config as config
from game_helpers import (
    draw_room, draw_player, draw_enemy, is_blocked, show_game_over
)

def move_enemies(enemies, target_pos, dt, speed):
    for e in enemies:
        dx, dy = target_pos[0] - e["x"], target_pos[1] - e["y"]
        dist = math.hypot(dx, dy) or 1
        e["x"] += dx / dist * speed * dt
        e["y"] += dy / dist * speed * dt

def check_collisions(enemies, player_pos, player_r):
    px, py = player_pos
    for e in enemies:
        if math.hypot(px - e["x"], py - e["y"]) <= player_r + e["r"]:
            return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("Adventure Grid Game")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 28)
    hit_sound = pygame.mixer.Sound(buffer=b"\x00"*256)

    player = {"x": config.WIDTH/2, "y": config.HEIGHT/2, "r": 14}
    enemies = []
    state = {"running": True, "score": 0, "lives": 3}

    while state["running"]:
        dt = clock.tick(config.FPS) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                state["running"] = False

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        player["x"] += dx * config.PLAYER_SPEED * dt
        player["y"] += dy * config.PLAYER_SPEED * dt
        player["x"] = max(10, min(config.WIDTH - 10, player["x"]))
        player["y"] = max(10, min(config.HEIGHT - 10, player["y"]))

        if len(enemies) < 5 and random.random() < 0.02:
            enemies.append({"x": random.randint(50, 750), "y": random.randint(50, 550), "r": 12})

        move_enemies(enemies, (player["x"], player["y"]), dt, config.ENEMY_SPEED)

        if check_collisions(enemies, (player["x"], player["y"]), player["r"]):
            hit_sound.play()
            state["lives"] -= 1
            enemies.clear()
            if state["lives"] <= 0:
                show_game_over(screen)
                state["running"] = False

        state["score"] += 1

        screen.fill(config.BG_COLOR)
        for row in range(config.GRID_ROWS):
            for col in range(config.GRID_COLS):
                draw_room(screen, row, col)
        for e in enemies:
            draw_enemy(screen, e)
        draw_player(screen, player["x"], player["y"], player["r"])

        fps = clock.get_fps()
        info = font.render(f"Score: {state['score']}  Lives: {state['lives']}  FPS:{int(fps)}", True, (255,255,255))
        screen.blit(info, (10, 10))

        mx, my = pygame.mouse.get_pos()
        pygame.draw.rect(screen, (240,240,240), pygame.Rect(mx-5, my-5, 10, 10), 1)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

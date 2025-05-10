from random import randint
import pygame

from src.constants import (
    MAX_FPS,
    DISPLAY_SIZE,
    SHOOT_EVENT,
    SPAWN_EVENT,
    HEALTH_BAR_WIDTH,
    PLAYER_HEALTH,
    PLAYER_SPEED,
    ENEMY_DAMAGE,
    ENEMY_SPEED,
    BULLET_SPPED,
)
from src.player import Player
from src.bullet import Bullet
from src.enemy import Enemy
from src.utils import laod_image, get_path


def game(display, clock):
    asteroid_image = laod_image("assets", "images", "asteroid.png", size=[164, 164])
    background_image = laod_image(
        "assets", "images", "background.png", size=DISPLAY_SIZE
    )
    player_image = laod_image("assets", "images", "player.png", size=[96, 96])
    shot_image = laod_image("assets", "images", "shot.png", size=[64, 64])

    coords = DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] - 50
    player = Player(player_image, coords, PLAYER_SPEED, PLAYER_HEALTH)

    bullets = list()
    enemies = list()

    difficulty = 0
    pygame.time.set_timer(SPAWN_EVENT, 2000, 1)

    while player.health > 0:
        difficulty += clock.get_time()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            elif event.type == SHOOT_EVENT:
                b = Bullet(shot_image, player.rect.midtop, BULLET_SPPED)
                bullets.append(b)

            elif event.type == SPAWN_EVENT:
                millis = max(750, round(2000 - difficulty / 70))
                pygame.time.set_timer(SPAWN_EVENT, millis, 1)

                e = Enemy(
                    round(ENEMY_DAMAGE + difficulty / 7_000),
                    asteroid_image,
                    [randint(50, DISPLAY_SIZE[0] - 50), -asteroid_image.height],
                    ENEMY_SPEED + difficulty / 35_000,
                )
                enemies.append(e)

        # Обновление игровых объектов
        player.update()

        for i in bullets.copy():
            i.update()
            if not i.alive:
                bullets.remove(i)

        for i in enemies.copy():
            i.update()
            if not i.alive:
                enemies.remove(i)

        for b in bullets:
            for e in enemies:
                if b.collide_entity(e):
                    b.kill()
                    e.kill()

        for e in enemies:
            if e.collide_entity(player):
                player.get_damage(e.damage)
                e.kill()

        # Обновление экрана
        display.fill("black")
        display.blit(background_image, (0, 0))

        player.render(display)
        for u in bullets:
            u.render(display)
        for u in enemies:
            u.render(display)

        #                             цвет      x   y        ширина      высота
        pygame.draw.rect(display, (100, 0, 0), [10, 10, HEALTH_BAR_WIDTH, 20])
        width = int(player.health / PLAYER_HEALTH * HEALTH_BAR_WIDTH)
        pygame.draw.rect(display, (255, 0, 0), [10, 10, width, 20])
        pygame.draw.rect(display, (175, 0, 0), [8, 8, HEALTH_BAR_WIDTH + 4, 24], 2)

        pygame.display.update()
        clock.tick(MAX_FPS)


def show_lose(display, clock):
    running = True

    font = pygame.Font(get_path("assets", "fonts", "pixel.ttf"), 64)
    text = font.render("YOU LOSE!", True, (255, 50, 50))
    display.blit(text, text.get_rect(center=[DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] / 2]))
    pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                running = False

        clock.tick(MAX_FPS)


def main():
    pygame.init()

    display = pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE | pygame.SCALED)
    pygame.display.set_caption("Shooter")
    clock = pygame.time.Clock()

    while True:
        game(display, clock)
        show_lose(display, clock)


if __name__ == "__main__":
    main()

import pygame

from src.constants import MAX_FPS, DISPLAY_SIZE, SHOOT_EVENT
from src.player import Player


def game(display, clock):
    coords = DISPLAY_SIZE[0] / 2, DISPLAY_SIZE[1] - 50
    image = pygame.Surface([50, 50])
    image.fill( (255, 0, 0) )
    player = Player(image, coords, 5.5, 100)

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == SHOOT_EVENT:
                print(1)

        # Обновление игровых объектов
        player.update()

        # Обновление экрана
        display.fill((0, 0, 0))

        player.render(display)

        pygame.display.update()
        clock.tick(MAX_FPS)


def main():
    pygame.init()

    display = pygame.display.set_mode(DISPLAY_SIZE, pygame.RESIZABLE | pygame.SCALED)
    pygame.display.set_caption("Shooter")
    clock = pygame.time.Clock()

    while True:
        game(display, clock)


if __name__ == "__main__":
    main()

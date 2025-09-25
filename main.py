import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.font.init()
    score_font = pygame.font.SysFont("monospace", 28)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game_score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()

    Player.containers = (updatable, drawable)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        # Check for collisions between shots and asteroids
        # This is the corrected section. We need a nested loop.
        for shot in shots:
            for asteroid in asteroids:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
                    game_score += ASTEROID_SCORE_VALUE
                    # Once a shot hits an asteroid, we can break from the inner loop
                    # to avoid checking for more collisions with the same shot.
                    break 
        
        # Check for collisions between player and asteroids
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                # want to insert pop-up game over message here
                sys.exit()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
            
            
        score_text = score_font.render(f"Score: {game_score}", True, "white")
        score_rect = score_text.get_rect()
        score_rect.topleft = (9, 10) # 10 pixels from top, 10 from left
        screen.blit(score_text, score_rect)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000
        


if __name__ == "__main__":
    main()

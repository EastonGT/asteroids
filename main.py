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
    game_state = "playing"

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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and game_state == "game_over":
                    pygame.quit()
                    return
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_state == "game_over":
                    #reset_game()
                    # This is the current work in progress
                    # Reset function not started

        if game_state == "playing":
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_state = "game_over"
                

                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()
                        game_score += ASTEROID_SCORE_VALUE

            screen.fill("black")

            for obj in drawable:
                obj.draw(screen)
            
            
            score_text = score_font.render(f"Score: {game_score}", True, "white")
            score_rect = score_text.get_rect()
            score_rect.topleft = (9, 10) # 10 pixels from top, 10 from left
            screen.blit(score_text, score_rect)

        elif game_state == "game_over":
            
            screen.fill("black")

            # Render and display "Game Over!" message
            game_over_font = pygame.font.SysFont("monospace", 72) # Larger font for Game Over
            game_over_text = game_over_font.render("GAME OVER!", True, "red")
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50)) # Center it
            screen.blit(game_over_text, game_over_rect)

            # Display final score
            final_score_text = score_font.render(f"Final Score: {game_score}", True, "white")
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
            screen.blit(final_score_text, final_score_rect)

            # Instructions to player on game_over screen
            instructions_font = pygame.font.SysFont("monospace", 20)
            instructions_text = instructions_font.render("Press R to Restart or Q to Quit", True, "gray")
            instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 80))
            screen.blit(instructions_text, instructions_rect)      

        pygame.display.flip()
        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()

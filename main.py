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
    
    # Initialize fonts for score and game over message
    score_font = pygame.font.SysFont("monospace", 28)
    game_over_font = pygame.font.SysFont("monospace", 72, bold=True)
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Define groups outside the inner game loop, so they persist across resets
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Assign containers once (since they are class variables)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)
    
    # Function to set up or reset the game state
    def reset_game():
        # Clear all sprites from the groups
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        
        # Re-create persistent game objects
        asteroid_field = AsteroidField()
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        return 0, True, player # Return new score, active state, and player object

    game_score, game_active, player = reset_game()

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            # Allow the game to restart on 'R' key press if game is over
            if not game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    game_score, game_active, player = reset_game()

        if game_active:
            # --- UPDATE GAME LOGIC (ONLY RUNS WHEN ACTIVE) ---
            updatable.update(dt)

            # Check for collisions between shots and asteroids
            for shot in shots:
                for asteroid in asteroids:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        asteroid.split()
                        game_score += ASTEROID_SCORE_VALUE
                        break 
            
            # Check for collisions between player and asteroids
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_active = False # Set the flag to False to end the game loop
                    player.kill() 
                    # We do NOT return here, so the drawing phase can run

        # --- DRAWING PHASE (ALWAYS RUNS) ---
        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
            
        # Draw the score
        score_text = score_font.render(f"Score: {game_score}", True, "white")
        score_rect = score_text.get_rect()
        score_rect.topleft = (9, 10) 
        screen.blit(score_text, score_rect)

        # --- GAME OVER SCREEN LOGIC ---
        if not game_active:
            # Render the "Game Over" message
            game_over_text = game_over_font.render("GAME OVER", True, "red")
            
            # Center the text on the screen
            text_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            )
            screen.blit(game_over_text, text_rect)
            
            # Add a message to prompt the user to restart
            prompt_text = score_font.render("Press 'R' to Restart or close window to exit", True, "white")
            prompt_rect = prompt_text.get_rect(
                center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            )
            screen.blit(prompt_text, prompt_rect)


        pygame.display.flip()

        # limit the framerate
        dt = clock.tick(60) / 1000
        


if __name__ == "__main__":
    main()

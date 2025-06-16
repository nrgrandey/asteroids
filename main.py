import sys
import pygame
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

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

    score = 0
    lives = PLAYER_LIVES
    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot) and not asteroid.is_explosion_piece:
                    asteroid.split()
                    shot.kill()
                    score += ASTEROID_VALUE
                    break
            if player.collides_with(asteroid) and not asteroid.is_explosion_piece:
                lives -= 1
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.velocity = pygame.Vector2(0, 0)
                # Display GAME OVER screen when lives reach 0
                if lives <= 0:
                    # Display GAME OVER screen
                    game_over_surface = font.render("GAME OVER", True, (255, 0, 0))
                    restart_surface = font.render("Press ENTER to Restart or Q to Quit", True, (255, 255, 255))
                    screen.blit(game_over_surface, (SCREEN_WIDTH // 2 - game_over_surface.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
                    screen.blit(restart_surface, (SCREEN_WIDTH // 2 - restart_surface.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
                    pygame.display.flip()
                    waiting = True
                    while waiting:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                                    # Restart the game
                                    main()
                                    return
                                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                                    pygame.quit()
                                    sys.exit()
                        clock.tick(15)


        screen.fill("black")

        # Render the score
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))  # Draw at top-left corner
        # Render the lives
        lives_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_surface, (10, 40))

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()

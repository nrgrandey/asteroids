import pygame
import random
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x, y, radius, is_explosion_piece=False, lifetime=None):
        super().__init__(x, y, radius)
        self.is_explosion_piece = is_explosion_piece
        self.lifetime = lifetime
    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

        # Wrapping logic
        if self.position.x < 0:
            self.position.x += SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x -= SCREEN_WIDTH

        if self.position.y < 0:
            self.position.y += SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y -= SCREEN_HEIGHT


        # Explosion logic
        if self.is_explosion_piece:
            self.lifetime -= dt
            if self.lifetime <= 0:
                self.kill()

    def split(self):
        for i in range(0, 8):
            vector = self.velocity.rotate(i * 45)
            new_asteroid = Asteroid(
                self.position.x,
                self.position.y,
                self.radius / 5,
                is_explosion_piece=True,
                lifetime=0.4 # seconds
            )
            new_asteroid.velocity = vector
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        # Create two smaller asteroids
        random_angle = random.uniform(20, 50)
        vector_1 = self.velocity.rotate(random_angle)
        vector_2 = self.velocity.rotate(-random_angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vector_1
        asteroid2.velocity = vector_2

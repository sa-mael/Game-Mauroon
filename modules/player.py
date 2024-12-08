# player.py

import pygame

class Player:
    def __init__(self, x, y, layer):
        self.x = x
        self.y = y
        self.layer = layer
        self.speed = 250

    def move(self, keys, dt, world):
        # Handle movement using arrow keys or WASD
        if keys[pygame.K_a]:  # Move left
            self.x -= self.speed * dt
        if keys[pygame.K_d]:  # Move right
            self.x += self.speed * dt
        if keys[pygame.K_w]:  # Move up
            self.y -= self.speed * dt
        if keys[pygame.K_s]:  # Move down
            self.y += self.speed * dt

    def update_animation(self):
        pass

    def draw(self, surface, textures):
        # Draw the player at the correct position
        surface.blit(textures["player"], (self.x, self.y))

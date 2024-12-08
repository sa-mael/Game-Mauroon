# animated_sprite.py

import pygame

class AnimatedSprite:
    def __init__(self, sprite_sheet_path, frame_width, frame_height, scale_size, num_frames, frame_delay):
        self.sprite_sheet = pygame.image.load(sprite_sheet_path)
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scale_size = scale_size
        self.num_frames = num_frames
        self.frame_delay = frame_delay
        self.current_frame = 0
        self.elapsed_time = 0

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.elapsed_time = 0

    def draw(self, surface, x, y):
        frame_rect = pygame.Rect(self.current_frame * self.frame_width, 0, self.frame_width, self.frame_height)
        frame_image = self.sprite_sheet.subsurface(frame_rect)
        surface.blit(pygame.transform.scale(frame_image, (self.frame_width * self.scale_size, self.frame_height * self.scale_size)), (x, y))

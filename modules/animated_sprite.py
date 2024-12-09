import pygame
import sys

class AnimatedSprite:
    def __init__(self, image_path, frame_width, frame_height, num_frames, frame_delay):
        # Load sprite sheet
        try:
            self.sheet = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading animated sprite '{image_path}': {e}")
            sys.exit()

        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.frame_delay = frame_delay

        self.frames = []
        self.current_frame = 0
        self.elapsed_time = 0

        # Extract frames
        for i in range(self.num_frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            try:
                frame = self.sheet.subsurface(rect)
            except ValueError:
                print(f"Error: Frame {i} is outside the sprite sheet bounds.")
                sys.exit()
            self.frames.append(frame)

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.elapsed_time = 1
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, surface, x, y):
        surface.blit(self.frames[self.current_frame], (x, y))

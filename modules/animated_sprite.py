# modules/animated_sprite.py

import pygame
import sys

class AnimatedSprite:
    """
    Handles loading a sprite sheet and animating it frame-by-frame.
    """
    def __init__(self, image_path, frame_width, frame_height, num_frames, frame_delay):
        """
        :param image_path: Path to the sprite sheet image.
        :param frame_width: Width of each frame in the sprite sheet.
        :param frame_height: Height of each frame in the sprite sheet.
        :param num_frames: Total number of frames horizontally in the sheet.
        :param frame_delay: How many seconds each frame is displayed.
        """
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
        self.elapsed_time = 0.0

        # Extract each frame from the sprite sheet
        for i in range(self.num_frames):
            # Each frame is to the right of the previous one
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            try:
                frame_surface = self.sheet.subsurface(rect)
            except ValueError:
                print(f"Error: Frame {i} is outside the sprite sheet bounds.")
                sys.exit()

            self.frames.append(frame_surface)

    def update(self, dt):
        """
        Update the current frame based on the elapsed time (dt).
        """
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.elapsed_time = 0.0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, surface, x, y):
        """
        Draw the current frame at the specified (x, y) position on the surface.
        """
        frame_to_draw = self.frames[self.current_frame]
        surface.blit(frame_to_draw, (x, y))

# modules/animated_sprite.py

import pygame
import sys
from modules.resource_loader import load_image
from modules.logger import setup_logger

logger = setup_logger()

class AnimatedSprite:
    def __init__(self, image_path, num_frames=5, frame_delay=0.1, scale=(40, 40)):
        """
        Initializes an animated sprite.

        :param image_path: Path to the sprite sheet image.
        :param num_frames: Number of frames in the animation.
        :param frame_delay: Delay between frames (seconds).
        :param scale: Tuple (width, height) to scale the frames.
        """
        self.sheet = load_image(image_path, scale=None)
        self.num_frames = num_frames
        self.frame_delay = frame_delay
        self.frames = []
        self.current_frame = 0
        self.elapsed_time = 0

        # Extract frames from the sprite sheet
        sheet_width, sheet_height = self.sheet.get_size()
        frame_width = sheet_width // num_frames
        frame_height = sheet_height

        for i in range(self.num_frames):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = self.sheet.subsurface(rect)
            frame = pygame.transform.scale(frame, scale)
            self.frames.append(frame)

    def update(self, dt):
        """
        Updates the current frame based on elapsed time.

        :param dt: Time since last update (seconds).
        """
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, surface, x, y):
        """
        Draws the current frame at the specified position.

        :param surface: Pygame surface to draw on.
        :param x: X-coordinate.
        :param y: Y-coordinate.
        """
        try:
            surface.blit(self.frames[self.current_frame], (x, y))
        except IndexError:
            logger.error("AnimatedSprite: Frame index out of range.")

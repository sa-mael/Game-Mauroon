# modules/animated_sprite.py

import pygame
import sys
from config import FRAME_WIDTH, FRAME_HEIGHT, SCALE_SIZE, NUM_FRAMES, FRAME_DELAY

class AnimatedSprite:
    def __init__(self, image_path, num_frames=NUM_FRAMES, frame_delay=FRAME_DELAY):
        """
        Loads a sprite sheet and splits it into animation frames.

        :param image_path: Path to the sprite sheet image.
        :param num_frames: Number of frames in the animation.
        :param frame_delay: Delay between frames (seconds).
        """
        try:
            self.sheet = pygame.image.load(image_path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading animated sprite '{image_path}': {e}")
            sys.exit()

        self.num_frames = num_frames
        self.frame_delay = frame_delay
        self.frames = []
        self.current_frame = 0
        self.elapsed_time = 0

        # Extract frames from the sprite sheet
        for i in range(self.num_frames):
            rect = pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)
            try:
                frame = self.sheet.subsurface(rect)
            except ValueError:
                print(f"Error: Frame {i} is outside the sprite sheet bounds.")
                sys.exit()
            scaled_frame = pygame.transform.scale(
                frame,
                (int(FRAME_WIDTH * SCALE_SIZE), int(FRAME_HEIGHT * SCALE_SIZE))
            )
            self.frames.append(scaled_frame)

    def update(self, dt):
        """
        Updates the current animation frame based on elapsed time.

        :param dt: Time since the last update (seconds).
        """
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, surface, x, y):
        """
        Draws the current animation frame at the specified coordinates.

        :param surface: Pygame surface to draw on.
        :param x: X-coordinate.
        :param y: Y-coordinate.
        """
        surface.blit(self.frames[self.current_frame], (x, y))

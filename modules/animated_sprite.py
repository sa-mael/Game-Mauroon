# modules/animated_sprite.py
import pygame
import sys

class AnimatedSprite:
    def __init__(self, image_path, frame_width, frame_height, num_frames, frame_delay):
        """
        Loads an animated sprite from a sprite sheet and
        allows frame-by-frame animation.
        
        :param image_path: Path to the sprite sheet.
        :param frame_width: Width of each frame in the sheet.
        :param frame_height: Height of each frame in the sheet.
        :param num_frames: Number of frames horizontally.
        :param frame_delay: Seconds between frames.
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

        # Extract frames
        for i in range(self.num_frames):
            rect = pygame.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            try:
                frame_img = self.sheet.subsurface(rect)
            except ValueError:
                print(f"Error: Frame {i} is outside the sprite sheet bounds.")
                sys.exit()
            self.frames.append(frame_img)

    def update(self, dt):
        """
        Update the sprite's current frame based on elapsed time (dt).
        """
        self.elapsed_time += dt
        if self.elapsed_time >= self.frame_delay:
            self.elapsed_time = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames

    def draw(self, surface, x, y):
        """
        Draw the current frame at (x, y).
        """
        surface.blit(self.frames[self.current_frame], (x, y))

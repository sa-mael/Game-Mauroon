# modules/resource_loader.py

import pygame
import sys
import os
from modules.logger import setup_logger

logger = setup_logger()

def load_image(path, scale=None, fallback_color=(255, 0, 255)):
    """
    Loads an image from the specified path. If the image is missing, returns a placeholder surface.
    
    :param path: Path to the image file.
    :param scale: Tuple (width, height) to scale the image.
    :param fallback_color: Color of the placeholder if image is missing.
    :return: Loaded and scaled pygame.Surface object.
    """
    if not os.path.exists(path):
        logger.error(f"Missing image file: {path}")
        # Create a placeholder surface
        placeholder = pygame.Surface((50, 50))
        placeholder.fill(fallback_color)
        if scale:
            placeholder = pygame.transform.scale(placeholder, scale)
        return placeholder, f"Missing image: {path}"
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image, None
    except pygame.error as e:
        logger.error(f"Error loading image '{path}': {e}")
        # Create a placeholder surface in case of loading error
        placeholder = pygame.Surface((50, 50))
        placeholder.fill(fallback_color)
        if scale:
            placeholder = pygame.transform.scale(placeholder, scale)
        return placeholder, f"Error loading image: {path}"

def load_sound(path):
    """
    Loads a sound from the specified path. If the sound is missing, returns None.
    
    :param path: Path to the sound file.
    :return: Loaded pygame.mixer.Sound object or None.
    """
    if not os.path.exists(path):
        logger.error(f"Missing sound file: {path}")
        return None
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except pygame.error as e:
        logger.error(f"Error loading sound '{path}': {e}")
        return None

def load_font(path, size):
    """
    Loads a font from the specified path. If the font is missing, returns the default font.
    
    :param path: Path to the font file.
    :param size: Font size.
    :return: Loaded pygame.font.Font object.
    """
    if not os.path.exists(path):
        logger.error(f"Missing font file: {path}. Using default font.")
        return pygame.font.SysFont(None, size)
    try:
        font = pygame.font.Font(path, size)
        return font
    except pygame.error as e:
        logger.error(f"Error loading font '{path}': {e}. Using default font.")
        return pygame.font.SysFont(None, size)

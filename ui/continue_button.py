# ui/continue_button.py

import pygame

class ContinueButton:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.font = pygame.font.SysFont(None, 40)
        self.bg_color = (128, 128, 128)  # Gray background
        self.text_color = (255, 255, 255)

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            # Button was clicked
            self.callback()

    def draw(self, surface):
        # Draw button rectangle
        pygame.draw.rect(surface, self.bg_color, self.rect)
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

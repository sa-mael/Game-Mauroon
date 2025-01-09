# ui/settings_button.py

import pygame

class SettingsButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, 40)
        self.bg_color = (128, 128, 128)  # Gray background
        self.text_color = (255, 255, 255)

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            # Placeholder for actual logic
            print("Settings Button Clicked! (Open Settings Screen)")

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

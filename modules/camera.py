# modules/camera.py
from modules.config import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0

        # Define camera "dead zone" or frame
        self.frame_width = SCREEN_WIDTH // 2
        self.frame_height = SCREEN_HEIGHT // 2

        self.margin_left = self.frame_width // 2
        self.margin_right = self.frame_width // 2
        self.margin_top = self.frame_height // 2
        self.margin_bottom = self.frame_height // 2

    def update(self, player_iso_x, player_iso_y):
        """
        Moves the camera offsets so the player stays in the 'dead zone'
        in the center of the screen.
        """
        screen_player_x = player_iso_x + self.offset_x
        screen_player_y = player_iso_y + self.offset_y

        # Horizontal check
        if screen_player_x < self.margin_left:
            self.offset_x += self.margin_left - screen_player_x
        elif screen_player_x > (SCREEN_WIDTH - self.margin_right):
            self.offset_x -= screen_player_x - (SCREEN_WIDTH - self.margin_right)

        # Vertical check
        if screen_player_y < self.margin_top:
            self.offset_y += self.margin_top - screen_player_y
        elif screen_player_y > (SCREEN_HEIGHT - self.margin_bottom):
            self.offset_y -= screen_player_y - (SCREEN_HEIGHT - self.margin_bottom)

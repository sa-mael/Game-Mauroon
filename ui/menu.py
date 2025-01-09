# ui/menu.py

import pygame
from ui.continue_button import ContinueButton
from ui.settings_button import SettingsButton
from ui.updates_button import UpdatesButton
from ui.history_button import HistoryButton

GRAY = (100, 100, 100)

class Menu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.start_game = False  # Set to True when user clicks "Continue"

        # Compute button size (e.g., 1/7 of screen width, or use min(screen_width, screen_height)//7)
        self.button_width = screen_width // 7
        self.button_height = screen_height // 14  # or screen_height // 7, depending on your layout

        # Create button instances
        # We'll place them centered horizontally, stacked vertically
        gap = 10  # space between buttons
        total_height = 4 * self.button_height + 3 * gap
        start_y = (screen_height - total_height) // 2

        # X for center
        button_x = (screen_width - self.button_width) // 2

        self.continue_button = ContinueButton(
            x=button_x,
            y=start_y,
            width=self.button_width,
            height=self.button_height,
            text="Continue",
            callback=self.on_continue_clicked
        )

        self.settings_button = SettingsButton(
            x=button_x,
            y=start_y + self.button_height + gap,
            width=self.button_width,
            height=self.button_height,
            text="Settings"
        )

        self.updates_button = UpdatesButton(
            x=button_x,
            y=start_y + 2*(self.button_height + gap),
            width=self.button_width,
            height=self.button_height,
            text="Updates"
        )

        self.history_button = HistoryButton(
            x=button_x,
            y=start_y + 3*(self.button_height + gap),
            width=self.button_width,
            height=self.button_height,
            text="History"
        )

        self.buttons = [
            self.continue_button,
            self.settings_button,
            self.updates_button,
            self.history_button
        ]

    def on_continue_clicked(self):
        """
        This function is called by the ContinueButton when it's clicked.
        """
        self.start_game = True

    def handle_event(self, event):
        """
        Pass events to all buttons.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for btn in self.buttons:
                btn.handle_click(mouse_pos)

    def update(self, dt):
        """
        If you had animations or button hover states, you could update them here.
        """
        pass

    def draw(self, surface):
        """
        Draw each button.
        """
        for btn in self.buttons:
            btn.draw(surface)

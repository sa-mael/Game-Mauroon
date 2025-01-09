import pygame
import sys

pygame.init()

# Параметры окна
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Меню на Pygame")

# Создаём часы для ограничения FPS
clock = pygame.time.Clock()

# Определим базовые цвета
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифт для текста на кнопках (можно указать любой системный шрифт или файл .ttf)
font = pygame.font.SysFont("Arial", 32)

# Список пунктов меню
menu_items = ["Продолжить", "Настройки", "Обновления", "История"]

# Небольшая функция для отрисовки кнопки:
def draw_button(surface, text, rect, bg_color, text_color):
    """
    surface  : поверхность (screen), на которой рисуем
    text     : текст кнопки (строка)
    rect     : pygame.Rect (x, y, width, height) — координаты и размеры кнопки
    bg_color : цвет фона (кнопки)
    text_color: цвет текста
    """
    # Рисуем прямоугольник (фон кнопки)
    pygame.draw.rect(surface, bg_color, rect)
    
    # Рендерим текст
    text_surface = font.render(text, True, text_color)
    # Центрируем текст внутри кнопки
    text_rect = text_surface.get_rect(center=rect.center)
    
    # Отображаем текст
    surface.blit(text_surface, text_rect)

def main():
    # Координаты для кнопок, чтобы все разместить по центру
    # Заранее зададим ширину и высоту каждой кнопки
    button_width = 300
    button_height = 60

    # Промежутки между кнопками
    spacing = 20

    # Начнём от середины экрана и распределим кнопки
    # Посчитаем, сколько всего места займут все кнопки + промежутки
    total_height = len(menu_items) * button_height + (len(menu_items) - 1) * spacing

    # Чтобы кнопки были по центру вертикали, нужно взять середину экрана и вычесть половину total_height
    start_y = (SCREEN_HEIGHT // 2) - (total_height // 2)

    # Создадим список Rect-ов для каждой кнопки
    button_rects = []
    for i, item in enumerate(menu_items):
        x = (SCREEN_WIDTH - button_width) // 2  # по центру горизонтально
        y = start_y + i * (button_height + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        button_rects.append(rect)

    running = True
    while running:
        screen.fill(BLACK)  # заливаем фон чёрным (можно любым другим цветом)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Обрабатываем клики мыши
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # левая кнопка
                mouse_pos = event.pos
                # Проверяем, на какую кнопку нажали
                for i, rect in enumerate(button_rects):
                    if rect.collidepoint(mouse_pos):
                        # В зависимости от индекса знаем, на какую кнопку нажали
                        if i == 0:
                            print("Нажали: Продолжить")
                            # Здесь можно поставить логику "продолжить игру", закрыть меню, и т.д.
                        elif i == 1:
                            print("Нажали: Настройки")
                        elif i == 2:
                            print("Нажали: Обновления")
                        elif i == 3:
                            print("Нажали: История")
                        # Можно добавить ещё кнопок, если требуется

        # Рисуем кнопки
        for i, rect in enumerate(button_rects):
            draw_button(screen, menu_items[i], rect, GRAY, WHITE)

        # Обновляем экран
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

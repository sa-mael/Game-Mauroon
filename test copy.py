import pygame
import sys

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Спрайт-класс в Pygame")

# Создание класса спрайта
class MySprite(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y):
        super().__init__()
        self.image = pygame.image.load(image_path)  # Загрузка изображения
        self.rect = self.image.get_rect()          # Получение прямоугольника спрайта
        self.rect.topleft = (x, y)                # Установка позиции

# Создание спрайта
sprite = MySprite("sprite.png", 100, 100)

# Группа спрайтов (для управления несколькими спрайтами)
all_sprites = pygame.sprite.Group()
all_sprites.add(sprite)

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Очистка экрана
    screen.fill((30, 30, 30))

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    # Обновление экрана
    pygame.display.flip()

# Выход
pygame.quit()
sys.exit()

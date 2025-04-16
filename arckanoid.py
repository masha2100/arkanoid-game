import pygame
import tkinter as tk
from tkinter import messagebox
from random import randrange as rnd
from arkanoid_logic import detect_collision

pygame.init()
pygame.font.init()

# Ініціалізація Tkinter
root = tk.Tk()
root.withdraw()  # Приховуємо головне вікно Tkinter

# Налаштування вікна гри
WIDTH, HEIGHT = 1000, 700  
fps = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Налаштування платформи
paddle_w = 300
paddle_h = 30
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# Налаштування м'яча
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Налаштування блоків
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(8) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(8 * 4)]

# Налаштування життів та рахунку
lives = 3
score = 0
font = pygame.font.SysFont('Arial', 30)

img = pygame.image.load('assets/1.jpg').convert()



# Функція перезапуску гри
def restart_game():
    global lives, score, block_list, color_list, ball, dx, dy
    lives = 3
    score = 0
    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(8) for j in range(4)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(8 * 4)]
    ball.x = rnd(ball_rect, WIDTH - ball_rect)
    ball.y = HEIGHT // 2
    dx, dy = 1, -1

# Запит на початок гри
start = messagebox.askyesno("Початок гри", "Хочете розпочати гру?")
if not start:
    pygame.quit()
    exit()

# Основний ігровий цикл
while True:
    sc.fill((0, 0, 0))  # Очищення екрану

    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEMOTION:
            paddle.centerx = event.pos[0]  # Рух платформи мишею

    # Рух м'яча
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # Відбиття м'яча від стін
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy

    # Взаємодія м'яча з платформою
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    # Взаємодія м'яча з блоками
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        score += 10  # +10 балів за знищений блок
        fps += 2

    # Перевірка на поразку (м'яч впав)
    if ball.bottom > HEIGHT:
        lives -= 1
        if lives == 0:
            sc.fill((0, 0, 0))  # Чорний екран
            game_over_text = font.render("GAME OVER", True, pygame.Color('red'))
            sc.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)

            restart = messagebox.askyesno("Гра закінчена", "Хочете зіграти ще раз?")
            if restart:
                restart_game()
                continue
            else:
                pygame.quit()
                exit()

        # Відновлення позиції м'яча та платформи
        ball.x = rnd(ball_rect, WIDTH - ball_rect)
        ball.y = HEIGHT // 2
        dx, dy = 1, -1
        paddle.x = WIDTH // 2 - paddle_w // 2
    
    # Перевірка на перемогу
    if not len(block_list):
        messagebox.showinfo("Перемога!", "Ви виграли!")
        pygame.quit()
        exit()

    # Відображення блоків
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]

    # Відображення платформи
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)

    # Відображення м'яча
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # Відображення життів та рахунку
    lives_text = font.render(f"Lives: {lives}  Score: {score}", True, pygame.Color('white'))
    sc.blit(lives_text, (10, 10))

    # Керування платформою за допомогою клавіш
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # Оновлення екрану
    pygame.display.flip()
    clock.tick(fps)

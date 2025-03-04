import pygame
import tkinter as tk
from tkinter import messagebox
from random import randrange as rnd

pygame.init()
pygame.font.init()

# Game settings
WIDTH, HEIGHT = 1000, 700  # Менше вікно для зручності
fps = 60

# Paddle settings
paddle_w = 300
paddle_h = 30
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

# Ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

# Blocks settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(8) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(8 * 4)]

# Lives and score settings
lives = 3
score = 0
font = pygame.font.SysFont('Arial', 30)

# Game window
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

# Background image
img = pygame.image.load('1.jpg').convert()

# Ініціалізація Tkinter для повідомлень
root = tk.Tk()
root.withdraw()  # Приховуємо головне вікно Tkinter

def detect_collision(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

def restart_game():
    global lives, score, block_list, color_list
    lives = 3
    score = 0
    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(8) for j in range(4)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(8 * 4)]

# 📌 Запит перед початком гри (Віконне повідомлення)
start = messagebox.askyesno("Початок гри", "Хочете розпочати гру?")
if not start:
    pygame.quit()
    exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEMOTION:
            paddle.centerx = event.pos[0]  # Рух платформи мишею

    sc.blit(img, (0, 0))

    # Draw blocks
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    
    # Draw paddle
    pygame.draw.rect(sc, pygame.Color('darkorange'), paddle)

    # Draw ball
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)

    # Ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # Collision with walls
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx = -dx
    if ball.centery < ball_radius:
        dy = -dy

    # Collision with paddle
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collision(dx, dy, ball, paddle)

    # Collision with blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        color_list.pop(hit_index)
        dx, dy = detect_collision(dx, dy, ball, hit_rect)
        score += 10  # +10 балів за знищений блок
        fps += 2

    # Check for game over (ball falls off the screen)
    if ball.bottom > HEIGHT:
        lives -= 1
        if lives == 0:
            # Відображення "GAME OVER"
            sc.fill((0, 0, 0))  # Чорний екран
            game_over_text = font.render("GAME OVER", True, pygame.Color('red'))
            sc.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.wait(2000)

            # 📌 Питаємо, чи гравець хоче ще раз (Віконне повідомлення)
            restart = messagebox.askyesno("Гра закінчена", "Хочете зіграти ще раз?")
            if restart:
                restart_game()
                continue
            else:
                pygame.quit()
                exit()

        else:
            # Reset ball and paddle positions
            ball.x = rnd(ball_rect, WIDTH - ball_rect)
            ball.y = HEIGHT // 2
            dx, dy = 1, -1
            paddle.x = WIDTH // 2 - paddle_w // 2  # Центруємо платформу

    # Win condition
    elif not len(block_list):
        messagebox.showinfo("Перемога!", "Ви виграли!")
        pygame.quit()
        exit()

    # Draw remaining lives and score
    lives_text = font.render(f"Lives: {lives}  Score: {score}", True, pygame.Color('white'))
    sc.blit(lives_text, (10, 10))

    # Control the paddle with arrow keys
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed

    # Update screen
    pygame.display.flip()
    clock.tick(fps)

import pygame
import tkinter as tk
from tkinter import messagebox
from random import randrange as rnd

pygame.init()
pygame.font.init()

root = tk.Tk()
root.withdraw()  # Приховуємо головне вікно Tkinter

WIDTH, HEIGHT = 1000, 700  # Менше вікно для зручності
fps = 60
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()

paddle_w = 300
paddle_h = 30
paddle_speed = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)

for event in pygame.event.get():
    if event.type == pygame.MOUSEMOTION:
        paddle.centerx = event.pos[0]  # Рух платформи мишею

ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT // 2, ball_rect, ball_rect)
dx, dy = 1, -1

ball.x += ball_speed * dx
ball.y += ball_speed * dy

block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(8) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(8 * 4)]

if ball.colliderect(paddle) and dy > 0:
    dx, dy = detect_collision(dx, dy, ball, paddle)

hit_index = ball.collidelist(block_list)
if hit_index != -1:
    hit_rect = block_list.pop(hit_index)
    color_list.pop(hit_index)
    dx, dy = detect_collision(dx, dy, ball, hit_rect)

if hit_index != -1:
    score += 10  # +10 балів за знищений блок
    fps += 2

if ball.bottom > HEIGHT:
    lives -= 1
    if lives == 0:
        sc.fill((0, 0, 0))  # Чорний екран
        game_over_text = font.render("GAME OVER", True, pygame.Color('red'))
        sc.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

font = pygame.font.SysFont('Arial', 30)
lives_text = font.render(f"Lives: {lives}  Score: {score}", True, pygame.Color('white'))
sc.blit(lives_text, (10, 10))

def restart_game():
    global lives, score, block_list, color_list
    lives = 3
    score = 0
    block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(8) for j in range(4)]
    color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for _ in range(8 * 4)]

start = messagebox.askyesno("Початок гри", "Хочете розпочати гру?")
if not start:
    pygame.quit()
    exit()

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        exit()


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

game_over_text = font.render("GAME OVER", True, pygame.Color('red'))
sc.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
pygame.display.flip()
pygame.time.wait(2000)

if not len(block_list):
    messagebox.showinfo("Перемога!", "Ви виграли!")
    pygame.quit()
    exit()

if ball.bottom > HEIGHT:
    lives -= 1
    ball.x = rnd(ball_rect, WIDTH - ball_rect)
    ball.y = HEIGHT // 2
    dx, dy = 1, -1
    paddle.x = WIDTH // 2 - paddle_w // 2  # Центруємо платформу

key = pygame.key.get_pressed()
if key[pygame.K_LEFT] and paddle.left > 0:
    paddle.left -= paddle_speed
if key[pygame.K_RIGHT] and paddle.right < WIDTH:
    paddle.right += paddle_speed


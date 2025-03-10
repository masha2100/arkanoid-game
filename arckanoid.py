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


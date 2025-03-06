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

import pygame
import pytest
from arkanoid_logic import detect_collision

@pytest.fixture
def setup():
    pygame.init()
    ball = pygame.Rect(50, 50, 20, 20)
    rect = pygame.Rect(60, 60, 100, 30)
    return ball, rect


@pytest.mark.parametrize("dx, dy", [(1, 1), (-1, 1), (1, -1), (-1, -1)])
def test_detect_collision(setup, dx, dy):
    ball, rect = setup
    new_dx, new_dy = detect_collision(dx, dy, ball, rect)
    assert isinstance(new_dx, int)
    assert isinstance(new_dy, int)

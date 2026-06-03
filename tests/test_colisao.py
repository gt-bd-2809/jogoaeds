"""Testes da função de colisão."""

import sys
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pygame
pygame.init()

from src.item import houve_colisao


def test_retangulos_sobrepostos_colidem():
    a = pygame.Rect(0, 0, 50, 50)
    b = pygame.Rect(25, 25, 50, 50)
    assert houve_colisao(a, b) is True


def test_retangulos_separados_nao_colidem():
    a = pygame.Rect(0, 0, 50, 50)
    b = pygame.Rect(100, 100, 50, 50)
    assert houve_colisao(a, b) is False


def test_retangulos_que_apenas_se_tocam_nao_colidem():
    a = pygame.Rect(0, 0, 50, 50)
    b = pygame.Rect(50, 0, 50, 50)
    assert houve_colisao(a, b) is False

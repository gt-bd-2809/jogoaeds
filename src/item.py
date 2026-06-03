"""Módulo de itens coletáveis."""

import random
import pygame
from src import settings


def houve_colisao(rect_a: pygame.Rect, rect_b: pygame.Rect) -> bool:
    """Retorna True se dois retângulos se sobrepõem (colisão real, sem apenas toque)."""
    return rect_a.colliderect(rect_b)


class Item:
    """Representa um fruto coletável no cenário."""

    def __init__(self, largura: int, altura: int) -> None:
        self.largura_tela = largura
        self.altura_tela = altura
        self.rect = pygame.Rect(0, 0, settings.ITEM_TAMANHO, settings.ITEM_TAMANHO)
        self.reposicionar()

    def reposicionar(self) -> None:
        """Move o item para uma posição aleatória dentro da tela."""
        self.rect.x = random.randint(0, self.largura_tela - settings.ITEM_TAMANHO)
        self.rect.y = random.randint(0, self.altura_tela - settings.ITEM_TAMANHO)

    def desenhar(self, tela: pygame.Surface) -> None:
        """Desenha o item na tela."""
        pygame.draw.rect(tela, settings.ITEM_COR, self.rect)

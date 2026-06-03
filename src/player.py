"""Módulo do jogador."""

import pygame
from src import settings


def calcular_pontuacao(pontos_atuais: int, itens_coletados: int) -> int:
    """Retorna a pontuação acumulada ignorando itens negativos."""
    if itens_coletados < 0:
        return pontos_atuais
    return pontos_atuais + itens_coletados * settings.PONTOS_POR_ITEM


class Jogador:
    """Representa o personagem controlado pelo jogador."""

    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, settings.JOGADOR_TAMANHO, settings.JOGADOR_TAMANHO)
        self.velocidade: int = settings.JOGADOR_VELOCIDADE
        self.pontos: int = 0

    def mover(self, dx: int, dy: int, largura: int, altura: int) -> None:
        """Move o jogador e mantém dentro dos limites da tela."""
        self.rect.x += dx * self.velocidade
        self.rect.y += dy * self.velocidade
        self.rect.clamp_ip(pygame.Rect(0, 0, largura, altura))

    def tratar_input(self, teclas: pygame.key.ScancodeWrapper, largura: int, altura: int) -> None:
        """Lê as teclas pressionadas e move o jogador."""
        dx = 0
        dy = 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -1
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = 1
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -1
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = 1
        if dx != 0 or dy != 0:
            self.mover(dx, dy, largura, altura)

    def desenhar(self, tela: pygame.Surface) -> None:
        """Desenha o jogador na tela."""
        pygame.draw.rect(tela, settings.JOGADOR_COR, self.rect)

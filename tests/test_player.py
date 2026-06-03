"""Testes da lógica do jogador."""

import sys
import os
os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pygame
pygame.init()

from src.player import Jogador, calcular_pontuacao


def test_calcular_pontuacao_soma_corretamente():
    assert calcular_pontuacao(0, 3) == 30


def test_calcular_pontuacao_ignora_valores_negativos():
    assert calcular_pontuacao(50, -2) == 50


def test_jogador_inicia_com_zero_pontos():
    jogador = Jogador(100, 100)
    assert jogador.pontos == 0


def test_jogador_nao_ultrapassa_limites_da_tela():
    jogador = Jogador(0, 0)
    # Tenta mover para fora da borda esquerda/superior
    jogador.mover(-10, -10, 800, 600)
    assert jogador.rect.x >= 0
    assert jogador.rect.y >= 0


def test_jogador_move_dentro_da_tela():
    jogador = Jogador(100, 100)
    jogador.mover(1, 1, 800, 600)
    assert jogador.rect.x == 100 + jogador.velocidade
    assert jogador.rect.y == 100 + jogador.velocidade

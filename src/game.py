"""Loop principal do jogo Floresta Sombria."""

import pygame
from src import settings
from src.player import Jogador, calcular_pontuacao
from src.item import Item, houve_colisao


def criar_tela() -> pygame.Surface:
    """Inicializa o Pygame e cria a janela principal."""
    pygame.init()
    tela = pygame.display.set_mode((settings.LARGURA, settings.ALTURA))
    pygame.display.set_caption(settings.TITULO)
    return tela


def processar_eventos() -> bool:
    """Processa os eventos do Pygame. Retorna False quando o jogo deve encerrar."""
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return False
    return True


def desenhar_hud(tela: pygame.Surface, fonte: pygame.font.Font, pontos: int) -> None:
    """Desenha a pontuação na tela."""
    texto = fonte.render(f"Pontos: {pontos}", True, settings.BRANCO)
    tela.blit(texto, (10, 10))


def atualizar_titulo(pontos: int) -> None:
    """Atualiza o título da janela com a pontuação atual."""
    pygame.display.set_caption(f"{settings.TITULO} — Pontos: {pontos}")


def executar() -> None:
    """Inicializa e executa o loop principal do jogo."""
    tela = criar_tela()
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, 36)

    jogador = Jogador(
        settings.LARGURA // 2 - settings.JOGADOR_TAMANHO // 2,
        settings.ALTURA // 2 - settings.JOGADOR_TAMANHO // 2,
    )
    item = Item(settings.LARGURA, settings.ALTURA)

    rodando = True
    while rodando:
        rodando = processar_eventos()

        # Entrada do jogador
        teclas = pygame.key.get_pressed()
        jogador.tratar_input(teclas, settings.LARGURA, settings.ALTURA)

        # Colisão com item
        if houve_colisao(jogador.rect, item.rect):
            jogador.pontos = calcular_pontuacao(jogador.pontos, 1)
            item.reposicionar()
            atualizar_titulo(jogador.pontos)

        # Desenho
        tela.fill(settings.COR_FUNDO)
        item.desenhar(tela)
        jogador.desenhar(tela)
        desenhar_hud(tela, fonte, jogador.pontos)

        pygame.display.flip()
        relogio.tick(settings.FPS)

    pygame.quit()

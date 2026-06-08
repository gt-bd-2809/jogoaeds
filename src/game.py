import random
import pygame
from src.config import (
    LARGURA, ALTURA, FPS, TITULO,
    COR_FUNDO, COR_JOGADOR, COR_FRUTO,
    COR_HUD_PTS, COR_HUD_VID,
    VELOCIDADE_JOGADOR, TAMANHO_JOGADOR, VIDAS_INICIAIS,
    TAMANHO_FRUTO, PONTOS_FRUTO,
)


def criar_jogador():
    return {
        "x":          LARGURA // 2 - TAMANHO_JOGADOR // 2,
        "y":          ALTURA  // 2 - TAMANHO_JOGADOR // 2,
        "tamanho":    TAMANHO_JOGADOR,
        "velocidade": VELOCIDADE_JOGADOR,
        "pontos":     0,
        "vidas":      VIDAS_INICIAIS,
    }


def criar_fruto():
    margem = TAMANHO_FRUTO + 10
    return {
        "x":    random.randint(margem, LARGURA - margem),
        "y":    random.randint(60,     ALTURA  - margem),
        "raio": TAMANHO_FRUTO // 2,
    }


def mover_jogador(jogador, teclas):
    if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]:
        jogador["x"] -= jogador["velocidade"]
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        jogador["x"] += jogador["velocidade"]
    if teclas[pygame.K_UP]    or teclas[pygame.K_w]:
        jogador["y"] -= jogador["velocidade"]
    if teclas[pygame.K_DOWN]  or teclas[pygame.K_s]:
        jogador["y"] += jogador["velocidade"]
    jogador["x"] = max(0, min(LARGURA - jogador["tamanho"], jogador["x"]))
    jogador["y"] = max(0, min(ALTURA  - jogador["tamanho"], jogador["y"]))


def verificar_coleta(jogador, fruto):
    t = jogador["tamanho"]
    r = fruto["raio"]
    rect_j = pygame.Rect(jogador["x"], jogador["y"], t, t)
    rect_f = pygame.Rect(fruto["x"] - r, fruto["y"] - r, r * 2, r * 2)
    return rect_j.colliderect(rect_f)


def desenhar_fundo(tela):
    tela.fill(COR_FUNDO)
    for linha in range(0, ALTURA, 64):
        for coluna in range(0, LARGURA, 64):
            pygame.draw.rect(tela, (28, 60, 28), (coluna + 1, linha + 1, 62, 62), 1)


def desenhar_jogador(tela, jogador):
    t    = jogador["tamanho"]
    rect = pygame.Rect(jogador["x"], jogador["y"], t, t)
    pygame.draw.rect(tela, COR_JOGADOR, rect, border_radius=8)
    pygame.draw.circle(tela, (0, 0, 0), (jogador["x"] + t // 3,     jogador["y"] + t // 3), 3)
    pygame.draw.circle(tela, (0, 0, 0), (jogador["x"] + 2 * t // 3, jogador["y"] + t // 3), 3)


def desenhar_fruto(tela, fruto):
    cx, cy, r = fruto["x"], fruto["y"], fruto["raio"]
    pygame.draw.circle(tela, COR_FRUTO, (cx, cy), r)
    pygame.draw.line(tela, (50, 140, 50), (cx, cy - r), (cx, cy - r - 8), 2)


def desenhar_hud(tela, fonte, jogador):
    tela.blit(fonte.render(f"Pontos: {jogador['pontos']}", True, COR_HUD_PTS), (10, 10))
    tela.blit(fonte.render(f"Vidas:  {jogador['vidas']}",  True, COR_HUD_VID), (10, 36))


def desenhar_controles(tela, fonte_peq):
    surf = fonte_peq.render("Mover: Setas / WASD   |   Sair: ESC", True, (100, 140, 100))
    tela.blit(surf, (LARGURA // 2 - surf.get_width() // 2, ALTURA - 26))


def processar_eventos():
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
            return False
    return True


def executar_jogo():
    pygame.init()
    tela      = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    relogio   = pygame.time.Clock()
    fonte     = pygame.font.SysFont("Arial", 24, bold=True)
    fonte_peq = pygame.font.SysFont("Arial", 18)
    jogador   = criar_jogador()
    fruto     = criar_fruto()
    rodando   = True
    while rodando:
        rodando = processar_eventos()
        teclas  = pygame.key.get_pressed()
        mover_jogador(jogador, teclas)
        if verificar_coleta(jogador, fruto):
            jogador["pontos"] += PONTOS_FRUTO
            fruto = criar_fruto()
        desenhar_fundo(tela)
        desenhar_fruto(tela, fruto)
        desenhar_jogador(tela, jogador)
        desenhar_hud(tela, fonte, jogador)
        desenhar_controles(tela, fonte_peq)
        pygame.display.flip()
        relogio.tick(FPS)
    pygame.quit()
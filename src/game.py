import random
import pygame
from src.config import (
  LARGURA, ALTURA, FPS, TITULO,
  COR_FUNDO, COR_JOGADOR, COR_FRUTO,
  COR_HUD_PTS, COR_HUD_VID,
  VELOCIDADE_JOGADOR, TAMANHO_JOGADOR, VIDAS_INICIAIS,
  TAMANHO_FRUTO, PONTOS_FRUTO,
)


# ── Criação dos elementos ─────────────────────────────────────────────────────

def criar_jogador():
  """
  Cria e retorna um dicionário com o estado inicial do jogador.
  O jogador começa no centro da tela.
  """
  return {
      "x":          LARGURA // 2 - TAMANHO_JOGADOR // 2,
      "y":          ALTURA  // 2 - TAMANHO_JOGADOR // 2,
      "tamanho":    TAMANHO_JOGADOR,
      "velocidade": VELOCIDADE_JOGADOR,
      "pontos":     0,
      "vidas":      VIDAS_INICIAIS,
  }


def criar_fruto():
  """
  Cria e retorna um dicionário com a posição aleatória do fruto.
  Evita as bordas da tela para não sobrepor o HUD.
  """
  margem = TAMANHO_FRUTO + 10
  return {
      "x":    random.randint(margem, LARGURA - margem),
      "y":    random.randint(60,     ALTURA  - margem),
      "raio": TAMANHO_FRUTO // 2,
  }


# ── Atualização ───────────────────────────────────────────────────────────────

def mover_jogador(jogador, teclas):
  """
  Atualiza a posição do jogador com base nas teclas pressionadas.
  Impede que o jogador saia dos limites da tela (clamping).
  """
  if teclas[pygame.K_LEFT]  or teclas[pygame.K_a]:
      jogador["x"] -= jogador["velocidade"]
  if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
      jogador["x"] += jogador["velocidade"]
  if teclas[pygame.K_UP]    or teclas[pygame.K_w]:
      jogador["y"] -= jogador["velocidade"]
  if teclas[pygame.K_DOWN]  or teclas[pygame.K_s]:
      jogador["y"] += jogador["velocidade"]

  # Limitar dentro dos limites da tela
  jogador["x"] = max(0, min(LARGURA - jogador["tamanho"], jogador["x"]))
  jogador["y"] = max(0, min(ALTURA  - jogador["tamanho"], jogador["y"]))


def verificar_coleta(jogador, fruto):
  """
  Verifica se o jogador tocou no fruto usando pygame.Rect.
  Retorna True se houve colisão, False caso contrário.
  """
  t = jogador["tamanho"]
  r = fruto["raio"]

  rect_jogador = pygame.Rect(jogador["x"], jogador["y"], t, t)
  rect_fruto   = pygame.Rect(fruto["x"] - r, fruto["y"] - r, r * 2, r * 2)

  return rect_jogador.colliderect(rect_fruto)


# ── Desenho ───────────────────────────────────────────────────────────────────

def desenhar_fundo(tela):
  """Preenche o fundo com a cor da floresta e desenha um grid sutil."""
  tela.fill(COR_FUNDO)
  cor_grade = (28, 60, 28)
  for linha in range(0, ALTURA, 64):
      for coluna in range(0, LARGURA, 64):
          pygame.draw.rect(tela, cor_grade, (coluna + 1, linha + 1, 62, 62), 1)


def desenhar_jogador(tela, jogador):
  """Desenha o jogador como um quadrado verde arredondado com olhos."""
  t    = jogador["tamanho"]
  rect = pygame.Rect(jogador["x"], jogador["y"], t, t)
  pygame.draw.rect(tela, COR_JOGADOR, rect, border_radius=8)
  # Olhos
  pygame.draw.circle(tela, (0, 0, 0), (jogador["x"] + t // 3,     jogador["y"] + t // 3), 3)
  pygame.draw.circle(tela, (0, 0, 0), (jogador["x"] + 2 * t // 3, jogador["y"] + t // 3), 3)


def desenhar_fruto(tela, fruto):
  """Desenha o fruto como um círculo laranja com um cabinho verde."""
  cx, cy = fruto["x"], fruto["y"]
  r      = fruto["raio"]
  pygame.draw.circle(tela, COR_FRUTO, (cx, cy), r)
  pygame.draw.line(tela, (50, 140, 50), (cx, cy - r), (cx, cy - r - 8), 2)


def desenhar_hud(tela, fonte, jogador):
  """Exibe pontuação e vidas no canto superior esquerdo."""
  surf_pts   = fonte.render(f"Pontos: {jogador['pontos']}", True, COR_HUD_PTS)
  surf_vidas = fonte.render(f"Vidas:  {jogador['vidas']}",  True, COR_HUD_VID)
  tela.blit(surf_pts,   (10, 10))
  tela.blit(surf_vidas, (10, 36))


def desenhar_controles(tela, fonte_peq):
  """Exibe dica de controles no rodapé da tela."""
  texto = "Mover: Setas / WASD   |   Sair: ESC"
  surf  = fonte_peq.render(texto, True, (100, 140, 100))
  tela.blit(surf, (LARGURA // 2 - surf.get_width() // 2, ALTURA - 26))


# ── Eventos ───────────────────────────────────────────────────────────────────

def processar_eventos():
  """
  Processa todos os eventos da fila do Pygame.
  Retorna False se o jogo deve encerrar, True caso contrário.
  """
  for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
          return False
      if evento.type == pygame.KEYDOWN:
          if evento.key == pygame.K_ESCAPE:
              return False
  return True


# ── Loop principal ────────────────────────────────────────────────────────────

def executar_jogo():
  """
  Inicializa o Pygame e executa o loop principal do jogo.
  Função chamada pelo main.py.
  """
  # Inicialização
  pygame.init()
  tela      = pygame.display.set_mode((LARGURA, ALTURA))
  pygame.display.set_caption(TITULO)
  relogio   = pygame.time.Clock()
  fonte     = pygame.font.SysFont("Arial", 24, bold=True)
  fonte_peq = pygame.font.SysFont("Arial", 18)

  # Criar elementos do jogo
  jogador = criar_jogador()
  fruto   = criar_fruto()

  # Loop principal
  rodando = True
  while rodando:

      # 1. Eventos
      rodando = processar_eventos()

      # 2. Atualização
      teclas = pygame.key.get_pressed()
      mover_jogador(jogador, teclas)

      if verificar_coleta(jogador, fruto):
          jogador["pontos"] += PONTOS_FRUTO
          fruto = criar_fruto()    # gera novo fruto após coleta

      # 3. Desenho
      desenhar_fundo(tela)
      desenhar_fruto(tela, fruto)
      desenhar_jogador(tela, jogador)
      desenhar_hud(tela, fonte, jogador)
      desenhar_controles(tela, fonte_peq)

      pygame.display.flip()
      relogio.tick(FPS)

  # Encerramento
  pygame.quit()
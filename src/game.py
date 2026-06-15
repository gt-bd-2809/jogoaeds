import random
import pygame
from src.config import (
    LARGURA, ALTURA, FPS, TITULO,
    COR_FUNDO, COR_JOGADOR, COR_FRUTO, COR_LOBO,
    COR_HUD_PTS, COR_HUD_VID, COR_CINZA,
    COR_VERMELHO, COR_AMARELO, COR_PRETO, COR_TEXTO,
    VELOCIDADE_JOGADOR, TAMANHO_JOGADOR, VIDAS_INICIAIS, FRAMES_INVULNERAVEL,
    TAMANHO_FRUTO, PONTOS_FRUTO,
    TAMANHO_LOBO, NOITES,
)
from src import logic
from src.ranking import carregar_ranking, adicionar_ao_ranking


def criar_jogador():
    return {
        "x": LARGURA // 2 - TAMANHO_JOGADOR // 2,
        "y": ALTURA // 2 - TAMANHO_JOGADOR // 2,
        "tamanho": TAMANHO_JOGADOR,
        "velocidade": VELOCIDADE_JOGADOR,
        "pontos": 0,
        "vidas": VIDAS_INICIAIS,
        "invulneravel": 0,
    }


def criar_fruto():
    margem = TAMANHO_FRUTO + 10
    return {
        "x": random.randint(margem, LARGURA - margem),
        "y": random.randint(60, ALTURA - margem),
        "raio": TAMANHO_FRUTO // 2,
    }


def criar_lobo(velocidade):
    lado = random.randint(0, 3)
    if lado == 0:
        x, y = random.randint(0, LARGURA), -TAMANHO_LOBO
    elif lado == 1:
        x, y = random.randint(0, LARGURA), ALTURA + TAMANHO_LOBO
    elif lado == 2:
        x, y = -TAMANHO_LOBO, random.randint(0, ALTURA)
    else:
        x, y = LARGURA + TAMANHO_LOBO, random.randint(0, ALTURA)
    return {"x": float(x), "y": float(y), "tamanho": TAMANHO_LOBO, "velocidade": velocidade}


def criar_lobos(quantidade, velocidade):
    return [criar_lobo(velocidade) for _ in range(quantidade)]


def criar_frutas(quantidade):
    return [criar_fruto() for _ in range(quantidade)]


def mover_jogador(jogador, teclas):
    dx, dy = 0, 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        dx -= jogador["velocidade"]
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        dx += jogador["velocidade"]
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        dy -= jogador["velocidade"]
    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        dy += jogador["velocidade"]
    jogador["x"] = logic.clamp(jogador["x"] + dx, 0, LARGURA - jogador["tamanho"])
    jogador["y"] = logic.clamp(jogador["y"] + dy, 0, ALTURA - jogador["tamanho"])
    if jogador["invulneravel"] > 0:
        jogador["invulneravel"] -= 1


def mover_lobos(lobos, jogador):
    cx = jogador["x"] + jogador["tamanho"] // 2
    cy = jogador["y"] + jogador["tamanho"] // 2
    for lobo in lobos:
        lobo["x"], lobo["y"] = logic.mover_em_direcao(lobo["x"], lobo["y"], cx, cy, lobo["velocidade"])


def verificar_coleta(jogador, frutas):
    t = jogador["tamanho"]
    rect_j = pygame.Rect(int(jogador["x"]), int(jogador["y"]), t, t)
    pontos_ganhos = 0
    restantes = []
    for fruta in frutas:
        r = fruta["raio"]
        rect_f = pygame.Rect(int(fruta["x"]) - r, int(fruta["y"]) - r, r * 2, r * 2)
        if rect_j.colliderect(rect_f):
            pontos_ganhos += PONTOS_FRUTO
        else:
            restantes.append(fruta)
    return restantes, pontos_ganhos


def verificar_colisao_lobos(jogador, lobos):
    if jogador["invulneravel"] > 0:
        return False
    t = jogador["tamanho"]
    rect_j = pygame.Rect(int(jogador["x"]), int(jogador["y"]), t, t)
    for lobo in lobos:
        tl = lobo["tamanho"]
        rect_l = pygame.Rect(int(lobo["x"]) - tl // 2, int(lobo["y"]) - tl // 2, tl, tl)
        if rect_j.colliderect(rect_l):
            return True
    return False


def desenhar_fundo(tela):
    tela.fill(COR_FUNDO)
    for linha in range(0, ALTURA, 64):
        for coluna in range(0, LARGURA, 64):
            pygame.draw.rect(tela, (28, 60, 28), (coluna + 1, linha + 1, 62, 62), 1)


def desenhar_jogador(tela, jogador):
    if jogador["invulneravel"] > 0 and (jogador["invulneravel"] // 6) % 2 == 1:
        return
    t = jogador["tamanho"]
    px = int(jogador["x"])
    py = int(jogador["y"])
    rect = pygame.Rect(px, py, t, t)
    pygame.draw.rect(tela, COR_JOGADOR, rect, border_radius=8)
    pygame.draw.circle(tela, COR_PRETO, (px + t // 3, py + t // 3), 3)
    pygame.draw.circle(tela, COR_PRETO, (px + 2 * t // 3, py + t // 3), 3)


def desenhar_frutas(tela, frutas):
    for fruta in frutas:
        cx, cy, r = int(fruta["x"]), int(fruta["y"]), fruta["raio"]
        pygame.draw.circle(tela, COR_FRUTO, (cx, cy), r)
        pygame.draw.line(tela, (50, 140, 50), (cx, cy - r), (cx, cy - r - 8), 2)


def desenhar_lobos(tela, lobos):
    for lobo in lobos:
        cx, cy, r = int(lobo["x"]), int(lobo["y"]), lobo["tamanho"] // 2
        pygame.draw.circle(tela, COR_LOBO, (cx, cy), r)
        pygame.draw.circle(tela, (220, 220, 0), (cx - 5, cy - 3), 3)
        pygame.draw.circle(tela, (220, 220, 0), (cx + 5, cy - 3), 3)


def desenhar_hud(tela, fontes, jogador, noite, timer):
    fn = fontes["normal"]
    fp = fontes["pequena"]
    tela.blit(fn.render("Vidas: " + str(jogador["vidas"]), True, COR_HUD_VID), (10, 10))
    tela.blit(fn.render("Pontos: " + str(jogador["pontos"]), True, COR_HUD_PTS), (10, 38))
    surf_n = fn.render("Noite " + str(noite), True, COR_TEXTO)
    tela.blit(surf_n, (LARGURA - surf_n.get_width() - 10, 10))
    surf_t = fp.render("Tempo: " + str(timer // FPS) + "s", True, COR_TEXTO)
    tela.blit(surf_t, (LARGURA - surf_t.get_width() - 10, 40))


def centralizar(tela, superficie, y):
    tela.blit(superficie, (LARGURA // 2 - superficie.get_width() // 2, y))


def tela_menu(tela, fontes):
    tela.fill(COR_PRETO)
    centralizar(tela, fontes["titulo"].render("Floresta Sombria", True, (34, 170, 34)), 120)
    centralizar(tela, fontes["normal"].render("Sobreviva as noites!", True, COR_CINZA), 210)
    centralizar(tela, fontes["grande"].render("ENTER  -  Jogar", True, COR_TEXTO), 300)
    centralizar(tela, fontes["normal"].render("R  -  Ver Ranking", True, COR_CINZA), 360)
    centralizar(tela, fontes["pequena"].render("ESC  -  Sair", True, COR_CINZA), 420)


def tela_game_over(tela, fontes, jogador, noite):
    tela.fill(COR_PRETO)
    centralizar(tela, fontes["titulo"].render("GAME OVER", True, COR_VERMELHO), 120)
    centralizar(tela, fontes["grande"].render("Pontos: " + str(jogador["pontos"]) + "   |   Noite: " + str(noite), True, COR_TEXTO), 230)
    centralizar(tela, fontes["normal"].render("ENTER  -  Salvar e ver Ranking", True, COR_AMARELO), 320)
    centralizar(tela, fontes["normal"].render("R  -  Jogar Novamente", True, COR_TEXTO), 370)
    centralizar(tela, fontes["pequena"].render("ESC  -  Menu Principal", True, COR_CINZA), 430)


def tela_ranking_screen(tela, fontes, ranking):
    tela.fill(COR_PRETO)
    centralizar(tela, fontes["titulo"].render("Ranking  Top 5", True, COR_AMARELO), 50)
    if not ranking:
        centralizar(tela, fontes["normal"].render("Nenhuma pontuacao registrada.", True, COR_CINZA), 220)
    else:
        cores = [COR_AMARELO, (200, 200, 200), (180, 120, 50), COR_TEXTO, COR_TEXTO]
        for i, e in enumerate(ranking):
            cor = cores[i] if i < len(cores) else COR_TEXTO
            txt = str(i + 1) + ".  " + str(e["nome"]) + "  -  " + str(e["pontos"]) + " pts   Noite " + str(e["noite"])
            centralizar(tela, fontes["normal"].render(txt, True, cor), 150 + i * 55)
    centralizar(tela, fontes["pequena"].render("ESC ou ENTER  -  Voltar", True, COR_CINZA), 510)


def tela_pausa(tela, fontes):
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 130))
    tela.blit(overlay, (0, 0))
    centralizar(tela, fontes["titulo"].render("PAUSADO", True, COR_TEXTO), 230)
    centralizar(tela, fontes["pequena"].render("P  -  Continuar", True, COR_CINZA), 320)


def eventos_menu():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return "sair"
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                return "jogar"
            if ev.key == pygame.K_r:
                return "ranking"
            if ev.key == pygame.K_ESCAPE:
                return "sair"
    return "menu"


def eventos_jogo(pausado):
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return "sair", pausado
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_p:
                return "jogando", not pausado
            if ev.key == pygame.K_ESCAPE:
                return "menu", False
    return "jogando", pausado


def eventos_game_over():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return "sair"
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                return "salvar"
            if ev.key == pygame.K_r:
                return "jogar"
            if ev.key == pygame.K_ESCAPE:
                return "menu"
    return "game_over"


def eventos_ranking():
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return "sair"
        if ev.type == pygame.KEYDOWN:
            if ev.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return "menu"
    return "ranking"


def executar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption(TITULO)
    relogio = pygame.time.Clock()

    fontes = {
        "titulo": pygame.font.SysFont("Arial", 56, bold=True),
        "grande": pygame.font.SysFont("Arial", 40, bold=True),
        "normal": pygame.font.SysFont("Arial", 28),
        "pequena": pygame.font.SysFont("Arial", 20),
    }

    estado = "menu"
    jogador = criar_jogador()
    frutas = []
    lobos = []
    noite = 1
    timer_noite = 0
    pausado = False
    ranking = carregar_ranking()
    nome_jogador = "Jogador"

    def iniciar_jogo():
        nonlocal jogador, frutas, lobos, noite, timer_noite, pausado
        noite = 1
        pausado = False
        jogador = criar_jogador()
        cfg = logic.get_config_noite(NOITES, noite)
        frutas = criar_frutas(cfg["frutas"])
        lobos = criar_lobos(cfg["lobos"], cfg["velocidade_lobo"])
        timer_noite = cfg["duracao"] * FPS

    def avancar_noite():
        nonlocal noite, frutas, lobos, timer_noite
        noite += 1
        cfg = logic.get_config_noite(NOITES, noite)
        frutas = criar_frutas(cfg["frutas"])
        lobos = criar_lobos(cfg["lobos"], cfg["velocidade_lobo"])
        timer_noite = cfg["duracao"] * FPS

    rodando = True
    while rodando:
        if estado == "menu":
            tela_menu(tela, fontes)
            acao = eventos_menu()
            if acao == "sair":
                rodando = False
            elif acao == "jogar":
                iniciar_jogo()
                estado = "jogando"
            elif acao == "ranking":
                ranking = carregar_ranking()
                estado = "ranking"
        elif estado == "jogando":
            acao, pausado = eventos_jogo(pausado)
            if acao == "sair":
                rodando = False
            elif acao == "menu":
                estado = "menu"
            if not pausado:
                teclas = pygame.key.get_pressed()
                mover_jogador(jogador, teclas)
                mover_lobos(lobos, jogador)
                frutas, pontos = verificar_coleta(jogador, frutas)
                jogador["pontos"] = logic.adicionar_pontos(jogador["pontos"], pontos)
                if not frutas:
                    frutas = criar_frutas(logic.get_config_noite(NOITES, noite)["frutas"])
                if verificar_colisao_lobos(jogador, lobos):
                    jogador["vidas"] = logic.perder_vida(jogador["vidas"])
                    jogador["invulneravel"] = FRAMES_INVULNERAVEL
                    if logic.is_game_over(jogador["vidas"]):
                        estado = "game_over"
                timer_noite -= 1
                if timer_noite <= 0:
                    avancar_noite()
            desenhar_fundo(tela)
            desenhar_frutas(tela, frutas)
            desenhar_lobos(tela, lobos)
            desenhar_jogador(tela, jogador)
            desenhar_hud(tela, fontes, jogador, noite, timer_noite)
            if pausado:
                tela_pausa(tela, fontes)
        elif estado == "game_over":
            tela_game_over(tela, fontes, jogador, noite)
            acao = eventos_game_over()
            if acao == "sair":
                rodando = False
            elif acao == "salvar":
                ranking = adicionar_ao_ranking(nome_jogador, jogador["pontos"], noite)
                estado = "ranking"
            elif acao == "jogar":
                iniciar_jogo()
                estado = "jogando"
            elif acao == "menu":
                estado = "menu"
        elif estado == "ranking":
            tela_ranking_screen(tela, fontes, ranking)
            acao = eventos_ranking()
            if acao == "sair":
                rodando = False
            elif acao == "menu":
                estado = "menu"
        pygame.display.flip()
        relogio.tick(FPS)
    pygame.quit()
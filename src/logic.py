import math


def clamp(valor, minimo, maximo):
    return max(minimo, min(maximo, valor))


def mover_em_direcao(x, y, alvo_x, alvo_y, velocidade):
    dx = alvo_x - x
    dy = alvo_y - y
    distancia = math.hypot(dx, dy)
    if distancia == 0:
        return x, y
    fator = min(velocidade / distancia, 1.0)
    return x + dx * fator, y + dy * fator


def adicionar_pontos(pontos_atuais, quantidade):
    if quantidade < 0:
        raise ValueError("Quantidade nao pode ser negativa")
    return pontos_atuais + quantidade


def perder_vida(vidas):
    return max(0, vidas - 1)


def is_game_over(vidas):
    return vidas <= 0


def get_config_noite(noites, numero_noite):
    idx = min(numero_noite - 1, len(noites) - 1)
    return noites[max(0, idx)]


def inserir_ranking(ranking, entrada, max_tamanho=5):
    atualizado = ranking + [entrada]
    atualizado.sort(key=lambda e: e["pontos"], reverse=True)
    return atualizado[:max_tamanho]
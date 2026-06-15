LARGURA = 800
ALTURA = 600
FPS = 60
TITULO = "Floresta Sombria"

COR_FUNDO = (18, 45, 18)
COR_JOGADOR = (50, 180, 50)
COR_FRUTO = (255, 140, 0)
COR_LOBO = (90, 60, 40)
COR_HUD_PTS = (255, 210, 0)
COR_HUD_VID = (220, 50, 50)
COR_TEXTO = (255, 255, 255)
COR_CINZA = (140, 140, 140)
COR_VERMELHO = (220, 50, 50)
COR_AMARELO = (255, 210, 0)
COR_PRETO = (0, 0, 0)

VELOCIDADE_JOGADOR = 4
TAMANHO_JOGADOR = 32
VIDAS_INICIAIS = 3
FRAMES_INVULNERAVEL = 120

TAMANHO_FRUTO = 20
PONTOS_FRUTO = 10

TAMANHO_LOBO = 28

NOITES = [
    {"lobos": 2, "velocidade_lobo": 1.5, "frutas": 6, "duracao": 30},
    {"lobos": 3, "velocidade_lobo": 2.0, "frutas": 5, "duracao": 30},
    {"lobos": 4, "velocidade_lobo": 2.5, "frutas": 4, "duracao": 30},
    {"lobos": 5, "velocidade_lobo": 3.0, "frutas": 4, "duracao": 30},
    {"lobos": 6, "velocidade_lobo": 3.5, "frutas": 3, "duracao": 30},
]

ARQUIVO_RANKING = "data/ranking.json"
MAX_RANKING = 5
import json
import os
from src.config import ARQUIVO_RANKING, MAX_RANKING
from src import logic


def carregar_ranking():
    if not os.path.exists(ARQUIVO_RANKING):
        return []
    try:
        with open(ARQUIVO_RANKING, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados if isinstance(dados, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def salvar_ranking(ranking):
    os.makedirs(os.path.dirname(ARQUIVO_RANKING), exist_ok=True)
    with open(ARQUIVO_RANKING, "w", encoding="utf-8") as f:
        json.dump(ranking, f, ensure_ascii=False, indent=2)


def adicionar_ao_ranking(nome, pontos, noite):
    entrada = {"nome": nome, "pontos": pontos, "noite": noite}
    atualizado = logic.inserir_ranking(carregar_ranking(), entrada, MAX_RANKING)
    salvar_ranking(atualizado)
    return atualizado
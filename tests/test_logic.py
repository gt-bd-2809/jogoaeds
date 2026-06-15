import pytest
from src import logic
from src.config import NOITES


class TestClamp:
    def test_dentro_do_intervalo(self):
        assert logic.clamp(5, 0, 10) == 5

    def test_abaixo_do_minimo(self):
        assert logic.clamp(-3, 0, 10) == 0

    def test_acima_do_maximo(self):
        assert logic.clamp(15, 0, 10) == 10

    def test_igual_ao_minimo(self):
        assert logic.clamp(0, 0, 10) == 0

    def test_igual_ao_maximo(self):
        assert logic.clamp(10, 0, 10) == 10


class TestMoverEmDirecao:
    def test_move_horizontal(self):
        nx, ny = logic.mover_em_direcao(0, 0, 10, 0, 1)
        assert abs(nx - 1.0) < 1e-6
        assert abs(ny) < 1e-6

    def test_nao_ultrapassa_destino(self):
        nx, ny = logic.mover_em_direcao(0, 0, 2, 0, 100)
        assert nx == 2.0

    def test_mesma_posicao(self):
        nx, ny = logic.mover_em_direcao(5, 5, 5, 5, 2)
        assert nx == 5.0 and ny == 5.0

    def test_move_diagonal(self):
        nx, ny = logic.mover_em_direcao(0, 0, 3, 4, 5)
        assert abs(nx - 3.0) < 1e-6
        assert abs(ny - 4.0) < 1e-6


class TestAdicionarPontos:
    def test_soma_normal(self):
        assert logic.adicionar_pontos(100, 10) == 110

    def test_soma_zero(self):
        assert logic.adicionar_pontos(50, 0) == 50

    def test_rejeita_negativos(self):
        with pytest.raises(ValueError):
            logic.adicionar_pontos(100, -1)

    def test_acumulacao(self):
        pts = 0
        for _ in range(5):
            pts = logic.adicionar_pontos(pts, 10)
        assert pts == 50


class TestPerderVida:
    def test_perde_uma_vida(self):
        assert logic.perder_vida(3) == 2

    def test_floor_zero(self):
        assert logic.perder_vida(0) == 0

    def test_ultima_vida(self):
        assert logic.perder_vida(1) == 0


class TestIsGameOver:
    def test_zero_vidas(self):
        assert logic.is_game_over(0) is True

    def test_uma_vida(self):
        assert logic.is_game_over(1) is False

    def test_tres_vidas(self):
        assert logic.is_game_over(3) is False


class TestGetConfigNoite:
    def test_primeira_noite(self):
        assert logic.get_config_noite(NOITES, 1) == NOITES[0]

    def test_ultima_noite(self):
        assert logic.get_config_noite(NOITES, len(NOITES)) == NOITES[-1]

    def test_clamp_acima(self):
        assert logic.get_config_noite(NOITES, 999) == NOITES[-1]

    def test_progressao_velocidade(self):
        for i in range(1, len(NOITES)):
            assert NOITES[i]["velocidade_lobo"] > NOITES[i - 1]["velocidade_lobo"]

    def test_progressao_lobos(self):
        for i in range(1, len(NOITES)):
            assert NOITES[i]["lobos"] > NOITES[i - 1]["lobos"]


class TestInserirRanking:
    def test_insere_vazio(self):
        r = logic.inserir_ranking([], {"nome": "A", "pontos": 100, "noite": 1})
        assert len(r) == 1

    def test_limite_maximo(self):
        r = []
        for i in range(7):
            r = logic.inserir_ranking(r, {"nome": "P" + str(i), "pontos": i * 10, "noite": 1})
        assert len(r) == 5

    def test_ordem_decrescente(self):
        r = logic.inserir_ranking([], {"nome": "B", "pontos": 50, "noite": 1})
        r = logic.inserir_ranking(r, {"nome": "A", "pontos": 100, "noite": 1})
        assert r[0]["nome"] == "A"
        assert r[1]["nome"] == "B"

    def test_nao_modifica_original(self):
        original = [{"nome": "X", "pontos": 200, "noite": 2}]
        logic.inserir_ranking(original, {"nome": "Y", "pontos": 150, "noite": 1})
        assert len(original) == 1
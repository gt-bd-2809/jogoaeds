# Floresta Sombria

Jogo 2D de **sobrevivência simples** em visão *top-down*, desenvolvido em **Python + Pygame**
como trabalho da disciplina de Introdução a Algoritmos / Programação — PUC Minas (CDIA).

> **Status:** Semana 1 concluída (documentação e proposta). Implementação começa na Semana 2.

## Integrantes
- Bernardo Demaria Santos
- Victhor Guilherme
- Lucas Domingos
- Gabriel Ovidio

## Descrição
O jogador controla um sobrevivente perdido em uma floresta sombria. Ele coleta frutos
para somar pontos e precisa desviar de lobos e obstáculos. O jogo é dividido em
**noites** (fases) com dificuldade progressiva e mantém um ranking dos 5 melhores
resultados.

## Objetivo
Sobreviver ao maior número possível de noites acumulando pontos e entrar no ranking.

## Regras (resumo)
- Inicia com 3 vidas e 0 pontos.
- Cada fruto coletado vale 10 pontos.
- Encostar em um lobo custa 1 vida.
- O jogo termina ao zerar as vidas.

## Controles
| Tecla            | Ação                  |
|------------------|-----------------------|
| Setas ou WASD    | Mover                 |
| Espaço           | Interagir / coletar   |
| P                | Pausar                |
| Enter            | Confirmar nos menus   |
| ESC              | Sair                  |

## Estrutura de pastas prevista
```
jogoaeds/
├── assets/           # imagens e sons
├── data/             # ranking.json e configs
├── docs/             # proposta e documentação
├── src/              # código-fonte do jogo
├── tests/            # testes automatizados (pytest)
├── main.py           # ponto de entrada
├── requirements.txt
└── README.md
```

## Como executar (a partir da Semana 2)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Rodar os testes:
```powershell
.\.venv\Scripts\python.exe -m pytest -v
```

## Cronograma
| Semana | Data  | Entrega                                              | Status        |
|--------|-------|------------------------------------------------------|---------------|
| 1      | 31/05 | Documentação + proposta                              | ✅ Concluída  |
| 2      | 07/06 | Protótipo executável                                 | ⏳ Próxima    |
| 3      | 14/06 | Versão quase completa (regras, ranking, testes)      | ⏳            |
| 4      | 21/06 | Versão final + apresentação                          | ⏳            |

## Checklist mínimo
- [x] Proposta (`docs/proposta.md`)
- [x] README preenchido
- [ ] Protótipo jogável
- [ ] Sistema de pontuação, vidas e ranking
- [ ] Testes automatizados
- [ ] Versão final apresentável

## Referências de assets
- [Kenney.nl](https://kenney.nl/) — sprites e ícones gratuitos.
- [OpenGameArt](https://opengameart.org/) — arte livre para jogos.
- [itch.io — game assets](https://itch.io/game-assets/free) — pacotes gratuitos.

## Baseado no template
[ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template](https://github.com/ICEI-PUC-Minas-PPL-CDIA/IntroAlgs_pygame_template)

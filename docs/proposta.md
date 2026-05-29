# Proposta — Floresta Sombria

## 1. Nome do jogo
**Floresta Sombria**

## 2. Integrantes
- Bernardo Demaria Santos
- Victhor Guilherme
- Lucas Domingos
- Gabriel Ouvidio

## 3. Tipo de jogo
Jogo 2D de **sobrevivência simples** com visão *top-down*, desenvolvido em **Python + Pygame**.

## 4. Descrição
O jogador controla um sobrevivente perdido em uma floresta sombria. Para se manter vivo,
precisa coletar frutos e água espalhados pelo cenário enquanto desvia de lobos, espinhos
e galhos caídos. O jogo é dividido em **noites** (fases) com dificuldade progressiva: a
cada noite surgem mais inimigos e eles se movem mais rápido.

## 5. Objetivo
Sobreviver ao maior número possível de noites, acumulando pontos ao coletar recursos.
A pontuação final é registrada em um ranking dos 5 melhores jogadores.

## 6. Regras
- O jogador inicia com **3 vidas** e **0 pontos** na primeira noite.
- Cada fruto coletado vale **10 pontos**.
- Encostar em um lobo causa **perda de 1 vida** com um curto período de invulnerabilidade.
- A cada intervalo de tempo o jogo avança para a próxima noite, aumentando a dificuldade.
- O jogador não pode sair dos limites da tela.

## 7. Condição de vitória
Não há vitória definitiva — o objetivo é **sobreviver o máximo possível** e entrar no
ranking dos 5 melhores. Concluir a última noite configurada conta como "vitória de etapa".

## 8. Condição de derrota
O jogo termina quando o jogador atinge **0 vidas**. A pontuação final é apresentada e,
se estiver entre as 5 melhores, é gravada no ranking.

## 9. Elementos do jogo
- **Jogador**: sobrevivente controlável.
- **Itens coletáveis**: frutos (e, futuramente, água).
- **Inimigos**: lobos que perseguem o jogador.
- **Obstáculos**: espinhos e galhos (escopo desejável).
- **Cenário**: floresta em tons escuros de verde.
- **HUD**: pontuação, vidas e noite atual.

## 10. Controles
| Tecla            | Ação                  |
|------------------|-----------------------|
| Setas ou WASD    | Mover o jogador       |
| Espaço           | Interagir / coletar   |
| P                | Pausar                |
| Enter            | Confirmar nos menus   |
| ESC              | Sair                  |

## 11. Estruturas de dados previstas
- **Listas** para manter inimigos e itens ativos no cenário.
- **Dicionários** para configurar cada noite (quantidade de lobos, velocidade).
- **`pygame.Rect`** como estrutura central de posição e colisão.
- **Lista de dicionários** para o ranking (`{"nome", "pontos", "noite"}`).

## 12. Uso de arquivos
- `data/ranking.json` — leitura e escrita do ranking persistente (top 5).
- Possível arquivo de configuração das noites (`data/noites.json`) no escopo desejável.

## 13. Testes planejados
- Cálculo e acumulação de pontuação (incluindo rejeição de valores negativos).
- Limites de movimentação do jogador (clamping na tela).
- Detecção de colisão entre retângulos.
- Inserção ordenada no ranking e limite de 5 entradas.
- Movimentação do inimigo em direção ao jogador.
- Transição entre noites.

## 14. Dificuldades esperadas
- Equilibrar dificuldade progressiva sem tornar o jogo injusto.
- Manter o código modular e testável separando lógica pura da renderização.
- Compatibilidade do Pygame com Python 3.14 (resolvida usando `pygame-ce`).
- Carregar/salvar JSON tratando arquivo inexistente ou corrompido.

## 15. Escopo mínimo
- Janela Pygame funcional com jogador controlável.
- Pelo menos um tipo de item coletável com pontuação.
- Pelo menos um inimigo com colisão e perda de vida.
- Condição de derrota (Game Over) e reinício.
- Ranking persistente em JSON.
- Testes automatizados das funções puras principais.

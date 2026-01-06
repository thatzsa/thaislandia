import pygame
import math
from constantes import BRANCO, PRETO, CEU_AZUL, AMARELO

class MinijogoMontanhaRussa:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.finalizado = False

        self.pontuacao = 0
        self.vidas = 3

        self.carrinho_x = 100
        self.carrinho_y = altura // 2
        self.velocidade = 3

        self.offset_trilha = 0
        self.pontos_trilha = self.gerar_trilha()

        self.zonas_altas = []
        self.criar_zonas_altas()

        self.braco_levantado = False
        self.feedback_timer = 0
        self.feedback_texto = ""

        self.game_over = False
        self.game_over_timer = 0

        self.fonte = pygame.font.SysFont("monospace", 30, bold=True)
        self.fonte_grande = pygame.font.SysFont("monospace", 50, bold=True)

    def gerar_trilha(self):
        pontos = []
        # Gera uma trilha longa
        for x in range(0, 6000, 10):
            y = self.altura // 2 + math.sin(x * 0.01) * 150
            pontos.append((x, y))
        return pontos

    def criar_zonas_altas(self):
        # Identifica os picos da montanha russa (onde deve levantar o braço)
        for i in range(1, len(self.pontos_trilha) - 1):
            _, y_prev = self.pontos_trilha[i - 1]
            x, y = self.pontos_trilha[i]
            _, y_next = self.pontos_trilha[i + 1]

            # Se é um pico local e está alto na tela
            if y < y_prev and y < y_next and y < self.altura // 2 - 50:
                self.zonas_altas.append({
                    "x": x,
                    "y": y,
                    "ativa": True,
                    "passou": False
                })

    def atualizar(self, eventos):
        # 1. INPUT (Eventos)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.finalizado = True
                elif evento.key == pygame.K_SPACE:
                    self.braco_levantado = True
            
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_SPACE:
                    self.braco_levantado = False

        # 2. LÓGICA DO JOGO
        if self.game_over:
            self.game_over_timer += 1
            if self.game_over_timer > 180: # Espera 3 seg e sai
                self.finalizado = True
            return

        self.offset_trilha += self.velocidade

        if self.feedback_timer > 0:
            self.feedback_timer -= 1

        # Verifica colisão com zonas altas (picos)
        for zona in self.zonas_altas:
            if not zona["ativa"]:
                continue

            x_tela = zona["x"] - self.offset_trilha
            distancia = x_tela - self.carrinho_x

            # Se está passando pelo pico agora (-40 a +40 pixels)
            if -40 <= distancia <= 40 and not zona["passou"]:
                if self.braco_levantado:
                    self.pontuacao += 20
                    zona["ativa"] = False
                    zona["passou"] = True
                    self.feedback_texto = "PERFEITO!"
                    self.feedback_timer = 30
            
            # Se já passou do pico e não pegou
            elif distancia < -40 and not zona["passou"]:
                self.vidas -= 1
                zona["ativa"] = False
                zona["passou"] = True
                self.feedback_texto = "PERDEU!"
                self.feedback_timer = 30

                if self.vidas <= 0:
                    self.game_over = True

        # Atualiza altura do carrinho com base na trilha
        indice = int(self.offset_trilha // 10)
        if indice < len(self.pontos_trilha):
            self.carrinho_y = self.pontos_trilha[indice][1]
        else:
            self.game_over = True # Acabou a trilha

    def desenhar(self, tela):
        tela.fill(CEU_AZUL)

        # Desenha a trilha visível
        pontos_visiveis = []
        for x, y in self.pontos_trilha:
            xt = x - self.offset_trilha
            # Só adiciona se estiver na tela (com margem)
            if -10 <= xt <= self.largura + 10:
                pontos_visiveis.append((xt, y))

        if len(pontos_visiveis) > 1:
            pygame.draw.lines(tela, (139, 69, 19), False, pontos_visiveis, 8)

        # Desenha os indicadores das zonas altas (círculos amarelos nos picos)
        for zona in self.zonas_altas:
            if zona["ativa"]:
                xt = zona["x"] - self.offset_trilha
                if 0 <= xt <= self.largura:
                    pygame.draw.circle(tela, AMARELO, (int(xt), int(zona["y"])), 25, 3)

        # Desenha o carrinho
        cor = (50, 255, 50) if self.braco_levantado else (255, 50, 50)
        # Corpo
        pygame.draw.rect(tela, cor, (self.carrinho_x - 20, int(self.carrinho_y) - 20, 40, 40))
        # Borda
        pygame.draw.rect(tela, PRETO, (self.carrinho_x - 20, int(self.carrinho_y) - 20, 40, 40), 3)

        # HUD
        tela.blit(self.fonte.render(f"PONTOS: {self.pontuacao}", True, AMARELO), (20, 20))
        tela.blit(self.fonte.render("VIDAS:", True, BRANCO), (20, 60))
        for i in range(self.vidas):
            pygame.draw.circle(tela, (255, 50, 50), (130 + i * 30, 75), 10)

        # Feedback (Perfeito/Perdeu)
        if self.feedback_timer > 0:
            cor = (50, 255, 50) if self.feedback_texto == "PERFEITO!" else (255, 50, 50)
            txt = self.fonte_grande.render(self.feedback_texto, True, cor)
            tela.blit(txt, txt.get_rect(center=(self.largura // 2, self.altura // 2)))

        # Game Over
        if self.game_over:
            overlay = pygame.Surface((self.largura, self.altura))
            overlay.set_alpha(200)
            overlay.fill(PRETO)
            tela.blit(overlay, (0, 0))

            fim = self.fonte_grande.render("FIM DA VIAGEM", True, BRANCO)
            tela.blit(fim, fim.get_rect(center=(self.largura // 2, self.altura // 2)))
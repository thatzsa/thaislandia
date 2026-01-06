import pygame
from constantes import BRANCO, PRETO, CEU_AZUL, AMARELO

class MinijogoRodaGigante:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.finalizado = False # Controle para o main.py saber quando sair

        self.pontuacao = 0
        self.vidas = 3

        self.vomitometro = 0
        self.taxa_aumento = 0.3
        self.taxa_diminuicao = 1.0

        self.olhando_fora = True
        self.vomitou = False
        self.tempo_vomito = 0

        self.zona_amarela = 60
        self.zona_vermelha = 80
        self.limite_vomito = 100

        self.game_over = False
        self.game_over_timer = 0

        self.fonte = pygame.font.SysFont("monospace", 28, bold=True)
        self.fonte_grande = pygame.font.SysFont("monospace", 50, bold=True)
        self.fonte_pequena = pygame.font.SysFont("monospace", 20, bold=True)

    def atualizar(self, eventos):
        # 1. PROCESSAMENTO DE EVENTOS (Input)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.finalizado = True
                
                # Tecla ESPAÇO alterna a visão (se não estiver enjoado)
                if evento.key == pygame.K_SPACE:
                    if not self.vomitou: 
                        self.olhando_fora = not self.olhando_fora

        # 2. LÓGICA DO JOGO (Timer, Vômito, Pontos)
        if self.game_over:
            self.game_over_timer += 1
            if self.game_over_timer > 180: # Espera 3 segundos e sai
                self.finalizado = True
            return

        if self.olhando_fora:
            self.vomitometro += self.taxa_aumento
            self.pontuacao += 1
        else:
            self.vomitometro -= self.taxa_diminuicao

        self.vomitometro = max(0, min(100, self.vomitometro))

        if self.vomitometro >= self.limite_vomito:
            self.vidas -= 1
            self.vomitometro = 0
            self.vomitou = True
            self.tempo_vomito = 90 # 1.5 segundos de penalidade
            if self.vidas <= 0:
                self.game_over = True

        if self.tempo_vomito > 0:
            self.tempo_vomito -= 1
            if self.tempo_vomito == 0:
                self.vomitou = False

    def desenhar(self, tela):
        # Define cor do fundo
        cor_fundo = CEU_AZUL if self.olhando_fora else (80, 80, 100)
        tela.fill(cor_fundo)

        titulo = "VISTA EXTERNA" if self.olhando_fora else "DENTRO DA CABINE"
        tela.blit(self.fonte_grande.render(titulo, True, BRANCO),
                  (self.largura // 2 - 180, 80))

        # Placar
        tela.blit(self.fonte.render(f"PONTOS: {self.pontuacao}", True, AMARELO), (20, 20))
        tela.blit(self.fonte.render(f"VIDAS: {self.vidas}", True, BRANCO), (20, 50))
        
        # Instrução
        instrucao = self.fonte_pequena.render("ESPAÇO: Alternar Visão | ESC: Sair", True, BRANCO)
        tela.blit(instrucao, (20, self.altura - 30))

        self.desenhar_vomitometro(tela)

        if self.game_over:
            overlay = pygame.Surface((self.largura, self.altura))
            overlay.set_alpha(200)
            overlay.fill(PRETO)
            tela.blit(overlay, (0, 0))

            fim = self.fonte_grande.render("VOMITOU DEMAIS!", True, (255, 100, 100))
            tela.blit(fim, fim.get_rect(center=(self.largura // 2, self.altura // 2)))

    def desenhar_vomitometro(self, tela):
        barra_x = 50
        barra_y = self.altura - 120
        barra_l = self.largura - 100
        barra_h = 40

        pygame.draw.rect(tela, (50, 50, 50), (barra_x, barra_y, barra_l, barra_h))
        pygame.draw.rect(tela, BRANCO, (barra_x, barra_y, barra_l, barra_h), 3)

        largura = int((self.vomitometro / 100) * barra_l)

        if self.vomitometro < self.zona_amarela:
            cor = (50, 200, 50)
        elif self.vomitometro < self.zona_vermelha:
            cor = AMARELO
        else:
            cor = (255, 50, 50)

        pygame.draw.rect(tela, cor, (barra_x, barra_y, largura, barra_h))
        tela.blit(self.fonte_pequena.render(f"ENJOO: {int(self.vomitometro)}%", True, BRANCO),
                  (barra_x + barra_l - 120, barra_y - 25))
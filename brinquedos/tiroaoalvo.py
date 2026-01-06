import pygame
import random
from constantes import BRANCO, PRETO, AMARELO

class Alvo:
    def __init__(self, largura_tela, altura_tela):
        self.raio = random.randint(20, 40)
        self.x = random.randint(self.raio, largura_tela - self.raio)
        self.y = random.randint(self.raio, altura_tela - self.raio)
        self.cor = (random.randint(150, 255), 0, 0) 

    def desenhar(self, tela):
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), self.raio)
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio * 0.7)
        pygame.draw.circle(tela, BRANCO, (self.x, self.y), self.raio * 0.4)
        pygame.draw.circle(tela, self.cor, (self.x, self.y), self.raio * 0.2)

    def foi_atingido(self, pos_mouse):
        distancia = ((self.x - pos_mouse[0])**2 + (self.y - pos_mouse[1])**2)**0.5
        return distancia <= self.raio

class MinijogoTiroAoAlvo:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.alvos = []
        self.pontuacao = 0
        self.spawn_timer = 0
        self.fonte = pygame.font.SysFont("monospace", 30, bold=True)
        self.finalizado = False # Nova flag para controle de saída

    def atualizar(self, eventos):
        # 1. Gerencia Entrada (Cliques e ESC)
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.finalizado = True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                self.gerenciar_clique(evento.pos)

        # 2. Lógica de Spawn (criar novos alvos a cada 1 segundo/60 frames)
        self.spawn_timer += 1
        if self.spawn_timer >= 60:
            self.alvos.append(Alvo(self.largura, self.altura))
            self.spawn_timer = 0

    def gerenciar_clique(self, pos_mouse):
        # Verifica se clicou em algum alvo (do último para o primeiro - ordem de desenho)
        for alvo in reversed(self.alvos):
            if alvo.foi_atingido(pos_mouse):
                self.alvos.remove(alvo)
                self.pontuacao += 10
                return True
        return False

    def desenhar(self, tela):
        tela.fill((50, 50, 50)) 
        for alvo in self.alvos:
            alvo.desenhar(tela)
        
        # Placar
        texto_pontos = self.fonte.render(f"PONTOS: {self.pontuacao}", True, AMARELO)
        tela.blit(texto_pontos, (20, 20))
        
        # Instrução
        instrucao = self.fonte.render("ESC para Sair", True, BRANCO)
        tela.blit(instrucao, (self.largura - 250, 20))
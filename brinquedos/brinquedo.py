import pygame
from constantes import VERDE_PARQUE, BRANCO

class Brinquedo:
    def __init__(self, nome, x, y, largura, altura):
        self.nome = nome
        self.rect = pygame.Rect(x, y, largura, altura)
        self.cor = VERDE_PARQUE
        self.fonte = pygame.font.SysFont("Arial", 18, bold=True)

    def desenhar(self, tela, camera_x):
        # Cria um rect temporário para desenho baseado na câmera
        rect_desenho = self.rect.copy()
        rect_desenho.x -= camera_x
        
        # Desenha o brinquedo
        pygame.draw.rect(tela, self.cor, rect_desenho, border_radius=10)
        
        # Desenha o texto centralizado
        texto = self.fonte.render(self.nome, True, BRANCO)
        texto_rect = texto.get_rect(center=rect_desenho.center)
        tela.blit(texto, texto_rect)

    def clicou(self, mouse_pos, camera_x):
        # Ajusta a posição do clique para o sistema de coordenadas do mundo
        pos_mundo = (mouse_pos[0] + camera_x, mouse_pos[1])
        return self.rect.collidepoint(pos_mundo)
import pygame
from constantes import BRANCO

class Brinquedo:
    def __init__(self, nome, x, y, largura, altura):
        self.nome = nome
        self.rect = pygame.Rect(x, y, largura, altura)
        # Mudamos de VERDE_PARQUE para uma cor de "madeira" (Marrom)
        self.cor = (139, 69, 19) 
        self.fonte = pygame.font.SysFont("Arial", 18, bold=True)
        self.cor_texto = BRANCO

    def desenhar(self, tela, camera_x):
        # Cria um rect temporário para desenho baseado na câmera
        rect_desenho = self.rect.copy()
        rect_desenho.x -= camera_x
        
        # 1. Desenha a "placa" (fundo do botão)
        pygame.draw.rect(tela, self.cor, rect_desenho, border_radius=10)
        
        # 2. Desenha uma borda branca para destacar ainda mais
        pygame.draw.rect(tela, BRANCO, rect_desenho, 2, border_radius=10)
        
        # 3. Desenha o texto centralizado
        texto = self.fonte.render(self.nome, True, self.cor_texto)
        texto_rect = texto.get_rect(center=rect_desenho.center)
        tela.blit(texto, texto_rect)

    def clicou(self, mouse_pos, camera_x):
        # Ajusta a posição do clique para o sistema de coordenadas do mundo
        pos_mundo = (mouse_pos[0] + camera_x, mouse_pos[1])
        return self.rect.collidepoint(pos_mundo)
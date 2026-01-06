import pygame
import sys

def rodar_jogo():
    # Inicializa todos os módulos do Pygame
    pygame.init()

    # Configurações da tela
    LARGURA, ALTURA = 800, 600
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Parque da Thais - v0.1")
    
    # Gerenciador de tempo (FPS)
    relogio = pygame.time.Clock()

    # Loop principal
    while True:
        # 1. EVENTOS (Entradas do usuário)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 2. LÓGICA (Onde o backend vai rodar)
        # (Por enquanto vazio)

        # 3. RENDERIZAÇÃO (Onde o frontend aparece)
        tela.fill((20, 20, 20)) # Cor de fundo (quase preto)
        
        # Atualiza o que aparece na tela
        pygame.display.flip()
        
        # Trava o jogo em 60 quadros por segundo
        relogio.tick(60)

if __name__ == "__main__":
    rodar_jogo()
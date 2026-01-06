import pygame
import sys
from constantes import *
from brinquedos.brinquedo import Brinquedo

def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Thaislandia - v0.1")
    relogio = pygame.time.Clock()
    
    estado_atual = "MENU" 
    camera_x = 0
    
    # Instanciando os brinquedos como objetos
    brinquedos = [
        Brinquedo("Montanha Russa", 200, 250, 150, 100),
        Brinquedo("Roda Gigante", 500, 250, 150, 100),
        Brinquedo("Carrossel", 800, 250, 150, 100),
        Brinquedo("Tiro ao Alvo", 1100, 250, 150, 100),
    ]
    
    while True:
        # 1. EVENTOS
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN and estado_atual == "MENU":
                for b in brinquedos:
                    if b.clicou(evento.pos, camera_x):
                        print(f"Entrando no minijogo: {b.nome}")
                        estado_atual = b.nome.upper().replace(" ", "_")
        
        # 2. LÓGICA
        if estado_atual == "MENU":
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                camera_x = max(0, camera_x - VELOCIDADE_CAMERA)
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                camera_x = min(LARGURA_MUNDO - LARGURA, camera_x + VELOCIDADE_CAMERA)
        
        elif estado_atual == "TIRO_AO_ALVO":
            # Lógica de volta para o menu
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                estado_atual = "MENU"
        
        # 3. RENDERIZAÇÃO
        tela.fill(PRETO)
        
        if estado_atual == "MENU":
            for b in brinquedos:
                b.desenhar(tela, camera_x)
        else:
            # Placeholder para os minijogos
            fonte = pygame.font.Font(None, 50)
            msg = f"MINIJOGO: {estado_atual}"
            texto = fonte.render(msg, True, BRANCO)
            tela.blit(texto, (50, ALTURA//2))

        pygame.display.flip()
        relogio.tick(FPS)

if __name__ == "__main__":
    rodar_jogo()
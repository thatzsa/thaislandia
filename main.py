import pygame
import sys
from constantes import * # Certifique-se que constantes.py existe

# Assumindo que os arquivos estão na mesma pasta ou ajustados os imports
from brinquedos.brinquedo import Brinquedo
from brinquedos.tiroaoalvo import MinijogoTiroAoAlvo
from brinquedos.montanharussa import MinijogoMontanhaRussa
from brinquedos.rodagigante import MinijogoRodaGigante
from brinquedos.giftshop import GiftShop
from jogador import Jogador
from personagem import TelaCustomizacao

def rodar_jogo():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Thaislandia - v0.2")
    relogio = pygame.time.Clock()
    
    jogador = Jogador()
    
    # Inicializa estado
    if jogador.primeira_vez:
        estado_atual = "CUSTOMIZACAO"
    else:
        estado_atual = "MENU"
        
    camera_x = 0
    
    # Objetos do Mapa
    brinquedos = [
        Brinquedo("Montanha Russa", 200, 250, 150, 100),
        Brinquedo("Roda Gigante", 500, 250, 150, 100),
        Brinquedo("Gift Shop", 800, 250, 150, 100),
        Brinquedo("Tiro ao Alvo", 1100, 250, 150, 100),
    ]
    
    # Instâncias dos Minijogos (Carregadas uma vez para persistir estado, ou recriadas se preferir reiniciar sempre)
    jogo_tiro = MinijogoTiroAoAlvo(LARGURA, ALTURA)
    jogo_montanha = MinijogoMontanhaRussa(LARGURA, ALTURA)
    jogo_roda = MinijogoRodaGigante(LARGURA, ALTURA)
    loja = GiftShop(LARGURA, ALTURA, jogador)
    tela_custom = TelaCustomizacao(LARGURA, ALTURA, jogador.personagem)
    
    fonte_hud = pygame.font.Font(None, 32)
    
    while True:
        # 1. Captura TODOS os eventos uma única vez
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                jogador.salvar_dados()
                pygame.quit(); sys.exit()

        # 2. Máquina de Estados (Gerenciamento Lógico)
        
        if estado_atual == "CUSTOMIZACAO":
            # Passa eventos para a tela de customização
            if tela_custom.atualizar(eventos):
                jogador.primeira_vez = False
                jogador.salvar_dados()
                estado_atual = "MENU"

        elif estado_atual == "MENU":
            # Lógica do Menu (Movimento Câmera e Cliques)
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]: 
                camera_x = max(0, camera_x - VELOCIDADE_CAMERA)
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]: 
                camera_x = min(LARGURA_MUNDO - LARGURA, camera_x + VELOCIDADE_CAMERA)
            
            # Verifica entrada nos brinquedos
            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    for b in brinquedos:
                        if b.clicou(evento.pos, camera_x):
                            # Transição de estado baseada no nome
                            novo_estado = b.nome.upper().replace(" ", "_")
                            estado_atual = novo_estado
                            
                            # Opcional: Reiniciar o minijogo ao entrar
                            if novo_estado == "TIRO_AO_ALVO":
                                jogo_tiro = MinijogoTiroAoAlvo(LARGURA, ALTURA)
                            elif novo_estado == "MONTANHA_RUSSA":
                                jogo_montanha = MinijogoMontanhaRussa(LARGURA, ALTURA)
                            elif novo_estado == "RODA_GIGANTE":
                                jogo_roda = MinijogoRodaGigante(LARGURA, ALTURA)

        # === ESTADOS DOS MINIJOGOS ===
        # Note como o padrão agora é idêntico para todos
        
        elif estado_atual == "TIRO_AO_ALVO":
            jogo_tiro.atualizar(eventos)
            if jogo_tiro.finalizado:
                jogador.adicionar_pontos("TIRO_AO_ALVO", jogo_tiro.pontuacao)
                estado_atual = "MENU"
                
        elif estado_atual == "GIFT_SHOP":
            loja.atualizar(eventos)
            # A loja usa ESC dentro do atualizar, precisamos checar se o usuário quer sair
            # Sugestão: adicione self.finalizado na loja também, ou verifique ESC aqui:
            for ev in eventos:
                if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
                    estado_atual = "MENU"

        elif estado_atual == "MONTANHA_RUSSA":
            jogo_montanha.atualizar(eventos)
            if jogo_montanha.finalizado:
                jogador.adicionar_pontos("MONTANHA_RUSSA", jogo_montanha.pontuacao)
                estado_atual = "MENU"

        elif estado_atual == "RODA_GIGANTE":
            jogo_roda.atualizar(eventos) # Lembre de atualizar rodagigante.py também!
            if jogo_roda.finalizado:
                jogador.adicionar_pontos("RODA_GIGANTE", jogo_roda.pontuacao)
                estado_atual = "MENU"

        # 3. Renderização
        tela.fill(PRETO)
        
        if estado_atual == "CUSTOMIZACAO":
            tela_custom.desenhar(tela)
        elif estado_atual == "MENU":
            tela.fill(VERDE_PARQUE) # Fundo do parque
            for b in brinquedos: 
                b.desenhar(tela, camera_x)
            desenhar_hud_jogador(tela, jogador, fonte_hud)
        elif estado_atual == "TIRO_AO_ALVO":
            jogo_tiro.desenhar(tela)
        elif estado_atual == "GIFT_SHOP":
            loja.desenhar(tela)
        elif estado_atual == "MONTANHA_RUSSA":
            jogo_montanha.desenhar(tela)
        elif estado_atual == "RODA_GIGANTE":
            jogo_roda.desenhar(tela)

        pygame.display.flip()
        relogio.tick(FPS)

def desenhar_hud_jogador(tela, jogador, fonte):
    # 1. Configurações de layout
    largura_hud = 280
    altura_hud = 90
    margem = 10
    x_hud = LARGURA - largura_hud - margem
    y_hud = margem
    
    # 2. Desenha o Fundo da caixa
    cor_fundo = (40, 40, 60) # Azul escuro acinzentado
    pygame.draw.rect(tela, cor_fundo, (x_hud, y_hud, largura_hud, altura_hud), border_radius=15)
    pygame.draw.rect(tela, BRANCO, (x_hud, y_hud, largura_hud, altura_hud), 2, border_radius=15)
    
    # 3. Área do Avatar (Truque do Clipping)
    # Salvamos a área de desenho atual
    area_original = tela.get_clip()
    # Definimos que só pode desenhar DENTRO da caixa do HUD
    tela.set_clip(pygame.Rect(x_hud, y_hud, largura_hud, altura_hud))
    
    # Posição do boneco (Lado direito)
    centro_avatar_x = x_hud + largura_hud - 50
    centro_avatar_y = y_hud + 55 # Empurrei um pouco pra baixo pra aparecer só o busto
    
    # Círculo de destaque atrás do boneco
    pygame.draw.circle(tela, (70, 70, 90), (centro_avatar_x, centro_avatar_y - 25), 35)
    
    # Desenha o boneco (escala 0.8 fica bom)
    jogador.personagem.desenhar(tela, centro_avatar_x, centro_avatar_y, 0.8)
    
    # Removemos o limite de desenho (restaura o normal)
    tela.set_clip(area_original)
    
    # 4. Textos (Lado esquerdo)
    # Fonte menor para os títulos
    fonte_lbl = pygame.font.SysFont("arial", 14)
    # Fonte maior para os números
    fonte_val = pygame.font.SysFont("arial", 24, bold=True)
    
    # Coluna 1: Pontos
    tela.blit(fonte_lbl.render("PONTOS", True, (200, 200, 200)), (x_hud + 20, y_hud + 15))
    tela.blit(fonte_val.render(f"{jogador.pontos_totais}", True, AMARELO), (x_hud + 20, y_hud + 35))
    
    # Coluna 2: Nível (um pouco mais para a direita)
    tela.blit(fonte_lbl.render("NÍVEL", True, (200, 200, 200)), (x_hud + 120, y_hud + 15))
    tela.blit(fonte_val.render(f"{jogador.obter_nivel()}", True, BRANCO), (x_hud + 120, y_hud + 35))

if __name__ == "__main__":
    rodar_jogo()
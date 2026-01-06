import pygame

class Personagem:
    CORES_PELE = {
        "clara": (255, 220, 177), "media": (210, 180, 140),
        "morena": (180, 140, 100), "escura": (139, 90, 60), "negra": (80, 50, 30)
    }
    CORES_CABELO = {
        "loiro": (255, 220, 100), "castanho": (101, 67, 33),
        "preto": (40, 40, 40), "ruivo": (180, 70, 40),
        "branco": (230, 230, 230), "colorido": (200, 100, 255)
    }
    ESTILOS_CABELO = {
        "curto": "curto", "medio": "medio",
        "longo": "longo", "careca": "careca"
    }
    CORES_ROUPA = {
        "vermelho": (220, 50, 50), "azul": (50, 100, 220),
        "verde": (50, 200, 50), "amarelo": (255, 220, 50),
        "roxo": (150, 50, 200), "preto": (40, 40, 40),
        "branco": (240, 240, 240), "marrom": (120, 80, 50)
    }

    def __init__(self):
        self.nome_cor_pele = "media"
        self.nome_cor_cabelo = "castanho"
        self.estilo_cabelo = "curto"
        self.nome_cor_camiseta = "azul"
        self.nome_cor_calca = "preto"

        self.cor_pele = self.CORES_PELE[self.nome_cor_pele]
        self.cor_cabelo = self.CORES_CABELO[self.nome_cor_cabelo]
        self.cor_camiseta = self.CORES_ROUPA[self.nome_cor_camiseta]
        self.cor_calca = self.CORES_ROUPA[self.nome_cor_calca]

    def aplicar_personalizacao(self, pele, cabelo, estilo, camiseta, calca):
        self.nome_cor_pele = pele
        self.nome_cor_cabelo = cabelo
        self.estilo_cabelo = estilo
        self.nome_cor_camiseta = camiseta
        self.nome_cor_calca = calca

        self.cor_pele = self.CORES_PELE[pele]
        self.cor_cabelo = self.CORES_CABELO[cabelo]
        self.cor_camiseta = self.CORES_ROUPA[camiseta]
        self.cor_calca = self.CORES_ROUPA[calca]

    def desenhar(self, tela, x, y, escala=1.0):
        s = escala
        centro_x = int(x)
        centro_y = int(y)

        # 1. CABELO DE TRÁS (Desenha antes para ficar no fundo)
        self.desenhar_cabelo_tras(tela, centro_x, centro_y, s)

        # 2. CORPO
        # Calça
        pygame.draw.rect(tela, self.cor_calca, (centro_x - 12*s, centro_y + 12*s, 24*s, 22*s), border_radius=int(4*s))
        # Camiseta
        pygame.draw.rect(tela, self.cor_camiseta, (centro_x - 14*s, centro_y - 8*s, 28*s, 24*s), border_radius=int(5*s))

        # 3. CABEÇA
        # Círculo do rosto
        pygame.draw.circle(tela, self.cor_pele, (centro_x, int(centro_y - 18*s)), int(16*s))

        # 4. OLHOS (Agora desenhados como ovais verticais para estilo "chibi")
        cor_olhos = (20, 20, 20)
        olho_y = int(centro_y - 20*s) # Altura dos olhos
        
        # Olho Esquerdo
        pygame.draw.ellipse(tela, cor_olhos, (centro_x - 9*s, olho_y, 5*s, 7*s))
        # Olho Direito
        pygame.draw.ellipse(tela, cor_olhos, (centro_x + 4*s, olho_y, 5*s, 7*s))

        # 5. CABELO DA FRENTE (Franja e Topo)
        self.desenhar_cabelo_frente(tela, centro_x, centro_y, s)

    def desenhar_cabelo_tras(self, tela, x, y, s):
        if self.estilo_cabelo == "careca":
            return
        
        topo_y = y - 30*s 
        if self.estilo_cabelo == "longo":
            # Cabelo comprido atrás das costas
            pygame.draw.rect(tela, self.cor_cabelo, (x - 22*s, topo_y, 44*s, 65*s), border_radius=int(10*s))
        elif self.estilo_cabelo == "medio":
            # Cabelo médio
            pygame.draw.rect(tela, self.cor_cabelo, (x - 20*s, topo_y, 40*s, 45*s), border_radius=int(10*s))

    def desenhar_cabelo_frente(self, tela, x, y, s):
        if self.estilo_cabelo == "careca":
            return
        
        # Topo da cabeça (Reduzi a altura para não descer na testa)
        # y-44 sobe o topo, altura 18 garante que pare na testa (-26), longe dos olhos (-20)
        topo_rect = pygame.Rect(x - 17*s, y - 44*s, 34*s, 18*s) 
        pygame.draw.ellipse(tela, self.cor_cabelo, topo_rect)

        if self.estilo_cabelo == "curto":
            # Costeletas curtas
            pygame.draw.rect(tela, self.cor_cabelo, (x - 19*s, y - 30*s, 4*s, 14*s), border_radius=int(2*s))
            pygame.draw.rect(tela, self.cor_cabelo, (x + 15*s, y - 30*s, 4*s, 14*s), border_radius=int(2*s))
            # Franjinha pequena no topo
            pygame.draw.rect(tela, self.cor_cabelo, (x - 6*s, y - 38*s, 12*s, 6*s), border_radius=int(2*s))
            
        elif self.estilo_cabelo in ["medio", "longo"]:
            # Laterais (mais afastadas para não cobrir o rosto)
            # Lado Esquerdo
            pygame.draw.rect(tela, self.cor_cabelo, (x - 22*s, y - 32*s, 8*s, 35*s), border_radius=int(4*s))
            # Lado Direito
            pygame.draw.rect(tela, self.cor_cabelo, (x + 14*s, y - 32*s, 8*s, 35*s), border_radius=int(4*s))
            
            # FRANJA "CORTINA" (Aberta no meio para ver os olhos)
            # Ao invés de um retângulo no meio, fazemos dois menores nas laterais da testa
            
            # Mecha Esquerda
            pygame.draw.rect(tela, self.cor_cabelo, (x - 15*s, y - 38*s, 11*s, 12*s), border_radius=int(3*s))
            # Mecha Direita
            pygame.draw.rect(tela, self.cor_cabelo, (x + 4*s, y - 38*s, 11*s, 12*s), border_radius=int(3*s))

class TelaCustomizacao:
    def __init__(self, largura, altura, personagem):
        self.largura = largura
        self.altura = altura
        self.personagem = personagem

        self.cores_pele_lista = list(Personagem.CORES_PELE.keys())
        self.cores_cabelo_lista = list(Personagem.CORES_CABELO.keys())
        self.estilos_cabelo_lista = list(Personagem.ESTILOS_CABELO.keys())
        self.cores_camiseta_lista = list(Personagem.CORES_ROUPA.keys())
        self.cores_calca_lista = list(Personagem.CORES_ROUPA.keys())

        self.indice_pele = self.cores_pele_lista.index(personagem.nome_cor_pele)
        self.indice_cabelo = self.cores_cabelo_lista.index(personagem.nome_cor_cabelo)
        self.indice_estilo_cabelo = self.estilos_cabelo_lista.index(personagem.estilo_cabelo)
        self.indice_camiseta = self.cores_camiseta_lista.index(personagem.nome_cor_camiseta)
        self.indice_calca = self.cores_calca_lista.index(personagem.nome_cor_calca)

        self.primeira_vez = False
        self.fonte_t = pygame.font.Font(None, 50)
        self.fonte_m = pygame.font.Font(None, 28)

        self.fundo = pygame.Surface((largura, altura))
        for y in range(altura):
            r = min(255, 100 + y // 6)
            g = min(255, 150 + y // 8)
            b = min(255, 200 + y // 10)
            pygame.draw.line(self.fundo, (r, g, b), (0, y), (largura, y))

    def atualizar(self, eventos):
        for ev in eventos:
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_1:
                    self.indice_pele = (self.indice_pele + 1) % len(self.cores_pele_lista)
                elif ev.key == pygame.K_2:
                    self.indice_cabelo = (self.indice_cabelo + 1) % len(self.cores_cabelo_lista)
                elif ev.key == pygame.K_3:
                    self.indice_estilo_cabelo = (self.indice_estilo_cabelo + 1) % len(self.estilos_cabelo_lista)
                elif ev.key == pygame.K_4:
                    self.indice_camiseta = (self.indice_camiseta + 1) % len(self.cores_camiseta_lista)
                elif ev.key == pygame.K_5:
                    self.indice_calca = (self.indice_calca + 1) % len(self.cores_calca_lista)
                elif ev.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return True

                self.aplicar()
        return False

    def aplicar(self):
        self.personagem.aplicar_personalizacao(
            self.cores_pele_lista[self.indice_pele],
            self.cores_cabelo_lista[self.indice_cabelo],
            self.estilos_cabelo_lista[self.indice_estilo_cabelo],
            self.cores_camiseta_lista[self.indice_camiseta],
            self.cores_calca_lista[self.indice_calca]
        )

    def desenhar(self, tela):
        tela.blit(self.fundo, (0, 0))

        titulo = "BEM-VINDO!" if self.primeira_vez else "CUSTOMIZE SEU PERSONAGEM"
        img = self.fonte_t.render(titulo, True, (255, 255, 255))
        tela.blit(img, (self.largura // 2 - img.get_width() // 2, 30))

        # Aumentei a escala para 3.5 para ficar bem visível no centro
        self.personagem.desenhar(tela, self.largura // 2, 300, 3.5)

        opcoes = [
            f"1. Pele: {self.cores_pele_lista[self.indice_pele]}",
            f"2. Cabelo: {self.cores_cabelo_lista[self.indice_cabelo]}",
            f"3. Estilo: {self.estilos_cabelo_lista[self.indice_estilo_cabelo]}",
            f"4. Camiseta: {self.cores_camiseta_lista[self.indice_camiseta]}",
            f"5. Calça: {self.cores_calca_lista[self.indice_calca]}"
        ]

        for i, texto in enumerate(opcoes):
            tela.blit(
                self.fonte_m.render(texto, True, (255, 255, 255)),
                (50, 150 + i * 40)
            )

        msg = self.fonte_m.render("ESPACO para confirmar", True, (100, 255, 100))
        tela.blit(msg, (self.largura // 2 - msg.get_width() // 2, self.altura - 50))
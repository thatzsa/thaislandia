import pygame

class Item:
    """Representa um item da loja"""
    
    def __init__(self, nome, descricao, preco, categoria, emoji="🎁"):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.categoria = categoria  # "roupa", "acessorio", "decoracao", "especial"
        self.comprado = False
        self.emoji = emoji

class GiftShop:
    """Loja do parque"""
    
    def __init__(self, largura, altura, jogador):
        self.largura = largura
        self.altura = altura
        self.jogador = jogador
        
        # Itens disponíveis na loja
        self.itens = [
            # ROUPAS
            Item("Camiseta Thaislandia", "Camiseta oficial do parque", 100, "roupa", "👕"),
            Item("Bone com Logo", "Bone estiloso do parque", 150, "roupa", "🧢"),
            Item("Moletom Premium", "Moletom quentinho", 300, "roupa", "🧥"),
            Item("Sapato Confortavel", "Para andar o dia todo", 250, "roupa", "👟"),
            
            # ACESSÓRIOS
            Item("Oculos de Sol", "Proteja seus olhos com estilo", 200, "acessorio", "🕶️"),
            Item("Mochila do Parque", "Carregue suas coisas", 180, "acessorio", "🎒"),
            Item("Relogio Digital", "Nunca perca a hora", 350, "acessorio", "⌚"),
            Item("Chaveiro Especial", "Lembranca do parque", 50, "acessorio", "🔑"),
            
            # DECORAÇÃO/COLECIONÁVEIS
            Item("Caneca Personalizada", "Tome cafe com estilo", 120, "decoracao", "☕"),
            Item("Poster do Parque", "Decore sua parede", 80, "decoracao", "🖼️"),
            Item("Miniatura Roda Gigante", "Replica em miniatura", 280, "decoracao", "🎡"),
            Item("Pelucia Mascote", "Fofinho demais!", 220, "decoracao", "🧸"),
            
            # ESPECIAIS (mais caros)
            Item("Ingresso VIP Anual", "Acesso ilimitado por 1 ano", 1000, "especial", "🎫"),
            Item("Foto com Mascote", "Sessao de fotos exclusiva", 400, "especial", "📸"),
            Item("Fast Pass Ouro", "Fure todas as filas", 800, "especial", "⚡"),
            Item("Troféu Campeao", "Prova de sua maestria", 1500, "especial", "🏆"),
        ]
        
        # Carregar itens comprados do jogador
        self.carregar_compras()
        
        # Interface
        self.scroll_y = 0
        self.item_selecionado = None
        self.item_hover = None
        
        # Categorias
        self.categorias = ["todas", "roupa", "acessorio", "decoracao", "especial"]
        self.categoria_selecionada = "todas"
        self.categoria_hover = None
        
        # Feedback de compra
        self.mensagem_feedback = ""
        self.feedback_timer = 0
        self.feedback_cor = (255, 255, 255)
        
        # Fontes
        self.fonte_titulo = pygame.font.SysFont("monospace", 36, bold=True)
        self.fonte_grande = pygame.font.SysFont("monospace", 28, bold=True)
        self.fonte_media = pygame.font.SysFont("monospace", 22, bold=True)
        self.fonte_pequena = pygame.font.SysFont("monospace", 18)
    
    def carregar_compras(self):
        """Carrega os itens já comprados pelo jogador"""
        if hasattr(self.jogador, 'itens_comprados'):
            for item in self.itens:
                if item.nome in self.jogador.itens_comprados:
                    item.comprado = True
        else:
            # Adiciona atributo ao jogador se não existir
            self.jogador.itens_comprados = []
    
    def salvar_compra(self, item):
        """Salva um item comprado no perfil do jogador"""
        if not hasattr(self.jogador, 'itens_comprados'):
            self.jogador.itens_comprados = []
        
        if item.nome not in self.jogador.itens_comprados:
            self.jogador.itens_comprados.append(item.nome)
            self.jogador.salvar_dados()
    
    def comprar_item(self, item):
        """Tenta comprar um item"""
        if item.comprado:
            self.mensagem_feedback = "Voce ja possui este item!"
            self.feedback_cor = (255, 150, 0)
            self.feedback_timer = 90
            return False
        
        if self.jogador.pontos_totais >= item.preco:
            # Deduz pontos
            self.jogador.pontos_totais -= item.preco
            item.comprado = True
            
            # Salva compra
            self.salvar_compra(item)
            self.jogador.salvar_dados()
            
            # Feedback positivo
            self.mensagem_feedback = f"Comprou: {item.nome}!"
            self.feedback_cor = (100, 255, 100)
            self.feedback_timer = 90
            
            print(f"[LOJA] Comprou {item.nome} por {item.preco} pontos")
            return True
        else:
            # Não tem pontos suficientes
            faltam = item.preco - self.jogador.pontos_totais
            self.mensagem_feedback = f"Faltam {faltam} pontos!"
            self.feedback_cor = (255, 100, 100)
            self.feedback_timer = 90
            return False
    
    def obter_itens_filtrados(self):
        """Retorna itens baseado na categoria selecionada"""
        if self.categoria_selecionada == "todas":
            return self.itens
        else:
            return [item for item in self.itens if item.categoria == self.categoria_selecionada]
    
    def atualizar(self, eventos):
        """Atualiza a loja"""
        # Atualiza feedback
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
        
        mouse_pos = pygame.mouse.get_pos()
        
        for evento in eventos:
            # Scroll com mouse wheel
            if evento.type == pygame.MOUSEWHEEL:
                self.scroll_y -= evento.y * 30
                self.scroll_y = max(0, min(self.scroll_y, max(0, len(self.obter_itens_filtrados()) * 120 - 400)))
            
            # Cliques
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Verifica clique nas categorias
                for i, categoria in enumerate(self.categorias):
                    cat_x = 20 + i * 150
                    cat_y = 80
                    cat_rect = pygame.Rect(cat_x, cat_y, 140, 40)
                    
                    if cat_rect.collidepoint(mouse_pos):
                        self.categoria_selecionada = categoria
                        self.scroll_y = 0
                        print(f"[LOJA] Categoria: {categoria}")
                
                # Verifica clique nos itens
                itens_filtrados = self.obter_itens_filtrados()
                for i, item in enumerate(itens_filtrados):
                    item_y = 150 + i * 120 - self.scroll_y
                    
                    if 150 <= item_y <= self.altura - 100:
                        # Botão de compra
                        botao_x = self.largura - 180
                        botao_y = item_y + 35
                        botao_rect = pygame.Rect(botao_x, botao_y, 150, 40)
                        
                        if botao_rect.collidepoint(mouse_pos):
                            self.comprar_item(item)
        
        # Atualiza hover
        self.item_hover = None
        self.categoria_hover = None
        
        # Hover nas categorias
        for i, categoria in enumerate(self.categorias):
            cat_x = 20 + i * 150
            cat_y = 80
            cat_rect = pygame.Rect(cat_x, cat_y, 140, 40)
            if cat_rect.collidepoint(mouse_pos):
                self.categoria_hover = categoria
        
        # Hover nos itens
        itens_filtrados = self.obter_itens_filtrados()
        for i, item in enumerate(itens_filtrados):
            item_y = 150 + i * 120 - self.scroll_y
            if 150 <= item_y <= self.altura - 100:
                item_rect = pygame.Rect(20, item_y, self.largura - 40, 100)
                if item_rect.collidepoint(mouse_pos):
                    self.item_hover = item
    
    def desenhar(self, tela):
        """Desenha a interface da loja"""
        # Fundo
        tela.fill((240, 230, 220))
        
        # Header
        header = pygame.Surface((self.largura, 70))
        header.fill((139, 90, 60))
        tela.blit(header, (0, 0))
        
        # Título
        titulo = self.fonte_titulo.render("GIFT SHOP", True, (255, 255, 255))
        tela.blit(titulo, (20, 15))
        
        # Saldo do jogador
        saldo_texto = self.fonte_media.render(f"Saldo: {self.jogador.pontos_totais} pts", True, (255, 215, 0))
        tela.blit(saldo_texto, (self.largura - 250, 20))
        
        # Abas de categorias
        for i, categoria in enumerate(self.categorias):
            cat_x = 20 + i * 150
            cat_y = 80
            cat_largura = 140
            cat_altura = 40
            
            # Cor da aba
            if categoria == self.categoria_selecionada:
                cor_fundo = (100, 60, 40)
            elif categoria == self.categoria_hover:
                cor_fundo = (120, 80, 60)
            else:
                cor_fundo = (139, 90, 60)
            
            pygame.draw.rect(tela, cor_fundo, (cat_x, cat_y, cat_largura, cat_altura), border_radius=5)
            pygame.draw.rect(tela, (80, 50, 30), (cat_x, cat_y, cat_largura, cat_altura), 2, border_radius=5)
            
            # Texto da categoria
            cat_nome = categoria.upper()
            texto_cat = self.fonte_pequena.render(cat_nome, True, (255, 255, 255))
            texto_rect = texto_cat.get_rect(center=(cat_x + cat_largura // 2, cat_y + cat_altura // 2))
            tela.blit(texto_cat, texto_rect)
        
        # Área de itens (com scroll)
        itens_filtrados = self.obter_itens_filtrados()
        
        # Área de clipping (para esconder itens fora da tela)
        area_itens = pygame.Rect(0, 140, self.largura, self.altura - 240)
        tela.set_clip(area_itens)
        
        for i, item in enumerate(itens_filtrados):
            item_y = 150 + i * 120 - self.scroll_y
            
            # Só desenha se estiver visível
            if item_y < -100 or item_y > self.altura:
                continue
            
            self.desenhar_item(tela, item, 20, item_y)
        
        tela.set_clip(None)
        
        # Barra de rolagem (se necessário)
        if len(itens_filtrados) * 120 > self.altura - 240:
            scroll_altura = max(50, (self.altura - 240) * (self.altura - 240) / (len(itens_filtrados) * 120))
            scroll_y_pos = 140 + (self.scroll_y / (len(itens_filtrados) * 120)) * (self.altura - 240)
            pygame.draw.rect(tela, (100, 100, 100), (self.largura - 15, scroll_y_pos, 10, scroll_altura), border_radius=5)
        
        # Footer com instruções
        footer = pygame.Surface((self.largura, 80))
        footer.set_alpha(230)
        footer.fill((139, 90, 60))
        tela.blit(footer, (0, self.altura - 80))
        
        instrucao = self.fonte_pequena.render("Clique para comprar | Mouse Wheel para rolar | ESC para sair", True, (255, 255, 255))
        tela.blit(instrucao, (20, self.altura - 60))
        
        # Estatísticas
        total_itens = len(self.itens)
        itens_comprados = sum(1 for item in self.itens if item.comprado)
        stats = self.fonte_pequena.render(f"Colecao: {itens_comprados}/{total_itens} itens", True, (255, 255, 255))
        tela.blit(stats, (20, self.altura - 35))
        
        # Mensagem de feedback
        if self.feedback_timer > 0:
            alpha = min(255, self.feedback_timer * 3)
            feedback_surface = self.fonte_grande.render(self.mensagem_feedback, True, self.feedback_cor)
            feedback_rect = feedback_surface.get_rect(center=(self.largura // 2, 200))
            
            # Sombra
            sombra = self.fonte_grande.render(self.mensagem_feedback, True, (0, 0, 0))
            sombra_rect = sombra.get_rect(center=(self.largura // 2 + 2, 202))
            tela.blit(sombra, sombra_rect)
            
            tela.blit(feedback_surface, feedback_rect)
    
    def desenhar_item(self, tela, item, x, y):
        """Desenha um item individual"""
        largura = self.largura - 40
        altura = 100
        
        # Fundo do card
        if item == self.item_hover:
            cor_fundo = (255, 250, 240)
        else:
            cor_fundo = (255, 255, 255)
        
        pygame.draw.rect(tela, cor_fundo, (x, y, largura, altura), border_radius=10)
        
        # Borda (diferente se já comprado)
        if item.comprado:
            cor_borda = (100, 200, 100)
            espessura = 4
        else:
            cor_borda = (139, 90, 60)
            espessura = 2
        
        pygame.draw.rect(tela, cor_borda, (x, y, largura, altura), espessura, border_radius=10)
        
        # Emoji/ícone
        emoji_texto = self.fonte_titulo.render(item.emoji, True, (0, 0, 0))
        tela.blit(emoji_texto, (x + 15, y + 25))
        
        # Nome do item
        nome = self.fonte_media.render(item.nome, True, (40, 40, 40))
        tela.blit(nome, (x + 80, y + 15))
        
        # Descrição
        descricao = self.fonte_pequena.render(item.descricao, True, (100, 100, 100))
        tela.blit(descricao, (x + 80, y + 45))
        
        # Preço e botão
        preco_texto = self.fonte_media.render(f"{item.preco} pts", True, (200, 150, 0))
        tela.blit(preco_texto, (x + 80, y + 70))
        
        # Botão de compra
        botao_x = x + largura - 160
        botao_y = y + 35
        botao_largura = 150
        botao_altura = 40
        
        if item.comprado:
            # Item já comprado
            cor_botao = (100, 200, 100)
            texto_botao = "COMPRADO ✓"
        elif self.jogador.pontos_totais >= item.preco:
            # Pode comprar
            cor_botao = (100, 180, 255)
            texto_botao = "COMPRAR"
        else:
            # Não pode comprar
            cor_botao = (150, 150, 150)
            texto_botao = "SEM PONTOS"
        
        pygame.draw.rect(tela, cor_botao, (botao_x, botao_y, botao_largura, botao_altura), border_radius=5)
        pygame.draw.rect(tela, (0, 0, 0), (botao_x, botao_y, botao_largura, botao_altura), 2, border_radius=5)
        
        texto = self.fonte_pequena.render(texto_botao, True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(botao_x + botao_largura // 2, botao_y + botao_altura // 2))
        tela.blit(texto, texto_rect)
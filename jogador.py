import json
import os
from personagem import Personagem 

class Jogador:
    """Classe para gerenciar dados do jogador"""
    
    def __init__(self):
        self.pontos_totais = 0
        self.historico_jogos = {
            "TIRO_AO_ALVO": {"jogadas": 0, "melhor_pontuacao": 0, "pontos_totais": 0},
            "MONTANHA_RUSSA": {"jogadas": 0, "melhor_pontuacao": 0, "pontos_totais": 0},
            "RODA_GIGANTE": {"jogadas": 0, "melhor_pontuacao": 0, "pontos_totais": 0}
        }
        self.itens_comprados = []  
        self.personagem = Personagem()
        self.carregar_dados()
    
    def adicionar_pontos(self, jogo, pontos):
        """
        Adiciona pontos de um jogo específico
        
        Args:
            jogo (str): Nome do jogo ("TIRO_AO_ALVO", "MONTANHA_RUSSA", etc)
            pontos (int): Pontos obtidos nessa partida
        """
        if jogo in self.historico_jogos:
            # Atualiza estatísticas do jogo específico
            self.historico_jogos[jogo]["jogadas"] += 1
            self.historico_jogos[jogo]["pontos_totais"] += pontos
            
            # Atualiza melhor pontuação se necessário
            if pontos > self.historico_jogos[jogo]["melhor_pontuacao"]:
                self.historico_jogos[jogo]["melhor_pontuacao"] = pontos
            
            # Adiciona aos pontos totais globais
            self.pontos_totais += pontos
            
            # Salva automaticamente
            self.salvar_dados()
            
            print(f"[JOGADOR] +{pontos} pontos de {jogo}")
            print(f"[JOGADOR] Total global: {self.pontos_totais} pontos")
    
    def obter_estatisticas(self, jogo=None):
        """
        Retorna estatísticas do jogador
        
        Args:
            jogo (str, optional): Nome do jogo específico. Se None, retorna estatísticas globais
        
        Returns:
            dict: Dicionário com estatísticas
        """
        if jogo:
            return self.historico_jogos.get(jogo, {})
        else:
            return {
                "pontos_totais": self.pontos_totais,
                "jogos": self.historico_jogos,
                "total_jogadas": sum(j["jogadas"] for j in self.historico_jogos.values())
            }
    
    def salvar_dados(self):
        """Salva os dados do jogador em um arquivo JSON"""
        try:
            dados = {
                "pontos_totais": self.pontos_totais,
                "historico_jogos": self.historico_jogos,
                "itens_comprados": self.itens_comprados,
                "personagem": self.personagem.para_dicionario(),
                "primeira_vez": False  # Depois da primeira vez, sempre False
            }
            
            with open("dados_jogador.json", "w") as arquivo:
                json.dump(dados, arquivo, indent=4)
            
            print("[JOGADOR] Dados salvos com sucesso!")
        except Exception as e:
            print(f"[JOGADOR] Erro ao salvar dados: {e}")
    
    def carregar_dados(self):
        """Carrega os dados do jogador de um arquivo JSON"""
        try:
            if os.path.exists("dados_jogador.json"):
                with open("dados_jogador.json", "r") as arquivo:
                    dados = json.load(arquivo)
                
                self.pontos_totais = dados.get("pontos_totais", 0)
                self.itens_comprados = dados.get("itens_comprados", [])
                self.primeira_vez = dados.get("primeira_vez", False)
                
                # Carrega personagem
                if "personagem" in dados:
                    self.personagem.carregar_de_dicionario(dados["personagem"])
                
                # Atualiza histórico
                historico_carregado = dados.get("historico_jogos", {})
                for jogo in self.historico_jogos.keys():
                    if jogo in historico_carregado:
                        self.historico_jogos[jogo] = historico_carregado[jogo]
                
                print(f"[JOGADOR] Dados carregados! Pontos totais: {self.pontos_totais}")
                print(f"[JOGADOR] Itens comprados: {len(self.itens_comprados)}")
            else:
                print("[JOGADOR] Nenhum save encontrado, iniciando novo jogador")
                self.primeira_vez = True
        except Exception as e:
            print(f"[JOGADOR] Erro ao carregar dados: {e}")
            self.primeira_vez = True
    
    def resetar_dados(self):
        """Reseta todos os dados do jogador (novo jogo)"""
        self.pontos_totais = 0
        self.itens_comprados = []
        for jogo in self.historico_jogos:
            self.historico_jogos[jogo] = {
                "jogadas": 0,
                "melhor_pontuacao": 0,
                "pontos_totais": 0
            }
        self.salvar_dados()
        print("[JOGADOR] Dados resetados!")
    
    def obter_nivel(self):
        """Calcula o nível do jogador baseado nos pontos totais"""
        # A cada 1000 pontos = 1 nível
        return self.pontos_totais // 1000 + 1
    
    def pontos_para_proximo_nivel(self):
        """Calcula quantos pontos faltam para o próximo nível"""
        nivel_atual = self.obter_nivel()
        pontos_necessarios = nivel_atual * 1000
        return pontos_necessarios - self.pontos_totais
    
    def obter_titulo(self):
        """Retorna um título baseado no nível do jogador"""
        nivel = self.obter_nivel()
        
        if nivel < 5:
            return "Visitante Novato"
        elif nivel < 10:
            return "Aventureiro"
        elif nivel < 20:
            return "Explorador Corajoso"
        elif nivel < 30:
            return "Mestre dos Brinquedos"
        elif nivel < 50:
            return "Lenda do Parque"
        else:
            return "Imperador da Thaislandia"
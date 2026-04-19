#importando bibliotecas externas
import random

class Tabuleiro:
	#iniciar classe
	def __init__(self) -> None:
		self.tab = [["-" for _ in range(0,9)] for _ in range(0,9)]
	
	#para recomecar o tabuleiro	
	def resetar(self) -> None:
		for i in range (0,9):
			for j in range (0,9):
				self.tab[i][j] = "-"
	
	#mostrar o proprio tabuleiro			
	def mostrar(self) -> None:
		print("\nSeu tabuleiro:")
		for coluna in range (0,9):
				for linha in range (0,9):
					print(self.tab[linha][coluna], end=" ")
				print(end="\n")
			
	#mostrar o tabuleiro do oponente
	def mostrarop(self) -> None:
		print("\nTabuleiro da máquina:")
		for coluna in range (0,9):
		  	for linha in range (0,9):
		  		if self.tab[linha][coluna] == "N":
		  			print("-", end=" ")
		  		else:
		  			print(self.tab[linha][coluna], end=" ") 
		  	print(end="\n")
		  	
	#ataca o tabuleiro
	def atacar(self, linha: int, coluna: int) -> bool | None:
	    if self.tab[linha][coluna] == "-":
	    	print("Pfff. Errou!")
	    	self.tab[linha][coluna] = "E"
	    	return False
	    elif self.tab[linha][coluna] == "N":
	    	print("Boom! Acertou!")
	    	self.tab[linha][coluna] = "A"
	    	return True
	    else:
	    	print("Essa coordenada já foi atacada. Tente novamente.")
	    	return None

	#colocar a pecas. retorna true se conseguiu. retorna false se já tinha um navio lá
	def posicionar(self, pecas: Pecas)-> bool:
		for i in range(0, len(pecas)):
			linha, coluna = pecas[i]
			if self.tab[linha][coluna] == "N":
				print("Casas já ocupadas. Tente novamente.")
				return False
		self.tab[linha][coluna] = "N"
		return True
	   	
	   
	
	    

class Pecas:
	#inicia a classe
	def __init__(self, tamanho: int, nome: str, dono: Jogador, tab: Tabuleiro) -> None:
		self.tamanho = tamanho
		self.nome = nome
		self.dono = dono
		for linha in range (0, tamanho-1):
				self.posicao[linha] = [-1, -1]
				
	def posicionar(self, posicoes: list[tuple[int]], tab: Tabuleiro) -> None:
		pass
	
				
class Jogador:
		def __init__(self, nome: str) -> None:
			self.nome = nome
			self.ataque = None
			self.vitorias = 0
			self.partidas = 0
			self.acertosPartidas = 0

		#pega do usuario as coordenadas que ele quer atacar, verifica se o usuario passou int
		def atacar(self, toponente: Tabuleiro) -> None:
			while self.ataque == None:
				linha = input("Qual linha você deseja atacar?")
				coluna = input("Qual coluna você deseja atacar?")			
				try:
					linha = int(linha) -1
					coluna = int(coluna) -1
				except:
					print("Algo deu errado. Insira um número entre 1 e 10.")
					self.atacar(toponente)
					return  
				if not(0<=linha<=9) or not(0<=coluna<=9):
					print("Insira um número entre 1 e 10.")
					self.atacar(toponente)
					return
				self.ataque = toponente.atacar(linha, coluna)
			if self.ataque:
				self.acertosPartidas += 1
			self.ataque = None
		
		#pega as coordenadas que ele deseja colocar o navio
		def posicao(self, peca: Pecas) -> None:
			nome = input(f"Dê  um nome para o seu navio de {peca.tamanho}.")
			peca.nome = nome
			verticalOuHorizontal = input("Você quer colocar a sua primeira peca na horizontal ou na vertical?")
			verticalOuHorizontal = verticalOuHorizontal.lower()
			if verticalOuHorizontal == "vertical" or verticalOuHorizontal == "v":
				pass
			elif verticalOuHorizontal == "horizontal" or verticalOuHorizontal == "h":
				pass
			else:
				print("ERRO! Não foi digitado horizontal ou vertical. Tente de novo colocar essa peca de {peca.tamanho} casas de tamanho.")
				self.posicao(peca)
			
		
class Maquina(Jogador):
		#escolhe as posicoes que as pecas da maquina serao colocadas
		def colocarPecas(self, tamanho: int) -> list[tuple[int]]:
			#sorteio para ver se o navio ficará na horizontal ou vertical:
			verticalOuHorizontal = random.randint(1,2)
			posicoes = []
			linha = random.randint(0,9)
			coluna = random.randit(0,9)
			for i in range(0, tamanho-1):
				if verticalOuHorizontal == 1:
					if coluna + tamanho <= 9:
						posicoes[i] = [linha, coluna+i]
					else:
						posicoes[i] = [linha, coluna-i]
				else:
					if linha + tamanho <= 9:
						posicoes[i] = [linha+i, coluna]
					else:
						posicoes[i] = [linha-i, coluna]
			return posicoes
			

		#escolhe e realiza o lance da máquina:
		def fazerLance(self, tseu: Tabuleiro) -> None:
			#Se a máquina ainda não acertou um navio, ela atacará casas aleatórias até acertar um navio.
			if self.streakAcerto == 0:
				while self.ataque == None:
					linha = random.randint(0,9)	
					coluna = random.randint(0,9)
					self.ataque = tseu.atacar(linha, coluna)
				if self.ataque:
					self.streakAcerto += 1
					self.acertosPartida += 1
				self.ataque = None
			else:
				#Se a máquina acertou um navio, ela irá tentar explorar horizontalmente e verticalmente os espaços adjacentes por um segundo acerto.
				
				pass
			
class Partida():
	def __init__(self, voce: Jogador, oponente: Maquina):
		self.quantidadeDeJogadas = 0
		self.vencedor = ""
		self.jogador1 = voce
		self.jogador2 = oponente
	
	def iniciarPartida(self, voce: Jogador, oponente: Maquina, tseu: Tabuleiro, toponente: Tabuleiro) -> None:
		voce.acertosPartidas = 0
		oponente.acertosPartida = 0
		oponente.streakAcerto = 0
		voce.ataque = None
		oponente.ataque = None
		tseu.resetar()
		toponente.resetar()
		tseu.mostrar()
		toponente.mostrarop()
		
	def novaRodada(self, voce: Jogador, oponente: Maquina, tseu: Tabuleiro, toponente: Tabuleiro) -> None:
		voce.atacar(toponente)
		toponente.mostrarop()
		oponente.fazerLance(tseu)
		if voce.acertosPartidas == 19 or oponente.acertosPartidas == 19:
			self.fimPartida()
	
	def fimPartida(self):
		if self.jogador1.acertosPartidas == 19:
			self.vencedor = self.jogador1.nome
		else:
			self.vencedor = self.jogador2.nome
		print(self.vencedor)
	

def menu() -> None:
	print("1 - Nova Partida \n2 - Estatisticas")
	resposta = input()
	if resposta == "1":
		nome = input("Qual é o seu nome?")
		tseu = Tabuleiro()
		toponente = Tabuleiro()
		voce = Jogador(nome)
		oponente = Maquina("Maquina")
		partidas.append(Partida(voce, oponente))
		partidas[-1].iniciarPartida(voce, oponente, tseu, toponente)
		partidas[-1].novaRodada(voce, oponente, tseu, toponente)
	elif resposta == "2":
		#algo
		pass
	else:
		print("Resposta Inválida!\n")
		menu()

partidas = []		
menu()














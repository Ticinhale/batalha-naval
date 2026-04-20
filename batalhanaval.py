#importando bibliotecas externas
import random

class Tabuleiro:
	#iniciar classe
	def __init__(self) -> None:
		self.tab = [["-" for _ in range(0,10)] for _ in range(0,10)]
	
	#para recomecar o tabuleiro	
	def resetar(self) -> None:
		for i in range (0,10):
			for j in range (0,10):
				self.tab[i][j] = "-"
	
	#mostrar o proprio tabuleiro			
	def mostrar(self) -> None:
		print("\nSeu tabuleiro:")
		for coluna in range (0,10):
				for linha in range (0,10):
					print(self.tab[linha][coluna], end=" ")
				print(end="\n")
			
	#mostrar o tabuleiro do oponente
	def mostrarop(self) -> None:
		print("\nTabuleiro da máquina:")
		for coluna in range (0,10):
		  	for linha in range (0,10):
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
		for i in range(0, len(pecas.posicao)):
			linha, coluna = pecas.posicao[i]
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
		self.posicao = []
		#for linha in range(0, tamanho):
				#self.posicao[linha] = [-1, -1]
				
	def posicionar(self, posicoes: list[tuple[int]], tab: Tabuleiro, atacante: Jogador) -> None:
		self.posicao = posicoes
		return tab.posicionar(self)
		
	
				
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
		def posicao(self, peca: Pecas, toponente: Tabuleiro) -> None:
			nome = input(f"Dê  um nome para o seu navio de {peca.tamanho}.")
			peca.nome = nome
			verticalOuHorizontal = input("Você quer colocar a sua primeira peca na horizontal ou na vertical?")
			verticalOuHorizontal = verticalOuHorizontal.lower()
			if verticalOuHorizontal == "vertical" or verticalOuHorizontal == "v":
				coluna = input("Em qual coluna você deseja colocar a sua peça?")
				try:
					coluna = int(coluna)-1
					if coluna<0 or coluna>9:
						erro = int("a")
				except:
					print(F"Erro! Só são aceitos números inteiros de 1 a 10. Tente de novo colocar essa peca de {peca.tamanho} casas de tamanho.")
					self.posicao(peca, toponente)
					return
				linha = input("Em qual linha você deseja colocar uma das extremidades do seu navio?")
				try:
					linha = int(linha)-1
					if linha<0 or linha>9:
						erro = int("a")
				except:
					print(F"Erro! Só são aceitos números inteiros de 1 a 10. Tente de novo colocar essa peca de {peca.tamanho} casas de tamanho.")
					self.posicao(peca, toponente)
					return
				if linha+peca.tamanho>9:
					linha2 = linha - peca.tamanho
				elif linha-peca.tamanho<0:
					linha2 = linha + peca.tamanho
				else:
					linha2 = input("Onde você deseja colocar a outra extremidade do navio? Na linha {linha + peca.tamanho} ou na linha {linha - peca.tamanho}?")
					try:
						linha2 = int(linha2)-1
						if linha2 != linha + peca.tamanho and linha != linha - peca.tamanho:
							erro = int("a")
					except:
						print(f"Nenhuma das opções selecionadas. Tente de novo colocar essa peca de {peca.tamanho} casas de tamanho.")
						self.posicao(peca, toponente)
						return
				if linha>linha2:
					i = linha2
					linha2 = linha
					linha = i
				posicoes = []
				for i in range(linha, linha2+1):
					posicoes.append([i, coluna])
				peca.posicionar(posicoes, toponente, self)
			elif verticalOuHorizontal == "horizontal" or verticalOuHorizontal == "h":
				pass
			else:
				print(F"ERRO! Não foi digitado horizontal ou vertical. Tente de novo colocar essa peca de {peca.tamanho} casas de tamanho.")
				self.posicao(peca)
			
		
class Maquina(Jogador):
		#escolhe as posicoes que as pecas da maquina serao colocadas
		def colocarPecas(self, peca: Pecas, tseu: Tabuleiro):
			#sorteio para ver se o navio ficará na horizontal ou vertical:
			verticalOuHorizontal = random.randint(1,2)
			posicoes = []
			linha = random.randint(0,9)
			coluna = random.randint(0,9)
			for i in range(0, peca.tamanho):
				if verticalOuHorizontal == 1:
					if coluna + peca.tamanho <= 9:
						posicoes.append([linha, coluna+i]) 
					else:
						posicoes.append([linha, coluna-i]) 
				else:
					if linha + peca.tamanho <= 9:
						posicoes.append([linha+i, coluna])
					else:
						posicoes.append([linha-i, coluna])
			if not(peca.posicionar(posicoes, tseu, self)):
				self.colocarPecas(peca, tseu)
				
			

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
		pseu.append(Pecas(2, "", voce, toponente))
		pseu.append(Pecas(2, "", voce, toponente))
		pseu.append(Pecas(3, "", voce, toponente))
		pseu.append(Pecas(3, "", voce, toponente))
		pseu.append(Pecas(4, "", voce, toponente))
		pseu.append(Pecas(5, "", voce, toponente))
		poponente.append(Pecas(2, "Rebocador 1", oponente, tseu))
		poponente.append(Pecas(2, "Rebocador 2", oponente, tseu))
		poponente.append(Pecas(3, "Contratorpedeiro 1", oponente, tseu))
		poponente.append(Pecas(3, "Contratorpedeiro 2", oponente, tseu))
		poponente.append(Pecas(4, "Cruzador", oponente, tseu))
		poponente.append(Pecas(5, "Porta-Aviões", oponente, tseu))
		oponente.colocarPecas(poponente[0], tseu)
		oponente.colocarPecas(poponente[1], tseu)
		oponente.colocarPecas(poponente[2], tseu)
		oponente.colocarPecas(poponente[3], tseu)









		
		
	def novaRodada(self, voce: Jogador, oponente: Maquina, tseu: Tabuleiro, toponente: Tabuleiro) -> None:
		voce.atacar(toponente)
		toponente.mostrarop()
		toponente.mostrar()
		oponente.fazerLance(tseu)
		if voce.acertosPartidas == 19 or oponente.acertosPartidas == 19:
			self.fimPartida()
		else:
			self.novaRodada(voce, oponente, tseu, toponente)
	
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
pseu = []
poponente = []		
menu()














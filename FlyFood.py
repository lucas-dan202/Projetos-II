
import itertools as it # Para fazer permutações e combinações
import operator # Para realizar operações
import random as rm # Para fazer algumas funções aleatórias
import time # Para saber o tempo gasto

ini = time.time_ns()

'''__Abrindo e lendo o arquivo de texto com a matriz__'''
with open("entrada7.txt", "r") as rotas:
    rota = rotas.read()

'''__Transformando a matriz do arquivo em uma matriz para o codigo__'''
rota = [x.split() for x in rota.split('\n')]



'''___Função procurando por pontos___'''
def procurandoPorPontosFora(i, j, pontos, todasComb): 
    global rota
    
    # Lendo cada item, em cada linha da matriz
    def procurandoPorPontosDentro(i, j):
        if j < len(rota[i]):
            # Desconsidera os itens que forem 0's e R
            if rota[i][j] != 'R' and rota[i][j] != '0':
                pontos.append(rota[i][j])
            else:
                pass
            procurandoPorPontosDentro(i, j+1)
        else:
            return 0
    # Acessando cada linha da matriz
    procurandoPorPontosDentro(i, j)
    j = 0
    i += 1
    if i < len(rota):
        procurandoPorPontosFora(i, j, pontos, todasComb)
    else:
        pass
    # Aqui utilizando a biblioteca itertools para fazer a 
    # permutação de cada ponto gerando cada percurso possivel
    todasComb = list(it.permutations(pontos))
    todasComb1 = []
    for i in todasComb:
        todasComb1.append(list(i))
        
    pop = todasComb1[rm.randrange(len(todasComb))]
    return pop 


'''__ Criação da classe Fitness
   __ Aqui será avaliada a aptidão das soluções, ou dos conjuntos de rotas __'''
class Fitness():
    def __init__(self, populacao, pontoR):
        # Os atributos iniciais
        self.populacao = populacao
        self.pontoR = pontoR
        self.dronometros = 0
        self.point = ()
        self.i = -1
        
    '''__Função que calcula a distancia entre os pontos__'''
    def Distancia(self, i, ponto, pontoP, linha):
        
        # Armazena na variável 'momento' a localização
        # do proximo ponto a ser calculado
        momento = (i, linha.index(ponto))
        # O calculo da distancia entre os dois pontos
        # que é o mesmo da diferença entre os dois
        p1 = abs(pontoP[0] - momento[0])   
        p2 = abs(pontoP[1] - momento[1])


        # Caso os valores da subtração dem negativos, é utilizado a função "abs()" do python
        # (essa função tranforma o valor em absoluto)
        # Após conseguir a diferença, se soma os valores
        point_value = p1 + p2

        return momento, point_value


    '''__Função que calcula o retorno ao ponto R__'''
    def Volta(self, ponto, pointR):
        
        
        # O calculo é o mesmo da função Distancia, porém apenas com o Ponto R
        p1 = abs(pointR[0] - ponto[0])   
        p2 = abs(pointR[1] - ponto[1])

        point_value = p1 + p2

        return point_value


    '''__Função que calcula a distancia atraves da chamada da função 'Distancia'__'''
    def calcDis(self, i):
        global rota

        # Caso não tenha recebido nenhum ponto, o primeiro ponto é o R
        if self.point == ():
            self.point = self.pontoR
        # O For vai iterar pelo percurso ou sequencia que foi entregue
        for k in self.populacao:
            # Aqui vai iterar por cada linha até encontrar a linha na qual o ponto 'k' está
            for i in range(len(rota)):
                if k in rota[i]:
                    # Quando encontrado a linha, ele entrega e chama a função 'Distancia'
                    ponto, ponto_valor = self.Distancia(i, k, self.point, rota[i])
                    self.dronometros += ponto_valor
                    self.point = ponto
            else:
                pass
        
        # Após ter passado por todos os pontos do percurso, ele faz o calculo do retorno ao ponto 'R'
        ponto_valor = self.Volta(self.point, self.pontoR)
        self.dronometros += ponto_valor
        # Retorna a distancia
        return self.dronometros
    
    
    '''__ Aqui é calculada a aptidão da população e é feita a chamada da função 'calcDis'__'''
    def fitnessValor(self):
        self.i += 1
        
        distancia = float(self.calcDis(self.i))

        if distancia == 0.0: 
            fitness = 1 
            return fitness
        else:
            fitness = 1/distancia      
            return fitness
            

'''__ Função que procura pela posição do R na matriz __'''
def procurandoPorR(i):
    global rota, pointR
    if i < len(rota):
        if 'R' in rota[i]:
            # Procura por R na matriz
            pointR = (i, rota[i].index('R'))
            
        else:
            procurandoPorR(i+1)
    return pointR

'''__ Função que gera a população incial __'''
def popInicial(tamanho):
    populacao = []
    for i in range(0, tamanho):
        # Cria a população chamando a função procurandoPorPontosFora
        # que retorna um conjunto aleatorio de possiveis soluções
        populacao.append(procurandoPorPontosFora(i=0, j=0, pontos = [], todasComb = []))
    return populacao

    
'''__ Aqui é instanciada a classe Fitness para obter a aptidão de cada possivel solução da populaçãp e listar em um dicionario'''
def melhorFitness(populacao): # melhorFitness
    lista = {}
    for i in range(0, len(populacao)):
        lista[i] = Fitness(populacao[i], procurandoPorR(i=0)).fitnessValor()
    return sorted(lista.items(), key=operator.itemgetter(1), reverse=True)

'''__ Função que atraves de elitismo deve separar dos melhores individuos/soluções da população que foi analisada __'''
def elitismo(melhorFitness, bestLen):
    resultado = []
    a = melhorFitness[rm.randint(0, len(melhorFitness) - 1)]
    b = melhorFitness[rm.randint(0, len(melhorFitness) - 1)]
    for i in range(0, bestLen):
        resultado.append(melhorFitness[i][0])
    for i in range(0, len(melhorFitness) - bestLen):
        a = melhorFitness[rm.randint(0, len(melhorFitness) - 1)][0]
        b = melhorFitness[rm.randint(0, len(melhorFitness) - 1)][0]
        while b == a:
            b = melhorFitness[rm.randint(0, len(melhorFitness) - 1)][0]
        if a >= b:
            resultado.append(a)
        else:
            resultado.append(b)
    return resultado
 
'''__ Função que irá determinar os individuos que farão parte do cruzamento __'''   
def selecionarParaCross(populacao, resultado): 
    selecao = []
    for i in range(0, len(resultado)):
        index = resultado[i]
        selecao.append(populacao[index])
    return selecao



'''__ Função que irá fazer o cruzamento atraves de crossover entre cada par de individuos que receber e retornar o seu 'filho' __'''
def crossover(solA, solB):
    filho = []
    filhoSA = []
    filhoSB = []

    geneA = int(rm.random() * len(solA))
    geneB = int(rm.random() * len(solB))

    inicio = min(geneA, geneB)
    fim = max(geneA, geneB)

    for i in range(inicio, fim):
        filhoSA.append(solA[i])

    filhoSB = [item for item in solB if item not in filhoSA]

    filho = filhoSA + filhoSB

    return filho


'''__ Função que irá iterar entre todos os selecionados da função 'elitismo' e passa-los para função de cruzamento crossover afim
    de gerar o restante da nova geração __'''
def popCrossover(selecao, bestLen):
    filhos = []
    lgth = len(selecao) - bestLen
    pool = rm.sample(selecao, len(selecao))
    
    for i in range(0, bestLen):
        filhos.append(selecao[i])
        
    for i in range(0, lgth):
        filho = crossover(pool[i], pool[len(selecao) - i - 1])
        filhos.append(filho)
    
    return filhos

'''__ Função que vai testar se o individuo ta dentro da taxa de mutação e, caso esteja, aplicar a mutação trocando a posição 
    de um ponto da rota por outro __'''
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if(rm.random() < taxa_mutacao):
            prox = int(rm.random() * len(individuo))
            
            pontoa = individuo[i]
            pontob = individuo[prox]
            
            individuo[i] = pontob
            individuo[prox] = pontoa
    
    return individuo

'''__ Função encarregada de iterar por todos os individuos e aplicar a função 'mutacao' __'''
def popMutacao(populacao, taxa_mutacao):
    mut = []
    
    for i in range(0, len(populacao)):
        individuo = mutacao(populacao[i], taxa_mutacao)
        mut.append(individuo)
    
    return mut

'''__ Função responsavel por chamar cada função necessária para criar uma nova geração e determinar seus resultados __'''
def novaGeracao(pop, bestLen, taxa_mutacao):
    best = melhorFitness(pop)
    resultado = elitismo(best, bestLen)
    selecaoCross = selecionarParaCross(pop, resultado)
    filhos = popCrossover(selecaoCross, bestLen)
    proxima = popMutacao(filhos, taxa_mutacao)
    return proxima

'''__ Função principal que vai criar a população inicial e, dentro do paramentro de parada, vai criar as proximas gerações
    para retornar a melhor rota __'''
def run(tamanho, bestLen, taxa_mutacao, parada):
    pop = popInicial(tamanho)
    melhor_dis = [1 / melhorFitness(pop)[0][1]]
    
    for i in range(1, parada + 1):
        pop = novaGeracao(pop, bestLen, taxa_mutacao)
        
        melhor_dis.append(1/melhorFitness(pop)[0][1])
        
    bestRoutIndex = melhorFitness(pop)[0][0]
    bestRout = pop[bestRoutIndex]
    print(melhor_dis[bestRoutIndex])     # Imprime o custo, que no caso são os 'dronômetros'
    return bestRout


# Declaração da função que vai receber a localização do ponto R
pointR = ()

'''__ A chamada da função principal e os atributos de tamanho da população, tamanho do elitismo, a taxa de mutação e a quantidade de gerações
   __ que também é o parametro de parada __'''
valor_final = run(100, 50, 0.5, 50)

end = time.time_ns()

'''__ Esse bloco de comado é para as conversões de nanosegundos, segundos, minutos, etc __'''
tempo = (end - ini) / 1*10**-9  # converte obrigatoriamente para segundos
if tempo > 60: 
    tempo = tempo / 60
    if tempo > 60: 
        tempo = tempo / 60
        if tempo > 24: 
            tempo = tempo / 24
            if tempo > 31: 
                tempo = tempo / 31
                if tempo > 12:
                    tempo = tempo / 12
                    print("%.2fanos" % (tempo)) # anos
                else:    
                    print("%.2fmeses" % (tempo)) # meses
            else:
                print("%.2fdias" % (tempo)) # dias
        else:
            print("%.2fh" % (tempo)) # horas
    else:
        print("%.2fmin" % (tempo)) # minutos
else:
    print("%.2fs" % (tempo)) # segundos

print(valor_final)

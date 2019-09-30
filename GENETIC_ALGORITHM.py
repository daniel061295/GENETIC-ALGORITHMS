import numpy as np
import matplotlib.pyplot as plt	
import math
from random import randrange
####################################BEGIN OF AG#######################################################################
class new_individual():
	def __init__(self):
		self.genotype = []
		self.fenotype = 0
		self.adaptation = 0		
		self.score = 0
		self.accumulated_score = 0	
	def generate_genotype(self,length):
		for i in range(length):
			b = float(np.random.rand(1,1))
			if b >= 0.5:
				self.genotype.append(1)
			if b < 0.5:
				self.genotype.append(0)	
	def generate_fenotype(self,initial,final):
		c = ''
		length = len(self.genotype)
		for i in range(length):
			c = c + str(self.genotype[i])
			num = initial + (int(c,2)*final) / (pow(2,length)-1)
		self.fenotype = num
	def generate_adaptation(self,function):
		self.adaptation = function(self.fenotype)

def generate_scores(population):
	k = len(population)
	#suma = 0
	new_adaptations = []
	for w in range(k):
		#suma = suma + population[w].adaptation
		new_adaptations.append(population[w].adaptation)
	for b in range(k):
		new_adaptations[b] = abs(min(new_adaptations)) + new_adaptations[b]  
	new_suma = sum(new_adaptations)
	population[0].score = new_adaptations[0]/new_suma
	population[0].accumulated_score = new_adaptations[0]/new_suma
	for n in range(1,k):
		population[n].score = new_adaptations[n]/new_suma
		population[n].accumulated_score = population[n-1].accumulated_score + population[n].score

def new_population(bits,length,initial,final,function):
	population = []
	for i in range(length):
		individual = new_individual()
		individual.generate_genotype(bits)
		individual.generate_fenotype(initial,final)
		individual.generate_adaptation(function)
		population.append(individual)
	generate_scores(population)
	return(population)

def roulette(population):
	k = len(population)
	a = np.random.rand(1,k)
	x=[0]*k
	for m in range(1,k):
		for i in range(k):
			if a[0][i] < population[m].accumulated_score and a[0][i] > population[m-1].accumulated_score :
				x[i] = new_individual()
				x[i].genotype = population[m].genotype
				x[i].fenotype = population[m].fenotype
				x[i].adaptation = population[m].adaptation 
			if a[0][i] < population[0].accumulated_score :	
				x[i] = new_individual()
				x[i].genotype = population[0].genotype
				x[i].fenotype = population[0].fenotype
				x[i].adaptation = population[0].adaptation
	generate_scores(x)
	return(x)

def crossover(population,reproduction,initial,final,function):
	for i in range(1,len(population),2):
		if reproduction > float(np.random.rand(1,1)):
			n = len(population[i].genotype)
			a = randrange (0, n ,1)
			son1 = new_individual()
			son2 = new_individual()
			genotype1 = [0]*n
			genotype2 = [0]*n
			genotype1 = population[i-1].genotype[:a] + population[i].genotype[a:]
			genotype2 = population[i].genotype[:a] + population[i-1].genotype[a:]
#			print(str(genotype1)+ ' from '+ str(i-1) +' and ' + str(i) + ' in the point ' + str(a) )
#			print(str(genotype2)+ ' from '+ str(i-1) +' and ' + str(i) + ' in the point ' + str(a) )		
			for w in range (n): 
				son1.genotype.append(genotype1[w])
			for q in range (n): 
				son2.genotype.append(genotype2[q]) 
			son1.generate_fenotype(initial,final)
			son2.generate_fenotype(initial,final)
			son1.generate_adaptation(function)
			son2.generate_adaptation(function)
			population[i] = son2
			population[i-1] = son1
	generate_scores(population)

def mutate(population,mutation,initial,final,function):
	for i in range(len(population)):	
		for x in range(len(population[i].genotype)):
			if mutation > float(np.random.rand(1,1)):
#				print(population[i].genotype)
				if population[i].genotype[x] == 0 :
					population[i].genotype[x] = 1
				else:
					population[i].genotype[x] = 0
#				print(str(population[i].genotype) + ' from index: ' + str(i) + ' in position: ' + str(x))
		population[i].generate_fenotype(initial,final)
		population[i].generate_adaptation(function)
	generate_scores(population)

def show(population,generation):
	popu_genotype = []
	popu_fenotype = []
	popu_adaptation = []
	popu_score = []
	popu_accumulated_score = []
	best_genotype = []
	best_fenotype = 0
	best_adaptation = 0
	for i in range(len(population)):
		popu_genotype.append(population[i].genotype)
		popu_fenotype.append(population[i].fenotype)
		popu_adaptation.append(population[i].adaptation)
		popu_score.append(population[i].score)
		popu_accumulated_score.append(population[i].accumulated_score)
	best_score = max(popu_score)	
	for x in range(len (popu_score)):
		if popu_score[x] == best_score :
			best_genotype.append(popu_genotype[x])
			best_fenotype = popu_fenotype[x]
			best_adaptation = popu_adaptation[x]  
			break
	average_adaptation = sum(popu_adaptation)/len(popu_adaptation)
	selective_pressure = best_adaptation/average_adaptation
#	print('================================================================================================================')
#	print ('\nGENOTYPE:\n' + str(popu_genotype))
#	print ('\nFENOTYPE:\n' + str(popu_fenotype))
#	print ('\nADAPTATION:\n' + str(popu_adaptation))
#	print ('\nSCORE:\n' + str(popu_score))
#	print ('\nACCUMULATED SCORE:\n' + str(popu_accumulated_score))
#	print ('\n\n\n BEST OF THIS GENERATION:\n' + ' GENOTYPE:' + str(best_genotype) +'\n FENOTYPE:' + str(best_fenotype) + '\n ADAPTATION:' + str(best_adaptation) + '\n SCORE: ' + str(best_score))
	print('BEST ADAPTATION OF GEN ' + str(generation)+': '+ str(best_adaptation))
#	print('ADAPTATION AVERAGE OF GEN ' + str(generation)+': '+ str(average_adaptation))
#	print('SELECTIVE PRESSURE OF GEN ' + str(generation)+': '+ str(selective_pressure))
#	print('================================================================================================================')
#	plt.bar(popu_fenotype, popu_adaptation, align='center', alpha=1, color='darkblue',width=0.1)
	#plt.show()
	#return [popu_genotype,popu_fenotype,popu_adaptation]
	return (best_fenotype,best_adaptation,popu_fenotype,popu_adaptation)

def implementation (generations,bits,length,initial,final,function,reproduction,mutation):
	population1 = new_population(bits,length,initial,final,function)
	if generations>1 :
		show(population1,1)
		for h in range(2,generations):
			population1 = roulette(population1)
			crossover(population1,reproduction,initial,final,function)
			mutate(population1,mutation,initial,final,function)
			show(population1,h)
	y = []
	x = np.linspace(initial,final,pow(2,bits)-1)
	for n in range(x.shape[0]):
		y.append(function(x[n]))
	#plt.plot(x,y)
	best = show(population1,generations)
	#plt.plot(best[0],function(best[0]),'rx')
	plt.bar(best[2], best[3], align='center', alpha=1, color='darkblue',width=0.01)
	plt.bar(best[0], best[1], align='center', alpha=1, color='darkred',width=0.01)
	plt.show()

############################################FINAL OF AG##############################################################
def cuadrado(x):
	out = -1*math.pow((x),2) +2 
	return out

implementation(25,8,100,-2,2,cuadrado,0.4,0.1)

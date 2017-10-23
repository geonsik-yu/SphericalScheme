import numpy
import scipy
import math
import sys
import getopt
import random
from scipy import spatial
from scipy.special import erfinv
import copy
import networkx as nx

def rewire(InitialMatrix, beta):
	AdjMatrix = InitMatrix = [[0]*n for i in range(n)]
	for i in range(0, len(InitMatrix)):
		for j in range(i+1, len(InitMatrix)):
			if (InitMatrix[i][j] == 1) and (random.random() > beta):
				candidates = [i for i,x in enumerate(i) if x == 0]
			elif (InitMatrix[i][j] == 1) and (random.random() <= beta):
				break;				

	return AdjMatrix


a = [0,0,0,0,0,0,0,1,1,1,0,0,0,1,1]
print 


m = 30 ## dimensionality
n = 280 ## organization size
## [Code to Individual] socialization coefficient
## [Individual to Code] learning coefficient
## [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] [0.1, 0.5, 0.9]

G = nx.caveman_graph(n, 7)
InitMatrix = [[0]*n for i in range(n)]
for i in range(0, n):
	Adjs = nx.all_neighbors(G, i)
	for ele in Adjs:
		InitMatrix[i][ele] = 1

f = open('./Fang16.txt', 'a');
"""

for beta in numpy.arange(0,1,0.05):
	for learning in [0.3]:
		Equils = []
		for instance in range(0, 100):
			AdjMatrix = copy.deepcopy(InitMatrix)



			reality = [1]*m
			beliefs = []

			## measurements
			elapsed_time = 0
			equilibrium = 0

			while len(beliefs) != n:
				belief = []
				for i in range(0, m):
					belief.append( random.choice([-1, 0, +1]) )
				if belief.count(1) <= 0.65 * m:
					beliefs.append( belief )

			equil_flag = False
			while ~(equil_flag):


	for p_2 in [0.1, 0.5, 0.9]:



			for z in range(0, 80):
				## Socialization Procedure
				for i in range(0, n):
					for j in range(0, m):
						if (orgCode[j] != 0) and (random.random() < p_1):
							beliefs[i][j] = orgCode[j]
				## End Procedure

				## Learning Procedure
				beliefs.sort(key=lambda x: -sum(x))
				#for i in range(0, n/2):
				#	print beliefs[i], beliefs[i].count(1)
				#print "asdfasdfa"

				dominance = {}
				dominance[1] = [0]*m
				dominance[0] = [0]*m
				dominance[-1] = [0]*m
				dominant_vector = [0]*m
				dominant_k      = [0]*m

				for i in range(0, n):
					if beliefs[i].count(1) > orgCode.count(1):
						for j in range(0, m):
							if beliefs[i][j] == 1:
								dominance[1][j] += 1
							elif beliefs[i][j] == -1:
								dominance[-1][j] += 1
							else:
								dominance[0][j] += 1
				#print dominance

				for i in range(0, m):
					if dominance[1][i] == dominance[-1][i]:
						dominant_vector[i] = 0
						dominant_k[i] = dominance[0][i] - dominance[orgCode[i]][i]
					elif (dominance[0][i] > dominance[1][i]) and (dominance[0][i] > dominance[-1][i]):
						dominant_vector[i] = 0
						dominant_k[i] = dominance[0][i] - dominance[orgCode[i]][i]
					elif (dominance[1][i] > dominance[0][i]) and (dominance[1][i] > dominance[-1][i]):
						dominant_vector[i] = 1
						dominant_k[i] = dominance[1][i] - dominance[orgCode[i]][i]
					elif (dominance[-1][i] > dominance[0][i]) and (dominance[-1][i] > dominance[1][i]):
						dominant_vector[i] = -1
						dominant_k[i] = dominance[-1][i] - dominance[orgCode[i]][i]

				for i in range(0, m):
					#print 1-(1-p_2)**dominant_k[i]
					if random.random() < 1-(1-p_2)**dominant_k[i]:
						orgCode[i] = dominant_vector[i]
				## End Procedure

				elapsed_time += 1

				orgKnowledge = orgCode.count(1)
				if orgKnowledge != equilibrium:
					equilibrium = orgKnowledge
				else:
					equil_flag = True
					for i in range(0, n/2):
						for j in range(0, m):
							if beliefs[i][j] != orgCode[j]:
								equil_flag = False
					if equil_flag == True:
						break;

				##print elapsed_time, orgKnowledge, orgCode
			Equils.append(orgKnowledge)
		
		f.write( repr(p_1)+","+repr(p_2)+","+repr(sum(Equils)/(len(Equils)*1.0))+","+repr(max(Equils))+'\n' )



"""




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

# This simulation scheme follows ISO spherical coordinate system convention.
#   - angle_t(theta) := polar angle     [0, pi]
#   - angle_p(phi)   := azimuth angle   [0, 2*pi] 

# Static variables (Hard-coded). ---------------------------------------
Instance_Count = 50
Angle_Lower_Bound = 0.003935
Angle_Upper_Bound = 3.126928
Max_Performance = 10 + math.sqrt(40/3)*erfinv( math.cos(Angle_Lower_Bound) ) # approx 21.5472
Min_Performance = 10 + math.sqrt(40/3)*erfinv( math.cos(Angle_Upper_Bound) ) # approx  0.0001

Approx_30p_Angle = 2.548343 # approx 10.7736
Approx_50p_Angle = 1.333029 # approx 10.7736
Approx_60p_Angle = 0.732863 # approx 12.9283
Approx_70p_Angle = 0.314320 # approx 15.083
Approx_80p_Angle = 0.100644 # approx 17.2377
Approx_90p_Angle = 0.023457 # approx 19.3924
## Explicit equation for angles x
## sqrt(40/3)*erfinv( cos(x) ) = P * ( sqrt(40/3)*erfinv( cos(LB) ) - sqrt(40/3)*erfinv( cos(UB) )) + sqrt(40/3)*erfinv( cos(UB) )
## sqrt(40/3)*erfinv( cos(x) ) = P * ( sqrt(40/3)*erfinv( cos(0.003935) ) - sqrt(40/3)*erfinv( cos(3.126928) )) + sqrt(40/3)*erfinv( cos(3.126928) )
# ----------------------------------------------------------------------

def normal_performance(opinion, answer): 
	# Assume market vector is not fixed.
	angle = angle_between(opinion, answer)
	return 10 + math.sqrt(40/3)*erfinv( math.cos(angle) )

def opinion_init(number_of_nodes, condition):
	## Initialize polar angles (angle_t) and azimuth angles (angle_p)
	angle_t = None
	angle_p = None
	if condition == 1:
		# Initial performances are between 50% and 100%.
		U50p = 0.5*(numpy.cos(Approx_50p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(U50p, 1.0, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 2:
		# Initial performances are between 60% and 100%.
		U60p = 0.5*(numpy.cos(Approx_60p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(U60p, 1.0, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 3:
		# Initial performances are between 50% and 60%.
		U50p = 0.5*(numpy.cos(Approx_50p_Angle) + 1)
		U60p = 0.5*(numpy.cos(Approx_60p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(U50p, U60p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 4:
		# Initial performances are between 0% and 50%.
		U50p = 0.5*(numpy.cos(Approx_50p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(0.0, U50p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 5:
		# Initial performances are between 0% and 60%.
		U60p = 0.5*(numpy.cos(Approx_60p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(0.0, U60p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 6:
		# Initial performances are between 0% and 70%.
		U70p = 0.5*(numpy.cos(Approx_70p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(0.0, U70p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 7:
		# Initial performances are between 0% and 80%.
		U80p = 0.5*(numpy.cos(Approx_80p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(0.0, U80p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 8:
		# Initial performances are between 0% and 90%.
		U90p = 0.5*(numpy.cos(Approx_90p_Angle) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(0.0, U90p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	elif condition == 9:
		# Initial performances are between 50% and 60%.
		# and angle_p (phi) are between 0 and pi/6
		U50p = 0.5*(numpy.cos(Approx_50p_Angle) + 1)
		U60p = 0.5*(numpy.cos(Approx_60p_Angle) + 1)		
		angle_t = numpy.arccos(2 * numpy.random.uniform(U50p, U60p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1/20, number_of_nodes))
	elif condition == 10:
		# Initial performances are between 50% and 60%.
		# and angle_p (phi) are between 0 and pi/6
		U60p = 0.5*(numpy.cos(Approx_60p_Angle) + 1)		
		angle_t = numpy.arccos(2 * numpy.random.uniform(0.0, U60p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1/20, number_of_nodes))
	elif condition == 11:
		# Initial performances are between 0% and 47%.
		U50p = 0.5*(numpy.cos(Approx_50p_Angle + 0.2) + 1)
		angle_t = numpy.arccos(2 * numpy.random.uniform(0.0, U50p, number_of_nodes) - 1)
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))

	result = []
	for i in range(0, number_of_nodes):
		result.append([angle_t[i], angle_p[i]])
	return result

def spherical2cartesian(a):
	## Input: a spherical coordinates with unit length. [theta, phi]
	return [numpy.sin(a[0])*numpy.cos(a[1]), numpy.sin(a[0])*numpy.sin(a[1]), numpy.cos(a[0])]

def arc_midpoint(a, b):
	## Input: two spherical coordinates with unit length.
	cartesian_a = spherical2cartesian(a)
	cartesian_b = spherical2cartesian(b)
	lin_mpt = [ (cartesian_a[0] + cartesian_b[0])/2, \
				(cartesian_a[1] + cartesian_b[1])/2, \
				(cartesian_a[2] + cartesian_b[2])/2]

	magnitude = numpy.sqrt(lin_mpt[0]**2 + lin_mpt[1]**2 + lin_mpt[2]**2)
	mid_theta = numpy.arccos(lin_mpt[2]/magnitude)
	mid_phi = numpy.arctan2(lin_mpt[1], lin_mpt[0]) ## [Note] usage of arctan2 
	return [mid_theta, mid_phi]

def learning(opinion_a, opinion_b, param):
	if param == 1: ## 12.5%, 1/8
		return arc_midpoint(opinion_a, learning(opinion_a, opinion_b, 2))
	elif param == 2: ## 25%, 2/8
		return arc_midpoint(opinion_a, learning(opinion_a, opinion_b, 4))
	elif param == 3: ## 37.5%, 3/8
		return arc_midpoint(learning(opinion_a, opinion_b, 2), learning(opinion_a, opinion_b, 4))
	elif param == 4: ## 50%, 4/8
		return arc_midpoint(opinion_a, opinion_b)
	elif param == 5: ## 62.5%, 5/8
		return arc_midpoint(learning(opinion_a, opinion_b, 4), learning(opinion_a, opinion_b, 6))
	elif param == 6: ## 75%, 6/8
		return arc_midpoint(learning(opinion_a, opinion_b, 4), opinion_b)
	elif param == 7: ## 87.5%, 7/8
		return arc_midpoint(learning(opinion_a, opinion_b, 6), opinion_b)

def angle_between(a, b):
	a = numpy.inner( spherical2cartesian(a), spherical2cartesian(b) )
	return numpy.arccos(a)
	#return numpy.arccos( numpy.inner( spherical2cartesian(a), spherical2cartesian(b) ) )

def standardize(a):
	# polar angle in [0, pi]
	if a[0] > math.pi:
		a[0] = 2*math.pi - a[0]
	if a[0] < 0:
		a[0] = -a[0]
	# azimuth angle in [0, 2*pi]	
	if a[1] > 2*math.pi:
		a[1] = a[1] - 2*math.pi
	if a[1] < 0:
		a[1] = 2*math.pi + a[1]
	if a[0] < 0.003935:
		##print a[0]
		a[0] = 0.003935
	if a[0] > 3.137657:
		a[0] = 3.137657
	return a

def simulator(input_option):
	# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]
	#	1. NodeCount     := Indicates the number agents in the system (organization).
	#	2. SearchRange   := Represents the search range of each agent's learning activity.
	#						It is an upper limit of angle between two opinions.
	#	3. LearningRate  := Represents the learning rate of each agent.
	#						In this simulation, it is {25%, 50%, 75%}.
	#	4. Behavior      := Represents the degree of randomness in the learning process.
	#	5. InitCondition := Represents the type of knowledge initialization pattern.
	#   6. marketFileName:= File name of market vector movement.

	NodeCount = int(input_option[0])
	SearchRange = float(input_option[1])
	LearningRate = int(input_option[2])
	BehaviorParameter = float(input_option[3])
	InitCondition = int(input_option[4])

	convergence_log = []
	elapsed_time_log = []

	market_file = open(input_option[5], 'r')
	market_data = []
	for i in range(0, 201):
		market_data.append( [float(x) for x in market_file.readline().split(",")] )


	# [START] Simulations ----------------------------------------------
	for instance in range(0, Instance_Count):
		## initialize market coordinate
		market = [0.0, 0.0]

		## initialize opinions
		opinion = opinion_init(NodeCount, InitCondition)
		performance_log = []

		flag = 0
		time = 0
		mind = 0
		stop = False
		current_performance = [0]*NodeCount

		if instance < 0.001 and InitCondition == 4:
			trackFile = open('./geonsik_result_track'+SearchRange+'.txt', 'w')

		##while(stop == False):
		while(time < 1000):
			mind = int((time-1)/5)
			market = market_data[mind]
			# Step 1. Evaluation
			performance_log.append(sum(current_performance)/((Max_Performance-Min_Performance)*NodeCount))
			for i in range(0, NodeCount):
				current_performance[i] = normal_performance(opinion[i], market)
			if time == 0:
				print "max!!", max(current_performance)/(Max_Performance-Min_Performance)			
			if instance < 0.001 and InitCondition == 4:
				for i in range(0, NodeCount):
					cart = spherical2cartesian(opinion[i])
					trackFile.write(repr(time)+","+",".join(str(x) for x in cart)+'\n');
			

			#	print opinion[i], " ::::", current_performance[i] 
			#print "----------------"
			#print time, " ",max(current_performance/(Max_Performance-Min_Performance))

			# Step 2. Learning.
			new_opinion = [[0 for v1 in range(2)] for v2 in range(NodeCount)]
			for i in range(0, NodeCount):
				# Step 2-1. Search and Assimilate.
				best_value = current_performance[i]
				best_index = i
				for j in range(0, NodeCount):
					if ( angle_between(opinion[i], opinion[j]) < SearchRange*math.pi ) \
						and current_performance[j] > best_value:
					#if current_performance[j] > best_value:
						best_value = current_performance[j]
						best_index = j
				#print best_index, "  ",best_value/(Max_Performance-Min_Performance)
				if i != best_index:
					new_opinion[i] = learning(opinion[i], opinion[best_index], LearningRate)
				else:
					new_opinion[i] = opinion[i]
				#print "---------"
				#print opinion[i]
				#print opinion[best_index]
				#print new_opinion[i]
				#print "---------"

				# Step 2-2. Add Perturbation.
				
				for j in range(0, 2):
					new_opinion[i][j] += numpy.random.uniform(-BehaviorParameter, +BehaviorParameter)
				# Step 2-3. Standardize.
				new_opinion[i] = standardize(new_opinion[i])	
			opinion = copy.deepcopy(new_opinion)

			# Step 3. Record Time and Check Exit Condition.
			time += 1
			if (len(performance_log) > 2) and (abs(performance_log[-1] - performance_log[-2]) < 0.002):
				flag += 1
			#else: 
			#	flag = 0
			if flag > 4:
				stop = True;
			if sum(current_performance)/((Max_Performance-Min_Performance)*NodeCount) > 0.95:
				stop = True;
			#if time%100 == 0:
			#	print sum(current_performance)/((Max_Performance-Min_Performance)*NodeCount), " ", best_value/(Max_Performance-Min_Performance)
			#if (len(performance_log) > 2):
			#	print performance_log[-1]
			#if time > 100:
			#	stop = True;

		org_performance = sum(current_performance)/((Max_Performance-Min_Performance)*NodeCount)
		print "Convergence = ", org_performance, ",   Elapsed Time = ", time
		convergence_log.append(org_performance)
		elapsed_time_log.append(time)
	# [END] Simulations ------------------------------------------------

	# return average statistics of instances under given conditions.
	##return [sum(convergence_log)/len(convergence_log), sum(elapsed_time_log)/(1.0*len(elapsed_time_log))]
	return [sum(convergence_log)/len(convergence_log), numpy.var(convergence_log)]
def main(argv=None):
	if argv is None:
		argv = sys.argv
    # parse command line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
	except getopt.error, msg:
 		print msg
		print "for help use --help"
		sys.exit(2)

	# process arguments
	NodeCount = 0
	Neighbor = 0
	LearningRate = 0
	BehaviorParameter = 0

	## set random seed.
	numpy.random.seed(1)

	if len(args) > 0:
		NodeCount		= int(args[0])
	if len(args) > 1:
		Neighbor    	= int(args[1])
	if len(args) > 2:
		LearningRate 	= float(args[2])
	if len(args) > 3:
		BehaviorParameter = float(args[3])

	##org_option = [NodeCount, LearningRate, BehaviorParameter]
	#for BP in [0.0, 0.05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4]:
	condition = 11
	##f = open('./geonsik_result'+repr(condition)+'.txt', 'w')
	
	##for BP in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4]:
	##for BP in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
	##for BP in [0.0, 0.4, 0.8, 1.2, 1.6]:
	##for BP in [0.0]:

	if False: ## Experiment 1: Effect of Randomness
		L = 3
		for BP in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]:
			print BP
			for condition in [11, 4,5,6,7]:
				org_option = [40, 1, L, BP, condition]
				# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]

				result = simulator(org_option)
				f.write(repr(condition)+","+repr(BP)+","+repr(result[0])+","+repr(result[1])+'\n');
	## --------------------------------------------------------------------------------------------

	if False: ## Experiment 2: Value of Slow Learning
		BP = 0
		##for L in [12.5, 25, 37.5, 50, 62.5, 75]:
		for L in [1,2,3,4,5,6,7]:
			for condition in [11, 4,5,6,7]:
				org_option = [40, 1, L, BP, condition]
					# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]
				result = simulator(org_option)
				f.write(repr(condition)+","+repr(BP)+","+repr(L)+","+repr(result[0])+","+repr(result[1])+'\n');
	## --------------------------------------------------------------------------------------------
	

	if True: ## Experiment 3: Value of 
		BP = 0
		L = 3
		market_file = "./market_simga2.0/market0_mu0.0_sigma2.0.txt"
		## market_file = "./market_simga2.0/market0_mu0.0_sigma2.0.txt"

		for condition in [11, 4,5,6,7]:

			##for searchRange in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
			#for searchRange in [0.1, 0,2]5
			for searchRange in [0.9, 1]:
				f = open('./geonsik_result'+repr(searchRange)+'.txt', 'w')

				org_option = [40, searchRange, L, BP, condition, market_file]
					# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]
				result = simulator(org_option)
				f.write(repr(condition)+","+repr(searchRange)+","+repr(result[0])+","+repr(result[1])+'\n');
	## --------------------------------------------------------------------------------------------


	f.close()

	
if __name__ == "__main__":
    main()
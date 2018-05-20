## -------------------------------------------------------------------------------------------
# This simulation scheme is extended from 'spherical.py'.
# It adds followings to existing scheme:
#   1. 
#   2. 
## -------------------------------------------------------------------------------------------
# This simulation scheme follows ISO spherical coordinate system convention.
#   - angle_t(theta) := polar angle     [0, pi]
#   - angle_p(phi)   := azimuth angle   [0, 2*pi] 
## -------------------------------------------------------------------------------------------

import copy
import math
import numpy
import random
import spherical
from scipy.special import erfinv
from scipy.special import erf
# Static values (Hard-coded). ----------------------------------------------------------------
Instance_Count = 200
Angle_Lower_Bound = 0.01

# Derived values -----------------------------------------------------------------------------
Max_Performance = numpy.round( 10 + math.sqrt(40/3)*erfinv( math.cos(Angle_Lower_Bound) ), 10)
Min_Performance = numpy.round( 10 - math.sqrt(40/3)*erfinv( math.cos(Angle_Lower_Bound) ), 10)
Angle_Upper_Bound = numpy.arccos( erf( (Min_Performance - 10)/math.sqrt(40/3) ) )

Approx_Angles_wPercentage = {}
for percentage in range(0, 11):
	x = numpy.arccos( erf(( percentage * 0.1 * ( Max_Performance - Min_Performance ) + Min_Performance -10 ) / math.sqrt(40/3)) )
	Approx_Angles_wPercentage[repr(percentage*10)+'%'] = numpy.round( x, 10 )
print Approx_Angles_wPercentage


# Static values (Hard-coded). ----------------------------------------------------------------
Number_Of_Candidates = 7
Org_Size = 10
Instance_Count = 500

def candidateSelect(Stacked, Candidates, Flag):
	# March's normal distribution assumption.
	# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]
	#	1. Stacked    := Indicates the list of opinions collected from previous employment cycles.
	#	2. Candidates := Represents the candidates of employment in this cycle.
	#   3. Flag       := 

	if Flag == 'r':
		return random.sample(range(0,Number_Of_Candidates), 1)[0]
	#----------------------------------------------------------------------------------------

	## Calculate current stack's average values.
	currentAvgFit = 0
	currentAvgDiv = 0
	if len(Stacked) > 0:
		for i in range(0, len(Stacked)):
			currentAvgFit += spherical.normal_performance(Stacked[i])
		currentAvgFit = currentAvgFit/len(Stacked)
	if len(Stacked) > 1:
		currentAvgDiv = spherical.dissimilarity(Stacked, len(Stacked))

	# Evaluate candidates.
	divEval = [0]*Number_Of_Candidates
	fitEval = [0]*Number_Of_Candidates
	all_negative_fit = True
	all_negative_div = True
	for i in range(0, Number_Of_Candidates):
		temp = copy.deepcopy(Stacked)
		temp.append(Candidates[i])
		divEval[i] = spherical.dissimilarity(temp, len(temp))
		fitEval[i] = spherical.normal_performance(Candidates[i])
		if divEval[i] > currentAvgDiv:
			all_negative_div = False
		if fitEval[i] > currentAvgFit:
			all_negative_fit = False

	if Flag == 'd1' or (Flag == 'd2' and all_negative_fit == True):  
		## Candidate maximizes diversity.
		bestValue = divEval[0]
		bestIndex = 0
		for i in range(1, Number_Of_Candidates):
			if divEval[i] > bestValue:
				bestIndex = i
		return i

	if Flag == 'd2' and all_negative_fit == False:  
		## Candidate maximizes diversity 
		## 1) while not weakening fitness.
		## 2) or minimizing diversity loss when condition 1) is not satisfiable.
		bestValue = divEval[0]
		bestIndex = 0
		for i in range(1, Number_Of_Candidates):
			if divEval[i] > bestValue and fitEval[i] > currentAvgFit:
				bestIndex = i
		return i

	if Flag == 'f1' or (Flag == 'f2' and all_negative_div == True):  ## Candidate maximizes fitness.
		bestValue = fitEval[0]
		bestIndex = 0
		for i in range(1, Number_Of_Candidates):
			if fitEval[i] > bestValue:
				bestIndex = i
		return i

	if Flag == 'f2':  ## Candidate maximizes fitness while not weakening diversity.
		bestValue = fitEval[0]
		bestIndex = 0
		for i in range(1, Number_Of_Candidates):
			if fitEval[i] > bestValue and divEval[i] > currentAvgDiv:
				bestIndex = i
		return i




### Over Mediocre Strategy 
def simulator_strategy2suitability(strategy, polar_upper_str = None, polar_lower_str = None):
	polar_upper = Angle_Upper_Bound
	polar_lower = Angle_Lower_Bound	
	if polar_upper_str != None:
		polar_upper = Approx_Angles_wPercentage[polar_upper_str]
	if polar_lower_str != None:
		polar_lower = Approx_Angles_wPercentage[polar_lower_str]

	div_log = []
	fit_log = []
	con_log = []

	# [START] Simulations --------------------------------------------------------------------
	for instance in range(0, Instance_Count):
		## initialize market coordinate
		market = [0.0, 0.0]
		stacked = spherical.opinion_init(2, polar_upper, polar_lower)
		## initialize opinions
		while len(stacked) != 10:
			candidates = spherical.opinion_init(Number_Of_Candidates, polar_upper, polar_lower) #azimuth_upper_ratio, azimuth_lower_ratio)
			select = candidateSelect(stacked, candidates, strategy)
			stacked.append(candidates[select])
		
		fitness = 0
		for i in range(0, 10):
			fitness += spherical.normal_performance(stacked[i])
		fit_log.append(	fitness )
		div_log.append(	spherical.dissimilarity(stacked, len(stacked) ))
		con_log.append( spherical.sphericalPolygon_contains(stacked, 10) )
	# [END] Simulations ----------------------------------------------------------------------
	
	output = {}
	output['fit'] = fit_log
	output['div'] = div_log
	output['con'] = con_log
	return output
	##return [sum(convergence_log)/len(convergence_log), sum(elapsed_time_log)/(1.0*len(elapsed_time_log))]
## -------------------------------------------------------------------------------------------


### Over Mediocre Strategy 
def simulator_strategy(NodeCount, SearchRange, LearningRate, BehaviorParameter, \
			polar_upper_str = None, polar_lower_str = None, bridgeFlag = False, \
			fitness_known = 'Normal', fitness_alpha = None):
			#polar_upper = Angle_Upper_Bound, \
			#polar_lower = Angle_Lower_Bound): # azimuth_upper_ratio = None, azimuth_lower_ratio = 0):

	# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]
	#	1. NodeCount     := Indicates the number agents in the system (organization).
	#	2. SearchRange   := Represents the search range of each agent's learning activity.
	#						It is an upper limit of angle between two opinions.
	#	3. LearningRate  := Represents the learning rate of each agent.
	#						In this simulation, it is {25%, 50%, 75%}.
	#	4. Behavior      := Represents the degree of randomness in the learning process.
	#	5. InitCondition := Represents the type of knowledge initialization pattern.
			
	polar_upper = Angle_Upper_Bound
	polar_lower = Angle_Lower_Bound	
	if polar_upper_str != None:
		polar_upper = Approx_Angles_wPercentage[polar_upper_str]
	if polar_lower_str != None:
		polar_lower = Approx_Angles_wPercentage[polar_lower_str]

	initial_dissimil_log = []
	initial_contains_log = []
	convergence_log = []
	elapsed_time_log = []

	# [START] Simulations --------------------------------------------------------------------
	for instance in range(0, Instance_Count):
		## initialize market coordinate
		market = [0.0, 0.0]

		## initialize opinions
		opinion = opinion_init(NodeCount, polar_upper, polar_lower) #azimuth_upper_ratio, azimuth_lower_ratio)
		initial_dissimil = dissimilarity(opinion, NodeCount)
		initial_contians = sphericalPolygon_contains(opinion, NodeCount)
		initial_dissimil_log.append(initial_dissimil)
		initial_contains_log.append(initial_contians)

		performance_log = []
		flag = 0
		time = 0
		stop = False
		current_performance = [0]*NodeCount

		#if BehaviorParameter < 0.001:
		#	trackFile = open('./geonsik_result_track.txt', 'w')

		while(stop == False):
			# Step 1. Opinion Evaluation. ----------------------------------------------------
			performance_log.append(sum(current_performance)/((Max_Performance-Min_Performance)*NodeCount))
			for i in range(0, NodeCount):
				current_performance[i] = normal_performance(opinion[i])

			#----- PRINTING. 
#			if time == 0:
#				print "max!!", max(current_performance)/(Max_Performance-Min_Performance)
			#-----

			# Step 2. Learning. --------------------------------------------------------------
			new_opinion = [[0 for v1 in range(2)] for v2 in range(NodeCount)]
			for i in range(0, NodeCount):
				# Step 2-1. Search and assimilate to the best neighbor within a certain range.
				best_value = current_performance[i]
				best_index = i
				for j in range(0, NodeCount):
					if ( angle_between(opinion[i], opinion[j]) < SearchRange*math.pi ) \
						and current_performance[j] > best_value:
						best_value = current_performance[j]
						best_index = j
					if bridgeFlag == True \
						and angle_between(opinion[i], opinion[j]) > (7/8)*math.pi \
						and current_performance[j] > best_value:
						best_value = current_performance[j]
						best_index = j
				if i != best_index:
					new_opinion[i] = arc_splitpoint(opinion[i], opinion[best_index], LearningRate)
				else:
					new_opinion[i] = opinion[i]
				# Step 2-2. Add randomness (Perturbation).	
				for j in range(0, 2):
					new_opinion[i][j] += numpy.random.uniform(-BehaviorParameter, +BehaviorParameter)
				# Step 2-3. Standardize.
				new_opinion[i] = standardize(new_opinion[i])	
			opinion = copy.deepcopy(new_opinion)

			# Step 3. Record Time and Check Exit Condition. ----------------------------------
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
		##print "Convergence = ", org_performance, ",   Elapsed Time = ", time, ",   InitDiss = ", initial_dissimil
		print ",c(", org_performance, ", ", initial_dissimil, ")"
		convergence_log.append(org_performance)
		elapsed_time_log.append(time)
	# [END] Simulations ----------------------------------------------------------------------

	output = {}
	output['convergence'] = convergence_log
	output['elapsedTime'] = elapsed_time_log
	output['dissimilarity'] = initial_dissimil_log
	output['contains'] = initial_contains_log
	return output
	##return [sum(convergence_log)/len(convergence_log), sum(elapsed_time_log)/(1.0*len(elapsed_time_log))]
## -------------------------------------------------------------------------------------------

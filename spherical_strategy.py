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
for percentage in range(0, 51):
	x = numpy.arccos( erf(( percentage * 0.02 * ( Max_Performance - Min_Performance ) + Min_Performance -10 ) / math.sqrt(40/3)) )
	Approx_Angles_wPercentage[repr(percentage*2)+'%'] = numpy.round( x, 10 )
print Approx_Angles_wPercentage

# Static values (Hard-coded). ----------------------------------------------------------------
Number_Of_Candidates = 50
Org_Size = 10
Instance_Count = 200

def candidateSelect(Stacked, Candidates, Flag, GuessMarket):
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
			currentAvgFit += spherical.normal_performance(Stacked[i], GuessMarket)
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
		#divEval[i] = spherical.dissimilarity(temp, len(temp))
		fitEval[i] = spherical.normal_performance(Candidates[i], GuessMarket)
		#if divEval[i] > currentAvgDiv:
		#	all_negative_div = False
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
def simulator_strategy2suitability(strategy, polar_upper_str = None, polar_lower_str = None, market = [0.0, 0.0]):
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
		stacked = spherical.opinion_init(2, polar_upper, polar_lower)
		## initialize opinions
		candidates = spherical.opinion_init(500, polar_upper, polar_lower) #azimuth_upper_ratio, azimuth_lower_ratio)
		while len(stacked) != 10:
			#candidates = spherical.opinion_init(Number_Of_Candidates, polar_upper, polar_lower) #azimuth_upper_ratio, azimuth_lower_ratio)
			select = candidateSelect(stacked, candidates, strategy, market)
			stacked.append(candidates[select])
			candidates.remove(candidates[select])
		'''
		candidates = spherical.opinion_init(50, polar_upper, polar_lower) #azimuth_upper_ratio, azimuth_lower_ratio)
		while len(stacked) != 10:
			select = candidateSelect(stacked, candidates, strategy, market)
			stacked.append(candidates[select])
			candidates.remove(candidates[select])
		'''
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


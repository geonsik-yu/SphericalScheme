## -------------------------------------------------------------------------------------------
# This simulation scheme follows ISO spherical coordinate system convention.
#   - angle_t(theta) := polar angle     [0, pi]
#   - angle_p(phi)   := azimuth angle   [0, 2*pi] 
## -------------------------------------------------------------------------------------------

import copy
import math
import numpy
import random
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
## -------------------------------------------------------------------------------------------
# | General performance function for normal distribution is as follows:
# |	 >>
# |	 >>   Performance of Theta
# |	 >>     = mean + sqrt(2) * sigma * erfinv( cos(Theta) )
# |  >>   
# |  >>   Since James March's setting has approximately follows distribution of N(10, 20/3),
# |  >>   Performance of Theta
# |	 >>     = 10 + sqrt(40/3) * sigma * erfinv( cos(Theta) )
# |  >>
# |
# | Approximate maximum and minimum values achievable: [ -0.339866, 20.339866 ] 
# |  >>   
# |	 >> Max Performance = 10 + sqrt(40/3) * erfinv( cos( Smallest Angle Possible ) )
# |  >> Min Performance = 10 + sqrt(40/3) * erfinv( cos( Largest Angle Possible ) ) 
# |  >>                 = 10 - sqrt(40/3) * erfinv( cos( Smallest Angle Possible ) )  (* Use this one for balance.)
# |  >> 
# |
# | Approximate angle values for each percentiles are calculated as follows:
# |	 >>
# |  >>   Performance of x 
# |  >>     = 10 + sqrt(40/3) * erfinv( cos(x) ) 
# |	 >>
# |	 >>   Percentile of Performace Range (PPR)
# |	 >>     = Percentage * ( Max Performance - Min Performance ) + Min Performance
# |	 >>
# |  >>   x = erf( (-10 + PPR) / (sqrt(40/3)) )
# |	 >>
## -------------------------------------------------------------------------------------------



## Math functions ----------------------------------------------------------------------------
def normal_performance(opinion, market = [0,0]): 
	# Assume market := [0, 0]
	angle = None
	if market == [0,0]:
		angle = opinion[0]
	else:
		angle = angle_between(opinion, market)
	return 10 + math.sqrt(40/3)*erfinv( math.cos(angle) )

def upperDomeNormal_performance(opinion, alpha): 
	# Assume market := [0, 0]
	angle = opinion[0]
	if angle > numpy.arccos(2*alpha-1):
		return Min_Performance
	return 10 + math.sqrt(40/3)*erfinv( (math.cos(angle)-alpha)/(1-alpha) )

def lowerDomeNormal_performance(opinion, alpha): 
	# Assume market := [0, 0]
	angle = opinion[0]
	if angle < numpy.arccos(2*alpha-1):
		return Max_Performance		
	return 10 + math.sqrt(40/3)*erfinv( (math.cos(angle)-alpha+1)/(alpha) )


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
	mid_phi = numpy.arctan2(lin_mpt[1], lin_mpt[0]) ## [Important Note] Use arctan2!!
	return [mid_theta, mid_phi]

def arc_splitpoint(opinion_a, opinion_b, param):
	## Input: two spherical coordinates with unit length and a ratio parameter.
	## Learning function for organizational simulations.
	if param == 1: ## 12.5%, 1/8
		return arc_midpoint(opinion_a, arc_splitpoint(opinion_a, opinion_b, 2))
	elif param == 2: ## 25%, 2/8
		return arc_midpoint(opinion_a, arc_splitpoint(opinion_a, opinion_b, 4))
	elif param == 3: ## 37.5%, 3/8
		return arc_midpoint(arc_splitpoint(opinion_a, opinion_b, 2) \
							, arc_splitpoint(opinion_a, opinion_b, 4))
	elif param == 4: ## 50%, 4/8
		return arc_midpoint(opinion_a, opinion_b)
	elif param == 5: ## 62.5%, 5/8
		return arc_midpoint(arc_splitpoint(opinion_a, opinion_b, 4) \
							, arc_splitpoint(opinion_a, opinion_b, 6))
	elif param == 6: ## 75%, 6/8
		return arc_midpoint(arc_splitpoint(opinion_a, opinion_b, 4), opinion_b)
	elif param == 7: ## 87.5%, 7/8
		return arc_midpoint(arc_splitpoint(opinion_a, opinion_b, 6), opinion_b)

def angle_between(a, b):
	a = numpy.inner( spherical2cartesian(a), spherical2cartesian(b) )
	return numpy.arccos(a)

def dissimilarity(opinions, NodeCount):
	total_dissimil = 0
	for i in range(0, NodeCount):
		for j in range(i+1, NodeCount):
			total_dissimil += angle_between(opinions[i], opinions[j])
	return (total_dissimil*2) / (NodeCount*(NodeCount-1))

def sphericalPolygon_contains(opinions, NodeCount):
	## Suppose that target coordinate is (0,0,1)
	flag = False
	cart_ops = []
	for i in range(0, NodeCount):
		cart_ops.append(spherical2cartesian(opinions[i]))

	for i in range(0, NodeCount):
		for j in range(i+1, NodeCount):
			for k in range(j+1, NodeCount):
				A = numpy.array([ [cart_ops[i][0], cart_ops[j][0], cart_ops[k][0],  0] \
								, [cart_ops[i][1], cart_ops[j][1], cart_ops[k][1],  0] \
								, [cart_ops[i][2], cart_ops[j][2], cart_ops[k][2], -1] \
								, [             1,              1,              1,  0] \
								])
				b = numpy.array([0,0,0,1])
				x = numpy.linalg.solve(A, b)
				if(x[0] > 0 and x[1] > 0 and x[2] > 0 and x[3] > 0):
					return True
	return flag

def standardize(a):
	# Polar angle standardized into [0, pi].
	if a[0] > math.pi:
		a[0] = 2*math.pi - a[0]
	if a[0] < 0:
		a[0] = -a[0]
	# Azimuth angle standardized into [0, 2*pi].
	if a[1] > 2*math.pi:
		a[1] = a[1] - 2*math.pi
	if a[1] < 0:
		a[1] = 2*math.pi + a[1]
	# Apply upper/lower bounds.
	if a[0] < Angle_Lower_Bound:
		a[0] = Angle_Lower_Bound
	if a[0] > Angle_Upper_Bound:
		a[0] = Angle_Upper_Bound
	return a
## -------------------------------------------------------------------------------------------



## Simulation functions ----------------------------------------------------------------------
def opinion_init(number_of_nodes, polar_upper = Angle_Upper_Bound \
								, polar_lower = Angle_Lower_Bound):
	## azimuth_upper_ratio = None , azimuth_lower_ratio = 0):
	
	upper_in_U = 0.5*(numpy.cos(polar_lower) + 1)
	lower_in_U = 0.5*(numpy.cos(polar_upper) + 1)
	angle_t = numpy.arccos(2 * numpy.random.uniform(lower_in_U, upper_in_U, number_of_nodes) - 1)
	angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	'''
	angle_p = None
	if azimuth_upper_ratio == None:
		angle_p = 2 * math.pi * (numpy.random.uniform(0, 1, number_of_nodes))
	else:
		angle_p = 2 * math.pi * (numpy.random.uniform(azimuth_lower_ratio, azimuth_upper_ratio, number_of_nodes))
	'''
	## ---------------------------------------------------------------------------------------
	# | Random variable Theta and Phi that distributes points on the surface of a sphere uniformly 
	# | is as follows:
	# |	 >>
	# |	 >>   Theta = arccos( 2*U - 1 )   where U is an unit uniform random variable.
	# |	 >>   Phi   = 2 * pi * V          where V is an unit uniform random variable.
	# |  >>   
	## ---------------------------------------------------------------------------------------
	result = []
	for i in range(0, number_of_nodes):
		result.append([angle_t[i], angle_p[i]])
	return result

def simulator(NodeCount, SearchRange, LearningRate, BehaviorParameter, \
			polar_upper_str = None, polar_lower_str = None, bridgeFlag = False):
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

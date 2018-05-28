import numpy
import spherical
import spherical_strategy
import sys
import getopt


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
	##for BP in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.1, 0.15, 0.20, 0.25, 0.3, 0.35, 0.4]:
	##for BP in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]:
	##for BP in [0.0, 0.4, 0.8, 1.2, 1.6]:
	##for BP in [0.0]:

	##org_option = [30, 0.5, 2, 0, polar_upper_str = '70%']

	## --------------------------------------------------------------------------------------------
	if False: ## Experiment 1: Effect of Diversity
		for i in range(0,4):
			search = 0.25 + 0.25*i
			f = open('./geonsik_result_diversityEffect_sRange'+repr(search)+'.txt', 'w')
			result = spherical.simulator(10, search, 2, 0, polar_lower_str = '60%')

			a = result['convergence'] 
			b = result['elapsedTime'] 
			c = result['dissimilarity']
			d = result['contains']

			for i in range(0, 200):
				f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+","+repr(d[i])+'\n');
			f.close()
	## --------------------------------------------------------------------------------------------
	if False: ## Experiment 3: Effect of Learning Rate
		for L in range(1, 8):
			learning = L * 12.5
			f = open('./geonsik_result_learning'+repr(learning)+'.txt', 'w')
			result = spherical.simulator(10, 0.75, L, 0, polar_lower_str = '60%')

			a = result['convergence'] 
			b = result['elapsedTime'] 
			c = result['dissimilarity']
			d = result['contains']

			for i in range(0, 200):
				f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+","+repr(d[i])+'\n');
			f.close()

	## --------------------------------------------------------------------------------------------
	if False: ## Experiment 2: Effect of Bridge
		for i in range(0,2):
			search = 0.25 + 0.25*i
			f = open('./geonsik_result_BridgeEffect_sRange'+repr(search)+'.txt', 'w')
			result = spherical.simulator(10, search, 2, 0, polar_lower_str = '60%', bridgeFlag=True)

			a = result['convergence'] 
			b = result['elapsedTime'] 
			c = result['dissimilarity']
			d = result['contains']

			for i in range(0, 200):
				f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+","+repr(d[i])+'\n');
			f.close()

	## --------------------------------------------------------------------------------------------
	if False: ## Experiment 2: Effect of Search Range
		for BP in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]:
			for i in range(0,2):
				search = 0.25 + 0.25*i
				f = open('./geonsik_result_Randomness'+repr(BP)+'_sRange'+repr(search)+'.txt', 'w')
				## NodeCount, SearchRange, LearningRate, BehaviorParameter,
				## polar_upper_str = None, polar_lower_str = None, bridgeFlag = False
				
				## result = spherical.simulator(10, 0.75, 2, BP, polar_lower_str = '60%')
				result = spherical.simulator(10, search, 2, BP, polar_lower_str = '60%')

				a = result['convergence'] 
				b = result['elapsedTime'] 
				c = result['dissimilarity']
				d = result['contains']

				for i in range(0, 200):
					f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+","+repr(d[i])+'\n');
				f.close()

	## --------------------------------------------------------------------------------------------
	if False: ## Experiment 2: Lower Dome Normal Model
		for alpha in [0.2, 0.6]:
			search = 0.25 + 0.25*i
			f = open('./geonsik_result_LDN_alpha'+repr(alpha)+'.txt', 'w')
			## NodeCount, SearchRange, LearningRate, BehaviorParameter,
			## polar_upper_str = None, polar_lower_str = None, bridgeFlag = False
			
			## result = spherical.simulator(10, 0.75, 2, BP, polar_lower_str = '60%')
			result = spherical.simulator(10, search, 2, BP, polar_lower_str = '60%')
			a = result['convergence'] 
			b = result['elapsedTime'] 
			c = result['dissimilarity']
			d = result['contains']

			for i in range(0, 200):
				f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+","+repr(d[i])+'\n');
			f.close()

	## --------------------------------------------------------------------------------------------
	if False: ## Experiment 2: Upper Dome Normal Model
		for alpha in [0.2, 0.6]:
			search = 0.25 + 0.25*i
			f = open('./geonsik_result_UDN_alpha'+repr(alpha)+'.txt', 'w')
			## NodeCount, SearchRange, LearningRate, BehaviorParameter,
			## polar_upper_str = None, polar_lower_str = None, bridgeFlag = False
			
			## result = spherical.simulator(10, 0.75, 2, BP, polar_lower_str = '60%')
			result = spherical.simulator(10, search, 2, BP, polar_lower_str = '60%')
			a = result['convergence'] 
			b = result['elapsedTime'] 
			c = result['dissimilarity']
			d = result['contains']

			for i in range(0, 200):
				f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+","+repr(d[i])+'\n');
			f.close()

	if True:
	#	for strategy in ['r', 'd1', 'd2', 'f1', 'f2']:
	#	for strategy in ['d1', 'f1']:
		for strategy in ['f1']:
			for tilt in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2]:
				for upper in ['50%', '52%', '54%', '56%', '58%', '60%', '62%', '64%', '66%', '68%', '70%']:
				##for upper in ['50%', '60%', '70%', '80%', '90%']:
					f = open('./geonsik_result_strategyTilt_'+repr(tilt)+'_'+strategy+'_UboundFit'+repr(upper)+'.txt', 'w')
					result = spherical_strategy.simulator_strategy2suitability(strategy, polar_lower_str = upper, market=[tilt, 0.0])
					a = result['fit'] 
					b = result['div'] 
					c = result['con']
					for i in range(0, 200):
						f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+'\n');
					f.close()

	if False:
		for strategy in ['r', 'd1', 'd2', 'f1', 'f2']:
			for lower in ['0%', '10%', '20%', '30%', '40%']:
				f = open('./geonsik_result_strategy_'+strategy+'_LboundFit'+repr(lower)+'.txt', 'w')
				result = spherical_strategy.simulator_strategy2suitability(strategy, polar_upper_str = lower)
				a = result['fit'] 
				b = result['div'] 
				c = result['con']
				for i in range(0, 500):
					f.write(repr(a[i])+","+repr(b[i])+","+repr(c[i])+'\n');
				f.close()


	"""
	## --------------------------------------------------------------------------------------------
	if True: ## Experiment 1: Effect of Randomness
		L = 3
		for BP in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]:
			print BP
			for condition in [11, 4,5,6,7,9,10]:
				org_option = [40, 1, L, BP, condition]
				# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]

				result = spherical.simulator(org_option)
				f.write(repr(condition)+","+repr(BP)+","+repr(result[0])+","+repr(result[1])+'\n');
	## --------------------------------------------------------------------------------------------


	if True: ## Experiment 1: Effect of Randomness
		L = 3
		for BP in [0.0, 0.01, 0.02, 0.03, 0.04, 0.05]:
			print BP
			for condition in [11, 4,5,6,7,9,10]:
				org_option = [40, 1, L, BP, condition]
				# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]

				result = spherical.simulator(org_option)
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
	

	if False: ## Experiment 3: Value of 
		BP = 0
		L = 3
		for condition in [11, 4,5,6,7]:
			for searchRange in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]:
				org_option = [40, searchRange, L, BP, condition]
					# input_option := [NodeCount, SearchRange, LearningRate, Behavior, InitCondition]
				result = simulator(org_option)
				f.write(repr(condition)+","+repr(searchRange)+","+repr(result[0])+","+repr(result[1])+'\n');
	## --------------------------------------------------------------------------------------------
	"""


	
if __name__ == "__main__":
    main()
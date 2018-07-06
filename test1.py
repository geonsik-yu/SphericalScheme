import numpy
import spherical
import spherical_strategy
import sys
import getopt

## 
NodeCount = 30
opinion = spherical.opinion_init(NodeCount, 2.10, 0.01) #azimuth_upper_ratio, azimuth_lower_ratio)
for param in range(1, 8):
	for i in range(0, 30):
		for j in range(i, 30):
			a = spherical.arc_splitpoint_cont(opinion[i], opinion[j], param*12.5*0.01)
			b = spherical.arc_splitpoint(opinion[i], opinion[j], param)
			if spherical.angle_between(a, b) > 0.5:
				print param*12.5*0.01
				print a
				print b
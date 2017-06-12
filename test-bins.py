from math import ceil, floor
from palettable.cmocean.sequential import Thermal_20 #Amp_20, Dense_20
# https://jiffyclub.github.io/palettable/#documentation
# https://jiffyclub.github.io/palettable/colorbrewer/sequential/



N = 100
# reds = Amp_20.hex_colors
# blues = Dense_20.hex_colors
# reds_rev = list(reversed(reds))
# ncol = len(blues) + len(reds)

therm = Thermal_20.hex_colors
therm_rev = list(reversed(therm))
ncol = len(therm)


def initialize():
	# session['number'] = 17# random.randrange(0, N) # random number between 0-100
	# n = session['number']
	n = 17
	binsize = float(max(N, N-n)) / ncol

	bins = {}

	## add the left side bins
	x = max(n - binsize/2, 0) # start at the LHS of the bin that contains n
	# cols = reds_rev + blues
	cols = therm_rev
	j = 0
	while x > -binsize and j < len(cols):
		newbin = {(x, x+binsize): {'num': -j, 'color': cols[j]}}
		bins.update(newbin)
		
		j += 1
		x -= binsize

	## add the right side bins
	x = list(bins.keys())[0][1] # start at the LHS of the bin AFTER the bin that contains n
	# cols = reds_rev + blues
	j = 1 # start with the second darkest red
	while x < N+binsize and j < len(cols):
		newbin = {(x, x+binsize): {'num': j, 'color': cols[j]}}
		
		bins.update(newbin)
		
		j += 1
		x += binsize

	# renumber the bins starting from 0
	m = -1*min([v['num'] for v in bins.values()])
	
	for k, v in bins.items():
		v['num'] += m
		bins.update({k: v})

	return bins


def get_bin(guess, bins):
	
	return [{str(v['num']): v['color']} for k, v in bins.items() if guess >= k[0] and guess < k[1]][0]


bins = initialize()
print (sorted([v['num'] for v in bins.values()]))


guesses = [0, 16, 22, 40, 70, 100]
guessbar = {}
for guess in guesses:
	guessbin = get_bin(guess, bins)
	#add = {num: color}
	guessbar.update(guessbin)

print (guessbar)
# print(len(guessbar))
"""
print(0, get_color(0, bins))
print(16, get_color(16, bins))
print(22, get_color(22, bins))
print(40, get_color(40, bins))
print(70, get_color(70, bins))
print(100, get_color(100, bins))
"""
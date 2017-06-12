from flask import Flask, render_template, redirect, request, session
import random
from math import ceil, floor
from palettable.cmocean.sequential import Amp_10, Dense_10
# from palettable.cmocean.sequential import Thermal_20 
# https://jiffyclub.github.io/palettable/#documentation
# http://jiffyclub.github.io/palettable/cmocean/sequential/#thermal_7


app = Flask(__name__)

secretKey = open('secret-key.txt', 'r').read().strip()
app.secret_key = secretKey

N = 100

# therm = Thermal_20.hex_colors
# therm_rev = list(reversed(therm))
reds = Amp_10.hex_colors
blues = list(reversed(Dense_10.hex_colors))
therm = blues + reds
therm_rev = list(reversed(therm))
ncol = len(therm)

def initialize():
	
	n = 17 # random.randrange(0, N+1) # random number between 0-N
	binsize = float(max(N, N-n)) / ncol

	bins = {}

	## add the left side bins
	x = n - binsize/2 # start at the LHS of the bin that contains n
	# cols = reds_rev + blues
	cols = therm_rev
	j = 0
	while x > -binsize and j < len(cols):
		newbin = {str(-j): {'range': (x, x+binsize), 'color': cols[j], 'num': -j}}
		bins.update(newbin)
		
		j += 1
		x -= binsize

	## add the right side bins
	x = n + binsize/2
	# list(bins.keys())[0][1] # start at the LHS of the bin AFTER the bin that contains n
	# cols = reds_rev + blues
	j = 1 # start with the second darkest red
	while x < N+binsize and j < len(cols):
		newbin = {str(j): {'range': (x, x+binsize), 'color': cols[j], 'num': j}}
		
		bins.update(newbin)
		
		j += 1
		x += binsize

	# renumber the bins starting from 0 so that
	# you cant tell where the answer is
	m = -1*min([v['num'] for v in bins.values()])
	
	for k, v in bins.items():
		v['num'] += m
		bins.update({k: v})

	session['number'] = n
	session['bins'] = bins
	session['binnums'] = sorted([v['num'] for v in bins.values()])
	session['guesses'] = []
	session['guessbar'] = dict()
	session['win'] = False
	session['msg'] = ''
	
	

def get_bin(guess):	
	return [{str(v['num']): v['color']} for v in session['bins'].values()\
			if guess >= v['range'][0] and guess < v['range'][1]][0]



@app.route('/')
def index():
	
	try:
		n = session['number']
	except:
		initialize()


	params = {'guesses': str(session['guesses']),
			  'guessbar': str(session['guessbar']),
			   'binnums': session['binnums'],
			   'msg': session['msg']}
	return render_template('index.html', **params)



@app.route('/check', methods=['POST'])
def check():
	guess = request.form['guess']
	session['guesses'].append(guess)

	guessbar = session['guessbar']
	guessbar.update(get_bin(int(guess)))
	session['guessbar'] = guessbar
	
	if int(guess) == int(session['number']):
		session['win'] = True
		return redirect('/win')
	else:
		if int(guess) < int(session['number']):
			session['msg'] = guess + ': Too low'
		else:
			session['msg'] = guess + ': Too high'
		return redirect('/')

@app.route('/win')
def win():
	if session['win']:
		return render_template('win.html', n=session['number'],
			nguesses=len(session['guesses']))
	else:
		return redirect('/')

@app.route('/reveal', methods=['post'])
def reveal():
	"""
	# it will throw an error even without checking this, 
	# because if you navigate directly to this page,
	# there will be no post request, and that will upset it.
	try:
		request.form['giveup']
		n = session['number']
	except:
		n = 'Keep guessing!'"""

	n = session['number']
	return render_template('answer.html', n=n)

@app.route('/restart')
def restart():
	initialize()
	return redirect('/')

app.run(debug=True)

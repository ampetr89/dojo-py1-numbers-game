from flask import Flask, render_template, redirect, request, session
import random
from math import ceil, floor
from palettable.colorbrewer.sequential import PuRd_9
# https://jiffyclub.github.io/palettable/#documentation
# https://jiffyclub.github.io/palettable/colorbrewer/sequential/


app = Flask(__name__)

secretKey = open('secret-key.txt', 'r').read().strip()
app.secret_key = secretKey

N = 100
colors = PuRd_9.hex_colors
colors.reverse()
ncol = len(colors)


def initialize():
	session['number'] = 17# random.randrange(0, N) # random number between 0-100
	n = session['number']
	session['binSize'] = ceil( max(n, N-n)/ncol )
	session['nbins'] = ceil(float(N)/session['binSize'])
	session['guesses'] = []
	session['guessbar'] = dict()
	session['win'] = False
	session['msg'] = ''
	print (session['number'])

def get_color(guess):
	number = session['number']
	binSize = session['binSize']

	diff = float(abs(number - guess))
	binId = min(floor(diff/binSize), ncol - 1)

	return {str(binId): colors[binId]}



@app.route('/')
def index():
	
	try:
		n = session['number']
	except:
		initialize()


	params = {'guesses': str(session['guesses']),
			  'guessbar': str(session['guessbar']),
			   'nbins': session['nbins'],
			   'msg': session['msg']}
	return render_template('index.html', **params)



@app.route('/check', methods=['POST'])
def check():
	guess = request.form['guess']
	session['guesses'].append(guess)

	guessbar = session['guessbar']
	guessbar.update(get_color(int(guess)))
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
	try:
		request.form['giveup']
		n = session['number']
	except:
		n = 'Keep guessing!'

	return render_template('answer.html', n=n)

@app.route('/restart')
def restart():
	initialize()
	return redirect('/')

app.run(debug=True)

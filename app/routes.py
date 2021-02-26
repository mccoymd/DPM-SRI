from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    analysisOptions = {'simulate': 'Simulate a New Patient Population',
                       'analyze': 'Analyze an Existing Simulation',
                       'experiment': 'Analyze Experimental Data'} 
    return render_template('index.html',
                           title='Home',
                           analysisOptions=analysisOptions)


from flask import render_template
from app import app
from app.forms import Parameter2012Form

@app.route('/')
@app.route('/index')
def index():
    analysisOptions = {'simulate': 'Simulate a New Patient Population',
                       'analyze': 'Analyze an Existing Simulation',
                       'experiment': 'Review Experimental Data'} 
    return render_template('index.html',
                           title='DPM-SRI',
                           analysisOptions=analysisOptions)


@app.route('/analyze')
def analyze():
    title = 'Analyze an Existing Simulation'
    form = Parameter2012Form()
    return render_template('analyze.html', title=title, form=form)

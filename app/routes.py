from flask import render_template, redirect
from app import app
from app.forms import PNAS2012_InputParamsForm, PNAS2012_FullParamsForm, PNAS2012_OutcomeFilterForm, PNAS2012_StrategiesForm
import os

@app.route('/')
@app.route('/index')
def index():
    analysisOptions = {'simulate': 'Simulate a New Patient Population',
                       'analyze': 'Analyze an Existing Simulation',
                       'experiment': 'Review Experimental Data'} 
    return render_template('index.html',
                           title='DPM-SRI',
                           analysisOptions=analysisOptions)

@app.route('/notConfigured')
def notConfigured():
    return render_template('notConfigured.html')

@app.route('/analyzeSim')
def analyzeSim():
    return render_template('analyzeSim.html')

@app.route('/selectPNAS2012_OutcomeFilter', methods=['GET','POST'])
def selectPNAS2012_OutcomeFilter():
    form = PNAS2012_OutcomeFilterForm()
    if form.validate_on_submit():
        #get patient table based on query and save as "./data/appData/outcomes.csv"
        commandString = "Rscript ./app/bin/filterPatient_byOutcome.R " + str(form.baseSurvival_min.data) + " " + str(form.baseSurvival_max.data)
        print(commandString)
        os.system(commandString)
        #option to also filter by parameters
        if form.filterParameters.data:
            #return redirect('/selectPNAS2012_FullParams')
            return redirect('/notCongifured')
        else:
            return redirect('/selectPNAS2012_SelectAnalysis')
    
    return render_template('selectPNAS2012_OutcomeFilter.html',form=form)



@app.route('/selectPNAS2012_InputParams')
def selectPNAS2012_InputParams():
    title = 'Analyze an Existing Simulation'
    form = PNAS2012_InputParamsForm()
    return render_template('selectPNAS2012_InputParams.html', title=title, form=form)

@app.route('/selectPNAS2012_FullParams')
def selectPNAS2012_FullParams():
    title = 'Analyze an Existing Simulation'
    form = PNAS2012_FullParamsForm()
    return render_template('selectPNAS2012_FullParams.html', title=title, form=form)

@app.route('/selectPNAS2012_SelectAnalysis')
def selectStrategy():
    form = PNAS2012_StrategiesForm()
    return render_template('selectPNAS2012_SelectAnalysis.html',form=form)


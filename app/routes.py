from flask import render_template, redirect
from app import app
from app.forms import PNAS2012_InputParamsForm, PNAS2012_FullParamsForm, PNAS2012_OutcomeFilterForm, PNAS2012_StrategiesForm
import os


@app.route('/')
@app.route('/index')
def index():

    sriOptions = {'Define a simulated patient population': 'selectModel',
                  'Review Experimental Data (NOT CONFIGURED)': 'selectExperiment'}


#testing functionality
#    analysisOptions_proj = {}
#    projects = os.listdir('app/projects')
#    print(projects)
#    for curr_project in projects:
#        desc_filename = os.path.join('app/projects/',curr_project,'description.txt')
#        if os.path.isfile(desc_filename):
#            with open(desc_filename,'r') as file:
#                desc = file.read()
#                print(desc)
#                analysisOptions_proj[curr_project] = desc
#remove once projects are configured

    return render_template('index.html',
                           title='DPM-SRI',
#                           analysisOptions_proj=analysisOptions_proj,
                           sriOptions=sriOptions)

@app.route('/selectModel')
def selectModel():
    modelTypes = {'PNAS 2012 Evolutionary Model':'parameterizePNAS2012',
                  'Short Term Plastisity (NOT CONFIGURED)':'notConfigured'}
    
    return render_template('selectModel.html',
                           modelTypes=modelTypes)

@app.route('/selectExperiment')
def selectExperiment():
    experimentTypes = {'DOD Hypermutation Cell Proliferation':'hypermutation',
                       'Panc Digital Twins':'notConfigured'}
    
    return render_template('notConfigured.html')

@app.route('/parameterizePNAS2012')
def parameterizePNAS2012():
    paramOptions = {'Filter by outcomes in simulated patient database':'selectPNAS2012_OutcomeFilter',
                    'PNAS 2012 Simplifying Assumptions':'selectPNAS2012_InputParams',
                    'Full PNAS 2012 Parameter Set':'selectPNAS2012_FullParams',
                    'Panc Digital Twins':'notConfigured'}
    return render_template('parameterizePNAS2012.html',
                           paramOptions=paramOptions)


@app.route('/selectPNAS2012_OutcomeFilter', methods=['GET','POST'])
def selectPNAS2012_OutcomeFilter():
    form = PNAS2012_OutcomeFilterForm()


    form.strategySelection.choices = [('strategy-0','Full Treatment with Standard Precision Medicine (Strategy 0 PNAS2012)'),
                                      ('strategy-22trial','First 2 Treatment Selections with DPM (Strategy 2.2 PNAS2012)'),
                                      ('strategy-22','Full Treatment with DPM (Strategy 2.2 PNAS2012)')]
    form.trialOutcomeSelection.choices = [('bothSame','Recommendations matched for BOTH evaluation windows'),
                                          ('firstSame','Recommendations matched for FIRST evaluation only'),
                                          ('secondSame','Recommendation matched for SECOND evaluation only'),
                                          ('bothDiff','Recommendation matched for NO evaluation windows')]

    #make this a dynamic selection based on uses input??
    databasePath = './app/data/database/PNAS2012/'
    outcomeReferenceStrategy = "strategy-0" #add option to use strategy-22trial and strategy-22
    outcomeTable = databasePath + "allPatientSurvival_" + outcomeReferenceStrategy +".csv"
    sessionOutcomesTable = './app/data/appData/outcomes.csv'
    
    if form.validate_on_submit():
        #get patient table based on query and save
        filterByOutcomeCommand = "Rscript ./app/bin/filterPatient_byOutcome.R " + \
                                 str(form.baseSurvival_min.data) + " " + \
                                 str(form.baseSurvival_max.data) + " " + \
                                 outcomeTable + " " + \
                                 sessionOutcomesTable
        print(filterByOutcomeCommand)
#        os.system(filterByOutcomeCommand)

        
        strategyString = ''
        if len(form.strategySelection.data) < 1:
            for x,y in form.strategySelection.choices:
                strategyString = x + " " + strategyString
        else:
            for x in form.strategySelection.data:
                strategyString = x + " " + strategyString

        print(strategyString)

#        print(len(form.strategySelection.data), form.trialOutcomeSelection.data, form.baseSurvival_min.data, form.baseSurvival_max.data)        
        #option to also filter by parameters
        if form.filterParameters.data:
            #return redirect('/selectPNAS2012_FullParams')
            return redirect('/notCongifured')
        else:

            return redirect('/notConfigured')#setup to select analysis options for R plots
    
    return render_template('selectPNAS2012_OutcomeFilter.html',form=form)


@app.route('/notConfigured')
def notConfigured():
    return render_template('notConfigured.html')



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

@app.route('/analyzeSim')
def analyzeSim():
    return render_template('analyzeSim.html')

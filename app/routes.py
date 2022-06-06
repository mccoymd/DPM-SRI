from flask import render_template, redirect, url_for
from app import app, db, models
from app.forms import PNAS2012_InputParamsForm, PNAS2012_FullParamsForm, PNAS2012_OutcomeFilterForm, PNAS2012_StrategiesForm
import os
import pandas as pd

@app.route('/')
@app.route('/index')
def index():

    sriOptions = {'Analyze simulated patient populations': 'selectModel',
                  'Review Experimental Data (NOT CONFIGURED)': 'selectExperiment'}

    return render_template('index.html',
                           title='DPM-SRI',
                           sriOptions=sriOptions)

@app.route('/selectModel')
def selectModel():
    modelTypes = {'PNAS 2012 Evolutionary Model':'parameterizePNAS2012',
                  'Generalized Multi-Drug Model (NOT CONFIGURED)':'notConfigured',
                  'Short Term Plastisity (NOT CONFIGURED)':'notConfigured'}

    return render_template('selectModel.html',
                           modelTypes=modelTypes)

@app.route('/selectExperiment')
def selectExperiment():
    experimentTypes = {'DOD Hypermutation Cell Proliferation':'hypermutation',
                       'Panc Digital Twins':'notConfigured'}

    return render_template('notConfigured.html',errorString='upload experimental data to be mapped to semi-automated parameter selection')

@app.route('/parameterizePNAS2012')
def parameterizePNAS2012():
    paramOptions = {'Filter by outcomes (Simulated DPM Trial)':'selectPNAS2012_OutcomeFilter',
                    'Filter by outcomes (Panc Digital Twins)':'selectPNAS2012_PancDT',
                    'Filter by input parameters (PNAS 2012 Simplifying Assumptions)':'selectPNAS2012_InputParams',
                    'Filter by input parameters (PNAS 2012 Full Parameter Set)':'selectPNAS2012_FullParams'}

    return render_template('parameterizePNAS2012.html',
                           paramOptions=paramOptions)


@app.route('/selectPNAS2012_OutcomeFilter', methods=['GET','POST'])
def selectPNAS2012_OutcomeFilter():
    form = PNAS2012_OutcomeFilterForm()

    #configure all choices TODO: configure to read from a DB metadata file
    # set DB path TODO: make this a dynamic selection based on available DB
    databasePath = './app/data/database/PNAS2012/'
    outcomesTable = databasePath + 'allPatientSurvival.csv'
    trialResultsTable = databasePath + 'allPatientTrialResults.csv'

    form.strategySelection.choices = [('strategy0','Full Treatment with Standard Precision Medicine (Strategy 0 PNAS2012)'),
                                      ('strategy22trial','First 2 Treatment Selections with DPM (Strategy 2.2 PNAS2012)'),
                                      ('strategy22','Full Treatment with DPM (Strategy 2.2 PNAS2012)')]
    form.trialOutcomeSelection.choices = [('bothSame','Recommendations matched for BOTH evaluation windows'),
                                          ('firstSame','Recommendations matched for FIRST evaluation only'),
                                          ('secondSame','Recommendation matched for SECOND evaluation only'),
                                          ('bothDiff','Recommendation matched for NO evaluation windows')]

    if form.validate_on_submit():
        survivalTable = pd.read_csv(outcomesTable)
        trialResults = pd.read_csv(trialResultsTable)

        # get patient table based on query and save
        strategySelection = form.strategySelection.data
        trialGroups = form.trialOutcomeSelection.data

        # filtering on strategy 0 outcomes TODO: filter on other strategy outcomes?
        survivalTable = survivalTable[survivalTable.strategy0 >= form.baseSurvival_min.data]
        survivalTable = survivalTable[survivalTable.strategy0 <= form.baseSurvival_max.data]

        # filtering by strategies based on user input
        if not strategySelection:
            print('comparing all strategies')
        else:
            print('filtering by selected strategies')
            strategySelection.insert(0,'paramID')
            survivalTable = survivalTable[strategySelection]


        # filtering based on trail results
        if not trialGroups:
            print('using all trial results')
        else:
            print('filtering by trial results')
            trialParamIDs = trialResults[trialResults['Category'].isin(trialGroups)].paramID
            survivalTable = survivalTable[survivalTable['paramID'].isin(trialParamIDs)]

        # adding trail results and filtering
        survivalTable = survivalTable.merge(trialResults,on='paramID')

        print(trialResults.shape,'\n',trialResults.head())
        print(survivalTable.shape[0],'\n',survivalTable.head())

        # TODO add option to also filter by parameters
        if not form.filterParameters.data:
            return redirect('/analyzePNAS2012')
        else:
            return redirect('/selectPNAS2012_filterOutcomeParameters')


    return render_template('selectPNAS2012_OutcomeFilter.html',form=form)

@app.route('/analyzePNAS2012')
def analyzePNAS2012():
    # TODO want to read the strategies and categories
    # list analysis options
    # add code to generate KM plots and others
    errorString = 'setup to select analysis options for R plots'
    return render_template('notConfigured.html',errorString=errorString)


@app.route('/selectPNAS2012_PancDT', methods = ['GET','POST'])
def selectPNAS2012_PancDT():
    return render_template('selectPNAS2012_PancDT.html')

@app.route('/selectPNAS2012_InputParams', methods=['GET','POST'])
def selectPNAS2012_InputParams():
    title = 'Analyze an Existing Simulation'
    form = PNAS2012_InputParamsForm()

    return render_template('selectPNAS2012_InputParams.html', title=title, form=form)

@app.route('/selectPNAS2012_FullParams', methods=['GET','POST'])
def selectPNAS2012_FullParams():
    title = 'Analyze an Existing Simulation'
    form = PNAS2012_FullParamsForm()
    return render_template('selectPNAS2012_FullParams.html', title=title, form=form)

@app.route('/selectPNAS2012_filterOutcomeParameters')
def selectPNAS2012_filterOutcomeParameters():
    errorString = 'filter the session outcome table by input parameters'
    return render_template('notConfigured.html',errorString=errorString)

@app.route('/notConfigured')
def notConfigured():
    errorString='Email mdm299@georgetown.edu for current status'
    return render_template('notConfigured.html',errorString=errorString)

@app.route('/results', methods=['POST'])
def results():
    form = PNAS2012_InputParamsForm()
    if form.validate_on_submit():
        field_names = ['growth_rate']
        results = db.session.\
                query(models.Parameters, models.DrugSensitivities).\
                join(models.Parameters, \
                models.Parameters.drug_sensitivities_id == \
                models.DrugSensitivities.id).\
                where(models.Parameters.growth_rate <= form.growthRate_max.data).\
                limit(5)
        return render_template('renderResults.html', results=results)
    else:
        print("AAAAAAAAA")
        return redirect('/notConfigured')

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


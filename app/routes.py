from flask import render_template, redirect, url_for, request
from app import app, db, models, utils
from app.forms import (
    PNAS2012_InputParamsForm,
    PNAS2012_FullParamsForm,
    PNAS2012_OutcomeFilterForm,
    PNAS2012_StrategiesForm,
    Upload_ResultsForm,
)
from app.models import (
    Parameters,
    Populations,
    DrugDosages,
    StoppingTimes,
    InitialPopulations,
    DrugSensitivities,
    TransitionRates,
)
from app.utils import file_transform
from werkzeug.utils import secure_filename
import os
import pandas as pd


@app.route("/")
@app.route("/index")
def index():

    sriOptions = {
        "Analyze simulated patient populations": "selectModel",
#        "Review Experimental Data (NOT CONFIGURED)": "selectExperiment",
        "Upload Simulation Results": "uploadResults",
    }

    return render_template("index.html", title="DPM-SRI", sriOptions=sriOptions)


@app.route("/selectModel")
def selectModel():
    modelTypes = {
        "Analyze 2 Drug Trial Simulation": "parameterizePNAS2012",
        "Simulate New Digital Twins": "notConfigured",
#        "Short Term Plastisity (NOT CONFIGURED)": "notConfigured",
    }

    return render_template("selectModel.html", modelTypes=modelTypes)


@app.route("/selectExperiment")
def selectExperiment():
    experimentTypes = {
        "DOD Hypermutation Cell Proliferation": "hypermutation",
        "Panc Digital Twins": "notConfigured",
    }

    return render_template(
        "notConfigured.html",
        errorString="upload experimental data to be mapped to semi-automated parameter selection",
    )


@app.route("/parameterizePNAS2012")
def parameterizePNAS2012():
    paramOptions = {
        "Filter by outcomes (Simulated DPM Trial)": "selectPNAS2012_OutcomeFilter",
        #"Filter by outcomes (Panc Digital Twins)": "selectPNAS2012_PancDT",
        "Filter by input parameters (PNAS 2012 Simplifying Assumptions)": "selectPNAS2012_InputParams",
        "Filter by input parameters (PNAS 2012 Full Parameter Set)": "selectPNAS2012_FullParams",
    }

    return render_template("parameterizePNAS2012.html", paramOptions=paramOptions)


@app.route("/selectPNAS2012_OutcomeFilter", methods=["GET", "POST"])
def selectPNAS2012_OutcomeFilter():
    form = PNAS2012_OutcomeFilterForm()

    # configure all choices TODO: configure to read from a DB metadata file
    # set DB path TODO: make this a dynamic selection based on available DB
    databasePath = "./app/data/database/PNAS2012/"
    outcomesTable = databasePath + "allPatientSurvival.csv"
    trialResultsTable = databasePath + "allPatientTrialResults.csv"

    form.strategySelection.choices = [
        (
            "strategy0",
            "Full Treatment with Standard Precision Medicine (Strategy 0 PNAS2012)",
        ),
        (
            "strategy22trial",
            "First 2 Treatment Selections with DPM (Strategy 2.2 PNAS2012)",
        ),
        ("strategy22", "Full Treatment with DPM (Strategy 2.2 PNAS2012)"),
    ]
    form.trialOutcomeSelection.choices = [
        ("bothSame", "Recommendations matched for BOTH evaluation windows"),
        ("firstSame", "Recommendations matched for FIRST evaluation only"),
        ("secondSame", "Recommendation matched for SECOND evaluation only"),
        ("bothDiff", "Recommendation matched for NO evaluation windows"),
    ]

    if form.validate_on_submit():
        survivalTable = pd.read_csv(outcomesTable)
        trialResults = pd.read_csv(trialResultsTable)

        # get patient table based on query and save
        strategySelection = form.strategySelection.data
        trialGroups = form.trialOutcomeSelection.data

        # filtering on strategy 0 outcomes TODO: filter on other strategy outcomes?
        survivalTable = survivalTable[
            survivalTable.strategy0 >= form.baseSurvival_min.data
        ]
        survivalTable = survivalTable[
            survivalTable.strategy0 <= form.baseSurvival_max.data
        ]

        # filtering by strategies based on user input
        if not strategySelection:
            print("comparing all strategies")
        else:
            print("filtering by selected strategies")
            strategySelection.insert(0, "paramID")
            survivalTable = survivalTable[strategySelection]

        # filtering based on trail results
        if not trialGroups:
            print("using all trial results")
        else:
            print("filtering by trial results")
            trialParamIDs = trialResults[
                trialResults["Category"].isin(trialGroups)
            ].paramID
            survivalTable = survivalTable[survivalTable["paramID"].isin(trialParamIDs)]

        # adding trail results and filtering
        survivalTable = survivalTable.merge(trialResults, on="paramID")

        print(trialResults.shape, "\n", trialResults.head())
        print(survivalTable.shape[0], "\n", survivalTable.head())

        # TODO add option to also filter by parameters
        if not form.filterParameters.data:
            return redirect("/analyzePNAS2012")
        else:
            return redirect("/selectPNAS2012_filterOutcomeParameters")

    return render_template("selectPNAS2012_OutcomeFilter.html", form=form)


@app.route("/analyzePNAS2012")
def analyzePNAS2012():
    # TODO want to read the strategies and categories
    # list analysis options
    # add code to generate KM plots and others
    errorString = "setup to select analysis options for R plots"
    return render_template("notConfigured.html", errorString=errorString)


@app.route("/selectPNAS2012_PancDT", methods=["GET", "POST"])
def selectPNAS2012_PancDT():
    return render_template("selectPNAS2012_PancDT.html")


@app.route("/selectPNAS2012_InputParams", methods=["GET", "POST"])
def selectPNAS2012_InputParams():
    title = "Analyze an Existing Simulation"
    form = PNAS2012_InputParamsForm()

    return render_template("selectPNAS2012_InputParams.html", title=title, form=form)


@app.route("/selectPNAS2012_FullParams", methods=["GET", "POST"])
def selectPNAS2012_FullParams():
    title = "Analyze an Existing Simulation"
    form = PNAS2012_FullParamsForm()
    return render_template("selectPNAS2012_FullParams.html", title=title, form=form)


@app.route("/selectPNAS2012_filterOutcomeParameters")
def selectPNAS2012_filterOutcomeParameters():
    errorString = "filter the session outcome table by input parameters"
    return render_template("notConfigured.html", errorString=errorString)


@app.route("/notConfigured")
def notConfigured():
    errorString = "Email mdm299@georgetown.edu for current status"
    return render_template("notConfigured.html", errorString=errorString)


@app.route("/results", methods=["POST"])
def results():
    form = PNAS2012_InputParamsForm()
    if form.validate_on_submit():
        results = (
            db.session.query(Parameters, InitialPopulations, TransitionRates, DrugSensitivities)
            .join(Parameters, Parameters.initial_subclone_population_id == InitialPopulations.id)
            .join(Parameters, Parameters.evolutionary_rates_id == TransitionRates.id)
            .join(Parameters, Parameters.drug_sensitivities_id == DrugSensitivities.id)
            .where(Parameters.growth_rate <= form.growthRate_max.data)
            .count()
        )
        return render_template("renderResults.html", results=results)
    else:
        print(form.errors)
        return redirect("/notConfigured")


@app.route("/uploadResults", methods=["GET", "POST"])
def uploadResults():
    form = Upload_ResultsForm()

    if form.validate_on_submit():
        files_dict = {"dosage": None, "param": None, "pop": None, "stopt": None}
        file_ids = set([])
        files = form.documents.data

        for f in files:
            filename = secure_filename(f.filename)
            split = os.path.splitext(filename)
            extension = split[1]

            if (extension != ".txt") and (extension != ".csv"):
                return render_template("uploadResults.html", form=form, file_error="Invalid file type, only csv and txt accepted")

            name_split = split[0].split("_")
            file_type = name_split[0]

            if "param" in file_type:
                files_dict["param"] = f
            elif "stopt" in file_type:
                files_dict["stopt"] = f
            elif "dosage" in file_type:
                files_dict["dosage"] = f
            elif "pop" in file_type:
                files_dict["pop"] = f
            else:
                return render_template("uploadResults.html", form=form, file_error="Invalid file name found: {0}".format(filename))

            file_id = name_split[2]
            file_ids.add(file_id)

        if len(file_ids) > 1:
            return render_template("uploadResults.html", form=form, file_error="Found multiple ids but expected 1: {0}".format(file_ids))

        values_set = set(files_dict.values())
        if (len(values_set) != 4) or (None in values_set):
            return render_template("uploadResults.html", form=form, file_error="Expected params, dosage, stopping times, and population files but found: {0}".format(values_set))

        process_file(files_dict["param"])
        process_file(files_dict["stopt"])
        process_file(files_dict["dosage"])
        process_file(files_dict["pop"])

        return redirect(url_for("uploadResults"))
    else:
        print(form.errors)

    return render_template("uploadResults.html", form=form)

def process_file(f):
    filename = secure_filename(f.filename)

    if f.filename != "":
        inputFile = os.path.join(app.config["UPLOAD_PATH"], filename)
        f.save(inputFile)
        split = os.path.splitext(filename)
        name = split[0]
        extension = split[1]

        if extension == ".txt":
            output = os.path.join(app.config["UPLOAD_PATH"], name) + ".csv"
            file_transform.convert_txt(inputFile, output)
            os.remove(inputFile)
            inputFile = output

        file_transform.process_file(inputFile, name)
        os.remove(inputFile)  #keep file for certain amount of time before deleting?

# testing functionality
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
# remove once projects are configured

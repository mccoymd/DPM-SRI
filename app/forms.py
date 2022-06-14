from flask_wtf import FlaskForm
#from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import (
    SubmitField,
    DecimalField,
    FloatField,
    StringField,
    BooleanField,
    SelectMultipleField,
    MultipleFileField,
)
from wtforms.validators import DataRequired, InputRequired


class PNAS2012_OutcomeFilterForm(FlaskForm):
    filterParameters = BooleanField("Check if also filtering by parameters")
    baseSurvival_min = FloatField(
        "Survival Range (days) on Standard Precision Medicine", default=0.0
    )
    baseSurvival_max = FloatField(
        "Survival Range (days) on Standard Precision Medicine",
        default=1845.0,
        validators=[DataRequired()],
    )
    strategySelection = SelectMultipleField(
        "Select Available Strategies (hold control for multiple)"
    )
    trialOutcomeSelection = SelectMultipleField(
        "Select Trial Outcomes (hold control for multiple)"
    )
    submit = SubmitField("Submit Parameters")


class PNAS2012_InputParamsForm(FlaskForm):
    R1popRatio_min = FloatField(
        "R1 Population Ratio", default=0, validators=[InputRequired()]
    )
    R1popRatio_max = FloatField(
        "R1 Population Ratio", default=0.9, validators=[InputRequired()]
    )
    R2popRatio_min = FloatField(
        "R2 Population Ratio", default=0, validators=[InputRequired()]
    )
    R2popRatio_max = FloatField(
        "R2 Population Ratio", default=0.9, validators=[InputRequired()]
    )
    growthRate_min = FloatField(
        "Growth Rate", default=0.001, validators=[InputRequired()]
    )
    growthRate_max = FloatField(
        "Growth Rate", default=0.34, validators=[InputRequired()]
    )
    S_D1senRatio_min = FloatField(
        "Sensitivity of S to D1 relative to growth rate",
        default=0.000560,
        validators=[InputRequired()],
    )
    S_D1senRatio_max = FloatField(
        "Sensitivity of S to D1 relative to growth rate",
        default=440,
        validators=[InputRequired()],
    )
    S_D2senRatio_min = FloatField(
        "Sensitivity of S to D2 relative to sensitivity to D1",
        default=0.0004,
        validators=[InputRequired()],
    )
    S_D2senRatio_max = FloatField(
        "Sensitivity of S to D2 relative to sensitivity to D1",
        default=1,
        validators=[InputRequired()],
    )
    R1_D1senRatio_min = FloatField(
        "Sensitivity of R1 to D1 over sensitivity of S to D1",
        default=0,
        validators=[InputRequired()],
    )
    R1_D1senRatio_max = FloatField(
        "Sensitivity of R1 to D1 over sensitivity of S to D1",
        default=0.8,
        validators=[InputRequired()],
    )
    R2_D2senRatio_min = FloatField(
        "Sensitivity of R2 to D2 over the sensitivity of S to D2",
        default=0,
        validators=[InputRequired()],
    )
    R2_D2senRatio_max = FloatField(
        "Sensitivity of R2 to D2 over the sensitivity of S to D2",
        default=0.8,
        validators=[InputRequired()],
    )
    S_to_R1_min = FloatField(
        "S transition to R1", default=0.00000000001, validators=[InputRequired()]
    )
    S_to_R1_max = FloatField(
        "S transition to R1", default=0.001, validators=[InputRequired()]
    )
    S_to_R2_min = FloatField(
        "S transition to R2", default=0.00000000001, validators=[InputRequired()]
    )
    S_to_R2_max = FloatField(
        "S transition to R2", default=0.001, validators=[InputRequired()]
    )
    submit = SubmitField("Submit Parameters")


class PNAS2012_FullParamsForm(FlaskForm):
    Spop_min = FloatField("S Population", validators=[DataRequired()])
    Spop_max = FloatField("S Population", validators=[DataRequired()])
    R1pop_min = FloatField("R1 Population", validators=[DataRequired()])
    R1pop_max = FloatField("R1 Population", validators=[DataRequired()])
    R2pop_min = FloatField("R2 Population", validators=[DataRequired()])
    R2pop_max = FloatField("R2 Population", validators=[DataRequired()])
    R12pop_min = FloatField("R12 Population", validators=[DataRequired()])
    R12pop_max = FloatField("R12 Population", validators=[DataRequired()])
    growthRate_min = FloatField("Growth Rate", validators=[DataRequired()])
    growthRate_max = FloatField("Growth Rate", validators=[DataRequired()])
    S_D1sensitivity_min = FloatField(
        "Base D1 sensitiviety", validators=[DataRequired()]
    )
    S_D1sensitivity_max = FloatField(
        "Base D1 sensitiviety", validators=[DataRequired()]
    )
    S_D2sensitivity_min = FloatField(
        "Base D2 sensitiviety", validators=[DataRequired()]
    )
    S_D2sensitivity_max = FloatField(
        "Base D2 sensitiviety", validators=[DataRequired()]
    )
    R1_D1sensitivity_min = FloatField("R1 D1 sensitiviety", validators=[DataRequired()])
    R1_D1sensitivity_max = FloatField("R1 D1 sensitiviety", validators=[DataRequired()])
    R1_D2sensitivity_min = FloatField("R1 D2 sensitiviety", validators=[DataRequired()])
    R1_D2sensitivity_max = FloatField("R1 D2 sensitiviety", validators=[DataRequired()])
    R2_D1sensitivity_min = FloatField("R2 D1 sensitiviety", validators=[DataRequired()])
    R2_D1sensitivity_max = FloatField("R2 D1 sensitiviety", validators=[DataRequired()])
    R2_D2sensitivity_min = FloatField("R2 D2 sensitiviety", validators=[DataRequired()])
    R2_D2sensitivity_max = FloatField("R2 D2 sensitiviety", validators=[DataRequired()])
    R12_D1sensitivity_min = FloatField(
        "R12 D1 sensitiviety", validators=[DataRequired()]
    )
    R12_D1sensitivity_max = FloatField(
        "R12 D1 sensitiviety", validators=[DataRequired()]
    )
    R12_D2sensitivity_min = FloatField(
        "R12 D2 sensitiviety", validators=[DataRequired()]
    )
    R12_D2sensitivity_max = FloatField(
        "R12 D2 sensitiviety", validators=[DataRequired()]
    )
    S_to_S_min = FloatField("S Self Transition", validators=[DataRequired()])
    S_to_S_max = FloatField("S Self Transition", validators=[DataRequired()])
    S_to_R1_min = FloatField("S transition to R1", validators=[DataRequired()])
    S_to_R1_max = FloatField("S transition to R1", validators=[DataRequired()])
    S_to_R2_min = FloatField("S transition to R2", validators=[DataRequired()])
    S_to_R2_max = FloatField("S transition to R2", validators=[DataRequired()])
    S_to_R12_min = FloatField("S transition to R12", validators=[DataRequired()])
    S_to_R12_max = FloatField("S transition to R12", validators=[DataRequired()])
    R1_to_S_min = FloatField("R1 transition to S", validators=[DataRequired()])
    R1_to_S_max = FloatField("R1 transition to S", validators=[DataRequired()])
    R1_to_R1_min = FloatField("R1 self Transition", validators=[DataRequired()])
    R1_to_R1_max = FloatField("R1 self Transition", validators=[DataRequired()])
    R1_to_R2_min = FloatField("R1 transition to R2", validators=[DataRequired()])
    R1_to_R2_max = FloatField("R1 transition to R2", validators=[DataRequired()])
    R1_to_R12_min = FloatField("R1 transition to R12", validators=[DataRequired()])
    R1_to_R12_max = FloatField("R1 transition to R12", validators=[DataRequired()])
    R2_to_S_min = FloatField("R2 transition to S", validators=[DataRequired()])
    R2_to_S_max = FloatField("R2 transition to S", validators=[DataRequired()])
    R2_to_R1_min = FloatField("R2 transition to R1", validators=[DataRequired()])
    R2_to_R1_max = FloatField("R2 transition to R1", validators=[DataRequired()])
    R2_to_R2_min = FloatField("R2 self transition", validators=[DataRequired()])
    R2_to_R2_max = FloatField("R2 self transition", validators=[DataRequired()])
    R2_to_R12_min = FloatField("R2 transition to R12", validators=[DataRequired()])
    R2_to_R12_max = FloatField("R2 transition to R12", validators=[DataRequired()])
    R12_to_S_min = FloatField("R12 transition to S", validators=[DataRequired()])
    R12_to_S_max = FloatField("R12 transition to S", validators=[DataRequired()])
    R12_to_R1_min = FloatField("R12 transition to R1", validators=[DataRequired()])
    R12_to_R1_max = FloatField("R12 transition to R1", validators=[DataRequired()])
    R12_to_R2_min = FloatField("R12 transition to R2", validators=[DataRequired()])
    R12_to_R2_max = FloatField("R12 transition to R2", validators=[DataRequired()])
    R12_to_R12_min = FloatField("R2 self transition", validators=[DataRequired()])
    R12_to_R12_max = FloatField("R2 self transition", validators=[DataRequired()])
    submit = SubmitField("Submit Parameters")


class PNAS2012_StrategiesForm(FlaskForm):
    strategy_0 = BooleanField("Standard Precision Medicine - Strategy 0")
    strategy_22 = BooleanField("Dynamic Precision Medicine - Strategy 2.2")
    strategy_22_trial = BooleanField(
        "Dynamic Precision Medicine Trial for first 2 steps ONLY - Strategy 2.2-trial"
    )
    kmPlot = BooleanField("Produce KM Plot for all selected strategies.")
    benefit_DPM = BooleanField(
        "Benefit with DPM over Strategy 0 - Increase in survival of at least 60 Days improvement representing at least a 25% overall increase."
    )
    outcomePlot = BooleanField(
        "Pairwise comparision plot of overall Survival for all selected strategies"
    )
    classifierPerformance = BooleanField(
        "Test Performance of Heuristic Classifier - Sa(R1, D2) X R1 X T(R1, R12) +    Sa(R2, D2) X R2 X T(R2, R12),  >    Sa(R2, D1) X R2 X T(R2, R12) +  Sa(R1, D1) X R1 X T(R1, R12)"
    )
    trialGroups_firstSame = BooleanField(
        "Analyze population where Strategy 0 and Strategy 2.2-trial treatments match for step 1 and diverge in step 2"
    )
    trialGroups_secondSame = BooleanField(
        "Analyze population where Strategy 0 and Strategy 2.2-trial treatments differ for step 1 and match in step 2"
    )
    trialGroups_bothDiff = BooleanField(
        "Analyze population where Strategy 0 and Strategy 2.2-trial treatments differ for both step 1 and step 2"
    )
    trialGroups_bothSame = BooleanField(
        "Analyze population where Strategy 0 and Strategy 2.2-trial treatments are the same for both step 1 and step 2"
    )
    submit = SubmitField("Submit Analysis")


class Upload_ResultsForm(FlaskForm):
    documents = MultipleFileField(
        "Files",
        #validators=[
        #    FileRequired(),
        #    FileAllowed(["txt", "csv"], "Only txt and csv files accepted"),
        #],
    )
    submit = SubmitField("Submit")

from app import db
from app.utils import enums
import sqlalchemy as sa
from datetime import datetime


class Populations(db.Model):
    __tablename__ = "populations"

    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey("parameters.id"))
    strategy_id = db.Column(db.Integer, db.ForeignKey("strategies.id"))
    t = db.Column(db.Integer, index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(
        self, parameter_id, strategy_id, t=None, s=None, r1=None, r2=None, r12=None
    ):
        self.parameter_id = parameter_id
        self.strategy_id = strategy_id
        self.t = t
        self.s = s
        self.r1 = r1
        self.r2 = r2
        self.r12 = r12

    def __repr__(self):
        return "<id {}>".format(self.id)


class DrugDosages(db.Model):
    __tablename__ = "drug_dosages"

    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey("parameters.id"))
    strategy_id = db.Column(db.Integer, db.ForeignKey("strategies.id"))
    t = db.Column(db.Integer, index=True)
    drug_1 = db.Column(db.Numeric, index=True)
    drug_2 = db.Column(db.Numeric, index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(self, parameter_id, strategy_id, t, drug_1=0.00, drug_2=0.00):
        self.parameter_id = parameter_id
        self.strategy_id = strategy_id
        self.t = t
        self.drug_1 = drug_1
        self.drug_2 = drug_2

    def __repr__(self):
        return "<id {}>".format(self.id)


class StoppingTimes(db.Model):
    __tablename__ = "stopping_times"

    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey("parameters.id"))
    strategy_0 = db.Column(db.Numeric, index=True)
    strategy_1 = db.Column(db.Numeric, index=True)
    strategy_2_1 = db.Column(db.Numeric, index=True)
    strategy_2_2 = db.Column(db.Numeric, index=True)
    strategy_3 = db.Column(db.Numeric, index=True)
    strategy_1_dp = db.Column(db.Numeric, index=True)
    strategy_2_1_dp = db.Column(db.Numeric, index=True)
    strategy_2_2_dp = db.Column(db.Numeric, index=True)
    strategy_3_dp = db.Column(db.Numeric, index=True)
    global_dp = db.Column(db.Numeric, index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(
        self,
        parameter_id,
        strategy_0=None,
        strategy_2_2=None,
        strategy_3=None,
        strategy_1=None,
        strategy_2_1=None,
        strategy_1_dp=None,
        strategy_2_1_dp=None,
        strategy_2_2_dp=None,
        strategy_3_dp=None,
        global_dp=None,
    ):
        self.parameter_id = parameter_id
        self.strategy_0 = strategy_0
        self.strategy_1 = strategy_1
        self.strategy_2_1 = strategy_2_1
        self.strategy_2_2 = strategy_2_2
        self.strategy_3 = strategy_3
        self.strategy_1_dp = strategy_1_dp
        self.strategy_2_1_dp = strategy_2_1_dp
        self.strategy_2_2_dp = strategy_2_2_dp
        self.strategy_3_dp = strategy_3_dp
        self.global_dp = global_dp

    def __repr__(self):
        return "<id {}>".format(self.id)


class Parameters(db.Model):
    __tablename__ = "parameters"

    id = db.Column(db.Integer, primary_key=True)
    initial_subclone_population_id = db.Column(
        db.Integer, db.ForeignKey("initial_populations.id")
    )
    growth_rate = db.Column(db.Numeric, index=True)
    evolutionary_rates_id = db.Column(db.Integer, db.ForeignKey("transition_rates.id"))
    drug_sensitivities_id = db.Column(
        db.Integer, db.ForeignKey("drug_sensitivities.id")
    )
    file_id = db.Column(db.Integer, index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(
        self,
        growth_rate,
        initial_subclone_population_id,
        evolutionary_rates_id,
        drug_sensitivities_id,
        paramter_id=None,
        file_id=None,
    ):
        if paramter_id:
            self.id = paramter_id
        if file_id:
            self.file_id = file_id
        self.growth_rate = growth_rate
        self.initial_subclone_population_id = initial_subclone_population_id
        self.evolutionary_rates_id = evolutionary_rates_id
        self.drug_sensitivities_id = drug_sensitivities_id

    def __repr__(self):
        return "<id {}>".format(self.id)


class InitialPopulations(db.Model):
    __tablename__ = "initial_populations"

    id = db.Column(db.Integer, primary_key=True)
    s = db.Column(db.Numeric, index=True)
    r1 = db.Column(db.Numeric, index=True)
    r2 = db.Column(db.Numeric, index=True)
    r12 = db.Column(db.Numeric, index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(self, s, r1, r2, r12):
        self.s = s
        self.r1 = r1
        self.r2 = r2
        self.r12 = r12

    def __repr__(self):
        return "<id {}>".format(self.id)


class DrugSensitivities(db.Model):
    __tablename__ = "drug_sensitivities"

    id = db.Column(db.Integer, primary_key=True)
    s_drug1 = db.Column(db.Numeric, index=True)
    s_drug2 = db.Column(db.Numeric, index=True)
    r1_drug1 = db.Column(db.Numeric, index=True)
    r1_drug2 = db.Column(db.Numeric, index=True)
    r2_drug1 = db.Column(db.Numeric, index=True)
    r2_drug2 = db.Column(db.Numeric, index=True)
    r12_drug1 = db.Column(db.Numeric, index=True)
    r12_drug2 = db.Column(db.Numeric, index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(
        self,
        s_drug1,
        s_drug2,
        r1_drug1,
        r1_drug2,
        r2_drug1,
        r2_drug2,
        r12_drug1,
        r12_drug2,
    ):
        self.s_drug1 = s_drug1
        self.s_drug2 = s_drug2
        self.r1_drug1 = r1_drug1
        self.r1_drug2 = r1_drug2
        self.r2_drug1 = r2_drug1
        self.r2_drug2 = r2_drug2
        self.r12_drug1 = r12_drug1
        self.r12_drug2 = r12_drug2

    def __repr__(self):
        return "<id {}>".format(self.id)


class TransitionRates(db.Model):
    __tablename__ = "transition_rates"

    id = db.Column(db.Integer, primary_key=True)
    s_s = db.Column(db.Numeric, index=True)
    s_r1 = db.Column(db.Numeric, index=True)
    s_r2 = db.Column(db.Numeric, index=True)
    s_r12 = db.Column(db.Numeric, index=True)
    r1_s = db.Column(db.Numeric, index=True)
    r1_r1 = db.Column(db.Numeric, index=True)
    r1_r2 = db.Column(db.Numeric, index=True)
    r1_r12 = db.Column(db.Numeric, index=True)
    r2_s = db.Column(db.Numeric, index=True)
    r2_r1 = db.Column(db.Numeric, index=True)
    r2_r2 = db.Column(db.Numeric, index=True)
    r2_r12 = db.Column(db.Numeric, index=True)
    r12_s = db.Column(db.Numeric, index=True)
    r12_r1 = db.Column(db.Numeric, index=True)
    r12_r2 = db.Column(db.Numeric, index=True)
    r12_r12 = db.Column(db.Numeric, index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(
        self,
        s_s=None,
        s_r1=None,
        s_r2=None,
        s_r12=None,
        r1_s=None,
        r1_r1=None,
        r1_r2=None,
        r1_r12=None,
        r2_s=None,
        r2_r1=None,
        r2_r2=None,
        r2_r12=None,
        r12_s=None,
        r12_r1=None,
        r12_r2=None,
        r12_r12=None,
    ):
        self.s_s = s_s
        self.s_r1 = s_r1
        self.s_r2 = s_r2
        self.s_r12 = s_r12
        self.r1_s = r1_s
        self.r1_r1 = r1_r1
        self.r1_r2 = r1_r2
        self.r1_r12 = r1_r12
        self.r2_s = r2_s
        self.r2_r1 = r2_r1
        self.r2_r2 = r2_r2
        self.r2_r12 = r2_r12
        self.r12_s = r12_s
        self.r12_r1 = r12_r1
        self.r12_r2 = r12_r2
        self.r12_r12 = r12_r12

    def __repr__(self):
        return "<id {}>".format(self.id)


class Strategy(db.Model):
    __tablename__ = "strategies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), index=True)
    description = db.Column(db.String(512), index=True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return "<id {}>".format(self.id)


class DrugCategorizations(db.Model):
    __tablename__ = "drug_categorizations"

    id = db.Column(db.Integer, primary_key=True)
    standard_t0 = db.Column(db.Integer, db.ForeignKey("drug_dosages.id"))
    dpm_t0 = db.Column(db.Integer, db.ForeignKey("drug_dosages.id"))
    standard_t45 = db.Column(db.Integer, db.ForeignKey("drug_dosages.id"))
    dpm_t45 = db.Column(db.Integer, db.ForeignKey("drug_dosages.id"))
    categorization = db.Column(db.Enum(enums.TrialOutcome))
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    updated_on = db.Column(
        db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()
    )

    def __init__(self, standard_t0, dpm_t0, standard_t45, dpm_t45, category):
        self.standard_t0 = standard_t0
        self.dpm_t0 = dpm_t0
        self.standard_t45 = standard_t45
        self.dpm_t45 = dpm_t45
        self.categorization = category

    def __repr__(self):
        return "<id {}>".format(self.id)

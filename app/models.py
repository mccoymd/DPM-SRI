from app import db

class SimulationTypes(db.Model):
    __tablename__ = 'simulation_types'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Parameters(db.Model):
    __tablename__ = 'parameters'

    id = db.Column(db.Integer, primary_key=True)
    simulation_output_id = db.Column(db.Integer, db.ForeignKey('simulation_output.id'))
    initial_subclone_population_id = db.Column(db.Integer, db.ForeignKey('initial_populations.id'))
    growth_rate = db.Column(db.Numeric, index=True)
    evolutionary_rates_id = db.Column(db.Integer, db.ForeignKey('transition_rates.id'))
    drug_sensitivities_id = db.Column(db.Integer, db.ForeignKey('drug_sensitivities.id'))

    def __init__(self, growth_rate, initial_subclone_population_id, evolutionary_rates_id, drug_sensitivities_id):
        self.growth_rate = growth_rate
        self.initial_subclone_population_id = initial_subclone_population_id
        self.evolutionary_rates_id = evolutionary_rates_id
        self.drug_sensitivities_id = drug_sensitivities_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

class InitialPopulations(db.Model):
    __tablename__ = 'initial_populations'

    id = db.Column(db.Integer, primary_key=True)
    s = db.Column(db.Numeric, index=True)
    r1 = db.Column(db.Numeric, index=True)
    r2 = db.Column(db.Numeric, index=True)
    r12 = db.Column(db.Numeric, index=True)

    def __init__(self, s, r1, r2, r12):
        self.s = s
        self.r1 = r1
        self.r2 = r2
        self.r12 = r12

    def __repr__(self):
        return '<id {}>'.format(self.id)

class DrugSensitivities(db.Model):
    __tablename__ = 'drug_sensitivities'

    id = db.Column(db.Integer, primary_key=True)
    s_drug1 = db.Column(db.Numeric, index=True)
    s_drug2 = db.Column(db.Numeric, index=True)
    r1_drug1 = db.Column(db.Numeric, index=True)
    r1_drug2 = db.Column(db.Numeric, index=True)
    r2_drug1 = db.Column(db.Numeric, index=True)
    r2_drug2 = db.Column(db.Numeric, index=True)
    r12_drug1 = db.Column(db.Numeric, index=True)
    r12_drug2 = db.Column(db.Numeric, index=True)

    def __init__(self, s_drug1, s_drug2, r1_drug1, r1_drug2, r2_drug1, r2_drug2, r12_drug1, r12_drug2):
        self.s_drug1 = s_drug1
        self.s_drug2 = s_drug2
        self.r1_drug1 = r1_drug1
        self.r1_drug2 = r1_drug2
        self.r2_drug1 = r2_drug1
        self.r2_drug2 = r2_drug2
        self.r12_drug1 = r12_drug1
        self.r12_drug2 = r12_drug2

    def __repr__(self):
        return '<id {}>'.format(self.id)

class TransitionRates(db.Model):
    __tablename__ = 'transition_rates'

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

    def __init__(self, s_s, s_r1, s_r2, s_r12, r1_s, r1_r1, r1_r2, r1_r12, r2_s, r2_r1, r2_r2, r2_r12, r12_s, r12_r1, r12_r2, r12_r12):
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
        return '<id {}>'.format(self.id)

class SimulationOutput(db.Model):
    __tablename__ = 'simulation_output'

    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'))
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameters.id'))
    subclone_populations = db.Column(db.Numeric, index=True)
    drug_dosage = db.Column(db.Numeric, index=True)
    stopping_time = db.Column(db.String(256), index=True)

    def __init__(self, subclone_populations, drug_dosage, stopping_time, parameter_id, strategy_id):
        self.subclone_populations = subclone_populations
        self.drug_dosage = drug_dosage
        self.stopping_time = stopping_time
        self.parameter_id = parameter_id
        self.strategy_id = strategy_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Strategy(db.Model):
    __tablename__ = 'strategy'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128), index=True)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

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
    growth_rate = db.Column(db.Numeric, index=True)
    initial_subclone_populations = db.Column(db.Numeric, index=True)
    evolutionary_rates = db.Column(db.Numeric, index=True)
    drug_sensitivity = db.Column(db.Numeric, index=True)

    def __init__(self, growth_rate, initial_subclone_populations, evolutionary_rates, drug_sensitivity):
        self.growth_rate = growth_rate
        self.initial_subclone_populations = initial_subclone_populations
        self.evolutionary_rates = evolutionary_rates
        self.drug_sensitivity = drug_sensitivity

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

    def __init__(self, subclone_populations, drug_dosage, stopping_time):
        self.description = description
        self.drug_dosage = drug_dosage
        self.stopping_time = stopping_time

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

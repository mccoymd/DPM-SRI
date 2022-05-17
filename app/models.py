from app import db

class SimulationTypes(db.Model):
    __tablename__ = 'simulation_types'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Parameters(db.Model):
    __tablename__ = 'parameters'

    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class SimulationOutput(db.Model):
    __tablename__ = 'simulation_output'

    id = db.Column(db.Integer, primary_key=True)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'))
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameters.id'))

    def __repr__(self):
        return '<id {}>'.format(self.id)

class Strategy(db.Model):
    __tablename__ = 'strategy'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(128))

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)

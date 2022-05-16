from app import db

class SimulationTypes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), index=True)
    number_of_drugs = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<SimulationTypes {}>'.format(self.username)

class Parameters(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Parameters {}>'.format(self.username)

class SimulationOutput(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parameter_id = db.Column(db.Integer, db.ForeignKey('parameters.id'), nullable=False)
    strategy_id = db.Column(db.Integer, db.ForeignKey('strategy.id'), nullable=False)
    stopping_time = db.Column(db.Integer)
    drug_dosage = db.Column(db.String(120))
    subclone_population = db.Column(db.String(500))

    def __repr__(self):
        return '<SimulationOutput {}>'.format(self.username)

class Strategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(140), index=True)

    def __repr__(self):
        return '<Strategy {}>'.format(self.username)

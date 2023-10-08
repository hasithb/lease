from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# SQLAlchemy Model
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clauses = db.Column(db.PickleType)
    sentences = db.Column(db.PickleType)
    summarized_dict = db.Column(db.PickleType)

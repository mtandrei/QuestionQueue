from queue import db

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, index=True, nullable=False)
    username = db.Column(db.String(15), index=True, nullable=False)
    question = db.Column(db.String(500), index=True, nullable=False)
    votes = db.Column(db.Integer, index=True, nullable=False)

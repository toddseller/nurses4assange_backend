from db import db


class SignatoryModel(db.Model):
    __tablename__ = 'signatories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    specialty = db.Column(db.String(150), nullable=True) 
    email = db.Column(db.String(150), nullable=False)
    country = db.Column(db.String(80), nullable=False)

    def __init__(self, firstname, lastname, title, specialty, email, country):
        self.name = f'{firstname} {lastname}'
        self.title = title
        self.specialty = specialty
        self.email = email
        self.country = country

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'name': self.name, 'title': self.title, 'specialty': self.specialty, 'country': self.country}

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

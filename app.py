import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api

from db import db
from resources.signatory import Signatory, SignatoryList


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY')
api = Api(app)

api.add_resource(Signatory, '/signatory')
api.add_resource(SignatoryList, '/signatories')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)

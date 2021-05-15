from flask_restful import Resource, reqparse

from models.signatory import SignatoryModel as signatory_model


class Signatory(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname',
                        type=str,
                        required=True,
                        help='This field is required'
                        )
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help='This field is required'
                        )
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help='This field is required'
                        )
    parser.add_argument('specialty',
                        type=str,
                        required=False
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help='This field is required'
                        )
    parser.add_argument('country',
                        type=str,
                        required=True,
                        help='This field is required'
                        )

    def post(self):
        data = Signatory.parser.parse_args()

        if signatory_model.find_by_email(data['email']):
            return {'message': f'Signatory with the email {data["email"]} already exists'}, 403

        signatory = signatory_model(**data)

        try:
            signatory.save_to_db()
        except:
            return {'message': 'An error occurred while adding the signatory'}, 500

        return signatory.json(), 201


class SignatoryList(Resource):
    def get(self):
        return {'signatories': [signatory.json() for signatory in signatory_model.query.all()]}

from airplane_api import db
from airplane_api.airplane.models import Airplane
from sqlalchemy import exc
from flask import (
    Blueprint, current_app, jsonify, make_response, request
)

bp = Blueprint('airplane', __name__, url_prefix='/v1/')

@bp.route("/airplane", methods=["POST"])
def store_airplane():
    """Store a new airplane

    Endpoint:
    POST /v1/airplane/
    Request Body:
    {
        "manufacturer":"Airbus",
        "model":"A220",
        "year":"2015",
        "fuel_capacity":"200000"
        "next_destination":"Rome"
    }

    Store an airplane's fields, while respecting the corresponding specifications.
    """
    reqJson = request.get_json()
    manufacturer = reqJson.get('manufacturer')
    model = reqJson.get('model')
    year = reqJson.get('year')
    fuel_capacity = reqJson.get('fuel_capacity')
    next_destination = reqJson.get('next_destination')

    try:
        new_airplane = Airplane(manufacturer = manufacturer, model = model,
            year = year, fuel_capacity = fuel_capacity, next_destination = next_destination)
    except AssertionError as exception_message:
        return make_response(jsonify(msg='Error: {}'.format(exception_message)), 400)
   
    try:
        db.session.add(new_airplane)
        db.session.commit()     
    except exc.IntegrityError as ex:
        db.session.rollback()
        return make_response(jsonify(msg='Error: {}'.format(ex)), 400)

    return make_response(jsonify(new_airplane.as_dict(), 200))

@bp.route("/airplane/<int:id>", methods=["GET"])
def retrieve(id: int):
    """Fetch an airplane by its id

    Endpoint:
    GET /v1/airplane/5

    Get an airplane's information.
    """
    if not isinstance(id, int):
        return make_response(jsonify(msg='Id should be int'), 400)
    
    airplane = Airplane.query.get(id)
    if not airplane:
        return make_response(jsonify(msg='Model with id = {} doesn\'t exist'.format(id)), 404)

    return make_response(jsonify(airplane.as_dict()), 200)

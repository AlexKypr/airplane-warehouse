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
        current_app.logger.error('Airplane object (manufacturer: {}, model: {}, year: {}, fuel_capacity: {}, next_destination: {}),\
                                 could not be created'.format(manufacturer, model, year, fuel_capacity, next_destination))
        return make_response(jsonify(msg='Error: {}'.format(exception_message)), 400)
   
    try:
        db.session.add(new_airplane)
        db.session.commit()     
    except exc.IntegrityError as ex:
        current_app.logger.error('Airplane could not be created!')
        db.session.rollback()
        return make_response(jsonify(msg='Error: {}'.format(ex)), 400)

    current_app.logger.debug('Airplane with Id: {} has been created!'.format(new_airplane.id))
    return make_response(jsonify(new_airplane.as_dict(), 200))

def get_airplane(airplane):
    current_app.logger.debug('Airplane with Id: {} exists!'.format(airplane.id))
    return make_response(jsonify(airplane.as_dict()), 200)

def delete_airplane(airplane):
    try:
        db.session.delete(airplane)
        db.session.commit()
    except exc.IntegrityError as ex:
        current_app.logger.error('Airplane with Id: {} could not be deleted!'.format(airplane.id))
        db.session.rollback()
        return make_response(jsonify(msg='Error: {}'.format(ex)), 500)

    current_app.logger.debug('Airplane with Id: {} has been deleted!'.format(airplane.id))
    return make_response(jsonify(msg='Airplane with Id: {} has been deleted!'.format(airplane.id)), 200)

def update_airplane(airplane):
    reqJson = request.get_json()
    next_destination = reqJson.get('next_destination')
    current_app.logger.debug('Airplane\'s next destination should be {}!'.format(next_destination))
    try:
        airplane.next_destination = next_destination
        db.session.commit()
    except exc.IntegrityError as ex:
        current_app.logger.error('Airplane with Id: {} could not be updated!'.format(airplane.id))
        db.session.rollback()
        return make_response(jsonify(msg='Error: {}'.format(ex)), 400)
    except AssertionError as exception_message:
        current_app.logger.error('Airplane with Id: {} and next destination: {} could not be updated!'.format(airplane.id, next_destination))
        db.session.rollback()
        return make_response(jsonify(msg='Error: {}'.format(exception_message)), 400)
    
    current_app.logger.debug('Airplane with Id: {} has been updated!'.format(airplane.id))
    return make_response(jsonify(airplane.as_dict()), 200)

@bp.route("/airplane/<int:id>", methods=["GET", "DELETE", "PUT"])
def airplane_ops(id: int):
    """(i)Fetch an airplane by its id

    Endpoint:
    GET /v1/airplane/5

    Get an airplane's information.

    (ii)Delete an airplane by its id

    Endpoint:
    DELETE /v1/airplane/5

    Delete an airplane's entry.

    (iii)Update an airplane's next destination

    Endpoint:
    PUT /v1/airplane/5
    Request Body:
    {
        "next_destination":"Athens"
    }

    Update an airplane's entry.
    """
    if not isinstance(id, int):
        current_app.logger.error('Id is not integer!')
        return make_response(jsonify(msg='Id should be int'), 400)
    
    airplane = Airplane.query.get(id)
    if not airplane:
        current_app.logger.error('The Id doesn\'t correspond to an Airplane object')
        return make_response(jsonify(msg='Airplane with id = {} doesn\'t exist'.format(id)), 404)

    if request.method == 'GET':
        return get_airplane(airplane)
    elif request.method == 'DELETE':
        return delete_airplane(airplane)
    else:
        return update_airplane(airplane)
        
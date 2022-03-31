from airplane_api import db
from typing import Final
from datetime import date
from flask_sqlalchemy import event
from sqlalchemy.orm import validates

MANUFACTURERS: Final[list] = ['Airbus', 'Boeing']
MODELS: Final[dict] = ['747-8', '767', '777', 'A220', 'A330', 'A350']

class Manufacturer(db.Model):
    """Manufacturer's enties are stored here
    
    Manufacturer's schema.
    Initialize it with one of [Airbus, Boeing]
    """
    __tablename__ = 'manufacturer'
    name = db.Column(db.String(20), primary_key=True)

@event.listens_for(Manufacturer.__table__, 'after_create')
def populate_manufacturer(*args, **kwargs):
    db.session.add(Manufacturer(name='Airbus'))
    db.session.add(Manufacturer(name='Boeing'))
    db.session.commit()

class AirplaneModel(db.Model):
    """AirplaneModel's enties are stored here
    
    AirplaneModel's schema.
    Initialize it with one of [747-8, 767, 777, A220, A330, A350]
    """
    __tablename__ = 'airplane_model'
    name = db.Column(db.String(20), primary_key=True)

@event.listens_for(AirplaneModel.__table__, 'after_create')
def populate_airplane_model(*args, **kwargs):
    db.session.add(AirplaneModel(name='747-8'))
    db.session.add(AirplaneModel(name='767'))
    db.session.add(AirplaneModel(name='777'))
    db.session.add(AirplaneModel(name='A220'))
    db.session.add(AirplaneModel(name='A330'))
    db.session.add(AirplaneModel(name='A350'))
    db.session.commit()

class ManufacturerModel(db.Model):
    """ManufacturerModel's enties are stored here
    
    ManufacturerModel's schema. Specifying manufacturer and model names 
    as composite primary key, while also defining both of them as foreign 
    keys to the respective tables. The addition of ManufacturerModel table allow 
    us to model the dependency between the models and the manufacturers. 
    For example, a320 is only Airbus model, so we want to restrict an entry
    that will have Boeing as manufacturer and a320 as model.
    """
    __tablename__ = 'manufacturer_model'
    make = db.Column(db.String(20), db.ForeignKey('manufacturer.name'), primary_key=True)
    model = db.Column(db.String(20), db.ForeignKey('airplane_model.name'), primary_key=True)

@event.listens_for(ManufacturerModel.__table__, 'after_create')
def populate_manufacturer_model(*args, **kwargs):
    db.session.add(ManufacturerModel(make='Boeing', model='747-8'))
    db.session.add(ManufacturerModel(make='Boeing', model='767'))
    db.session.add(ManufacturerModel(make='Boeing', model='777'))
    db.session.add(ManufacturerModel(make='Airbus', model='A220'))
    db.session.add(ManufacturerModel(make='Airbus', model='A330'))
    db.session.add(ManufacturerModel(make='Airbus', model='A350'))
    db.session.commit()

class Airplane(db.Model):
    """Airplane's enties are stored here
    
    Airplane's schema. We use manufacturer and model as foreign key to ManufacturerModel
    composite primary key, in order to restrict the manufacturer's and model's values
    to the ones defined in the manufacturer and model database model, respectively.
    """
    __tablename__ = 'airplane'
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(20), nullable=False)
    model = db.Column(db.String(20), nullable=False)
    year = db.Column(db.SmallInteger, nullable=True)
    fuel_capacity = db.Column(db.Integer, nullable=True)
    next_destination = db.Column(db.String(20), nullable=True)
    __table_args__ = (db.ForeignKeyConstraint([manufacturer, model],
                                           [ManufacturerModel.make, ManufacturerModel.model]), {}
                      )

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @validates('manufacturer')
    def validate_manufacturer(self, key, manufacturer):
        if not manufacturer:
            raise AssertionError('Manufacturer is not provided')
        elif manufacturer not in MANUFACTURERS:
            raise AssertionError('Manufacturer must be either "Airbus" or "Boeing"')
        return manufacturer

    @validates('model')
    def validate_model(self, key, model):
        if not model:
            raise AssertionError('Model is not provided')
        elif model not in MODELS:
            raise AssertionError('Model must be either 747-8, 767, 777, A220, A330 or A350')
        return model

    @validates('year')
    def validate_year(self, key, year):
        todays_date = date.today()
        this_year = todays_date.year
        if year:
            if not isinstance(year, str):
                raise AssertionError('Year\'s type should be string')
            if not year.isdigit():
                raise AssertionError('Year must be digit')
            if not (int(year) >= 1900 and int(year)<= this_year):
                raise AssertionError('Year must be between 1900 and the current year')
        return year
    
    @validates('fuel_capacity')
    def validate_fuel_capacity(self, key, fuel_capacity):
        if fuel_capacity:
            if not isinstance(fuel_capacity, str):
                raise AssertionError('Fuel capacity\'s type should be string')
            if not fuel_capacity.isdigit():
                raise AssertionError('Fuel capacity must be digit')
            if not (int(fuel_capacity) >= 0):
                raise AssertionError('Fuel capacity should be positive')
        return fuel_capacity

    @validates('next_destination')
    def validate_next_destination(self, key, next_destination):
        if next_destination:
            if not isinstance(next_destination, str):
                raise AssertionError('Next destination\'s type should be string')
            if len(next_destination) > 85:
                raise AssertionError('Next destination should contain less than 85 characters')
        return next_destination
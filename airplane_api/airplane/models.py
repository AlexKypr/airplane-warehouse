from airplane_api import db
from flask_sqlalchemy import event

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
    fuel_demands = db.Column(db.Integer, nullable=True)
    next_destination = db.Column(db.String(20), nullable=False)
    __table_args__ = (db.ForeignKeyConstraint([manufacturer, model],
                                           [ManufacturerModel.make, ManufacturerModel.model]), {}
                      )

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}


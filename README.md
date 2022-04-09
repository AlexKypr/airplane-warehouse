# airplane-warehouse

[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/AlexKypr/airplane-warehouse/blob/main/LICENSE)

CRUD REST API application with [Flask](http://flask.pocoo.org) and [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org), using SQlite db to store our data. 

The database contains four tables Airplane, Manufacturer, AirplaneModel and ManufacturerModel. ManufacturerModel has Many-to-One relationship with both Manufacturer and AirplaneModel to constrain the values of Manufacturer and Model columns with the respective ones specified
in the Manufacturer and AirplaneModel tables. Moreover, Airplane has Many-to-One relationship with Manufacturer Model using composite foreign key to ensure that combinations like Airbus 777
would not be allowed.

## Getting started
* Fetch the source code of the project.
```
$ git clone git@github.com:AlexKypr/airplane-warehouse.git
$ cd airplane-warehouse
```

* Create a virtual environment for this project
```
$ python3 -m venv your-virtual-env
```

* Activate the virtual environment
```
$ source your-virtual-env/bin/activate
```

* Install the dependencies
```
$ pip install -r requirements.txt
```

## Run the App
```
$ export FLASK_APP=airplane_api
$ flask init-db
```

* Run the app
```
$ flask run
```

## API Documentation

### 1. Create airplane

#### Request
```
POST /v1/airplane
```
#### Request body
```
{
    "manufacturer":"Airbus",
    "model":"A220",
    "year":"2015",
    "fuel_capacity":"200000",
    "next_destination":"Rome"
}
```
#### Response
```
[
    {
        "fuel_capacity": 200000,
        "id": 1,
        "manufacturer": "Airbus",
        "model": "A220",
        "next_destination": "Rome",
        "year": 2015
    },
    200
]
```

### 2. Get airplane information

#### Request
```
GET /v1/airplane/:id
```

#### Response
```
{
    "fuel_capacity": 200000,
    "id": 1,
    "manufacturer": "Airbus",
    "model": "A220",
    "next_destination": "Rome",
    "year": 2015
}
```

### 3. Update airplane's next destination

#### Request
```
PUT /v1/airplane/:id
```
#### Request body
```
{
    "next_destination":"Athens"
}
```
#### Response
```
{
    "fuel_capacity": 200000,
    "id": 1,
    "manufacturer": "Airbus",
    "model": "A220",
    "next_destination": "Athens",
    "year": 2015
}
```
### 4. Delete airplane

#### Request
```
DELETE /v1/airplane/:id
```
#### Response
```
{
    "msg": "Airplane with Id: 1 has been deleted!"
}
```

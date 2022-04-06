# airplane-warehouse

RESTful CRUD API application using [Flask](http://flask.pocoo.org), and [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org), using SQlite db to store our data. 

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



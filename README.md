# IS211_Assignment12
Web Development with Flask part two

To run the application follow the steps below:

1. Traverse to the project base path ( IS_211_Final)
2. One the CLI run:
    Windows 
    
    C:\IS211_Assignment12> set FLASK_APP=bookcatalog.py
    C:\IS211_Assignment12> flask run
    
    Unix
    
    ~/IS211_Final
    $ export FLASK_APP=bookcatalog.py
    $ flask run
            
#### Useful tips
Set your FLASK_DEBUG=1 so the flask app can run in debug mode and be able to hot reload instead of having to stop and start the flask app
            
### Database

FLASK_APP is a dependency and must be set to bookcatalog.py.

Once flask variable has been set run the following command to
initialize the database.


> flask db init

## Database migrations

> flask db migrate -m "users table"
> flask db upgrade
-m option is optional, it adds a short descriptive text to
the migration

## Enable Virtual env
virtualenv venv
venv\Scripts\activate
# Card Manager

This web application is designed to manage your credit card database.

Functionality of the program:
- a list of cards with fields: series, number, date of issue, date of expiration, status, svv, amount, card status (not activated/activated/expired)
- filtering by the same fields
- view the profile of the card with the history of purchases on it
- card activation/deactivation
- card deletion
- card generator with the following fields: series, number of generated cards, expiration date" with the values ​​"1 year", "6 months", "1 month".
- after the expiration of the card's activity period, the status "expired" is assigned to the card

You can check the project on Hiroku:

https://card-manager-test-task.herokuapp.com/

# Technology

- Python 3.7

- Django 3.2.13

- Celery + Redis

- Postgresql

- Heroku


# Installation 

## Local

1. Clone the repository

2. Create a virtual environment in the root folder `python -m venv venv`

3. Activate the virtual environment `venv\Scripts\activate.bat`

4. Install the dependencies `pip install -r requirements.txt`

5. Copy and fill in with your data `cp .env.example .env`

6. To run locally, replace the variable DATABASES to

`DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    }`

7. Run database migrations `python manage.py migrate`
 
8. Run fixteres  `python manage.py loaddata card.json transaction.json CardGeneration.json`

9. In terminal-1 run celery-beat
`celery -A core beat`

10. ВIn terminal-2 run celery worker
`celery -A core worker -l INFO`

11. To start the server, enter `python manage.py runserver`


## Heroku
1. Set up environment variables Heroku in Setting/Config_Vars

2. Log in to your Heroku

3. Use Git to clone app's source code to your local machine

4. Deploy app to Heroku using Git - `git push heroku main`

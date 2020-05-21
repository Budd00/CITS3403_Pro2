# CITS3403_Pro2

Multi-user quiz application allow administrators to set question sets, users to submit answers to the questions, and manual or automatic assessment of those answers.

## Dependency

Dependencies needed for running the system:

Flask

flask-login

sqlalchemy

flask-sqlalchemy

sqlalchemy-migrate

flask-wtf

Selenium

## Running System

flask run

The system will be running on http://localhost:5000

## Running Unittest 

Before running Unittest, you have to download chromedrive and change setting in app/__init__.py.

Download chromedriver from https://chromedriver.chromium.org/

Changing app.config.from_object(Config) to app.config.from_object(ConfigTest)

python -m test.unit

python -m test.test





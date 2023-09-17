# EscargotIT Snail Farm Management Web App

## About
EscargotIT is a Django project for a web application for snail farm efficiency management and progress tracking.
The application prides itself with being one of the first on the market as there is no snail farm software out there.
It uses machine learning (NeuralProphet) to provide the users with forecasts and insights for future permormance of Snail Beds.

## Technologies used
Mainly it uses Django, and the main feature which is the machine learning forecasts is provided by NeuralProphet.

## Functionality
A user (farm owner) can register their farm. They can create accounts for their employees and give them permissions.
The admin, and employee with permissions, can create Snail Beds on their dashboard page. Then for each Snail Bed, they can
log data like:
- new snails hatched
- snails expired
- feed given
- snails reached maturity age (marketable age) and the period they did so for

The Admin can see data correlation and graphs for each Snail Bed, possibly draw conclusions if correlations between 2 data types is high.
The Admin can also generate a Performance for each Snail Bed. This is done by the program, but the user needs to initiate the process.
The Performance of a snail bed is calculated by how many snails have hatched, how many have perished, how many have reached maturity and the time periods for all these.
The Admin can also generate a future Forecast graph and forecasted data points for the upcoming 8 weeks for all data parameters. Here NeuralProphet takes existing data that the users have entered, and runs a machine learning algorithm to try and predict how the Snail Bed will be doing in the future.

## How to setup and run locally

#### Youtube tutorial video
https://www.youtube.com/watch?v=v3qARIiHepc


You need to have pip installed on your PC.

Donwload the repository as a ZIP and unzip on your PC.

Open VS Code as Administrator to have full access to install packages for this project.

In VS Code, Open Folder and choose the Escargotit project folder.

Open a New Terminal, and use Command Prompt instead of Powershell.

### Virtual Env
Install virtual environment wrapper so that you can safely install and run packages.
- pip3 install virtualenvwrapper
- python -m venv env
- env\Scripts\activate 

Now you have the virtual environment active. Time to install dependencies.

### Packages 
This project uses NeuralProphet which is a library with many other dependencies of its own, so even if the requirements.txt file contains all packages, I suggets you do not run "pip install -r requirements.txt" because the order and the versions are not what NeuralProphet requires. Therefore, run the following commands:

- pip install django

- pip install djangorestframework
https://pypi.org/project/djangorestframework/

- pip install django-bootstrap-v5
https://pypi.org/project/django-bootstrap-v5/

This project uses numpy and pandas, but NeuralProphet will install the versions it wants, so don't install them separately.
Here is the documentation for them anyway:
https://numpy.org/install/
https://pypi.org/project/pandas/

- pip install neuralprophet
https://pypi.org/project/neuralprophet/

- pip install django-picklefield
https://pypi.org/project/django-picklefield/

- pip install scipy
https://scipy.org/install/

### Run
Now left to run locally 
- python manage.py runserver 127.0.0.1:8080 
Now if there are no errors open https://127.0.0.1:8080  in your browser and you should see EscargotIT running. 
Yay!

### Testing
The application has 37 unit tests prepared using Faker and Factory Boy packages, to create a dummy database and test each field for each model class.
To run the test, in terminal, navigate inside the outer escargotit repository and run:
- python manage.py test
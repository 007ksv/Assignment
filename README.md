# Django Employee Leave Management 
This is a fully functional Employee Leave Management web applications

Here is a quick overview, what this web app can do

## What employee can do
* Employee can login using their credentials. 
* Can create an application for Leave where they have to fill the basic field of application (Description, start date and end date).
* Can keep track of all of his/her applications on **Dashboard.** 
* Employee cann't take leave if they don't have any leave pending

## What Manager can do
* Can Approve or Decline the employee Leave application.
* Can keep track of all of his/her activity.

## What admin can do
* Admin have complete transaction flow with each steps.
* As you all know admin can do whatever he wants to.

# Instructions for running project
* Clone the repo using `git clone https://github.com/007ksv/Assignment.git`
* Install all the requirements using `pip install -r requirements.txt`
* Make all the migrations using `python manage.py makemigrations` and then `python manage.py migrate`.
* Then start the server `python manage.py runserver`

# Taskify-Backend
The backend has 3 routes

1) Post route

This route is reponsible for creating tasks, deleting tasks, updating tasks and filtering tasks.

2) Users route

This route is about creating users and searching user by id.

3) Auth route

This route is about login system.

# How To Run Locally

First clone this repo by using following command

git clone https://github.com/Izaac04/Taskify-Backend.git

then

cd Taskify-Backend

Then install fastapp using all flag like

pip install fastapi[all]

Then go into the app folder in your local computer run following the command

uvicorn main:app --reload

Then you can use following link to use the API

http://127.0.0.1:8000/docs 

# SoftDesk #

1.  [Description](#description)
2.  [Use](#use)
    1.  [setup](#setup)
    2.  [features](#features)

## 1. Description <a name="description"></a> ##

This API has been realized as part of a project of the course
'Application developer - Python' of OpenClassrooms.


The aim is to build an issue tracking application.
The API will essentially allow users to create various projects, add users to specific projects, create issues within projects and assign labels to these issues based on their priorities, tags, ...

This API is built with Django REST framework. The database is a SQLite file : db.sqlite3

## 2. Use <a name="use"></a> ##

#### SETUP : <a name="setup"></a> ####

First, start by cloning the repository:

```
git clone git@github.com:mariefj/P10_OC_SoftDesk.git
```

- Access the project folder
```
cd P10_OC_SoftDesk
```

- Create a virtual environment
```
python -m venv env
```

- Enable the virtual environment
```
source env/bin/activate
```

- Install the python dependencies on the virtual environment
```
pip install -r requirements.txt
```

- Start
```
python manage.py runserver
```

- Test the API with your favourite tool at this address (example: Postman)
```
http:/127.0.0.1:8000
```

#### FEATURES : <a name="features"></a> ####

This Django project contains 2 apps : authentication - tracking

##### API Endpoints #####

A complete documentation is available [here](https://documenter.getpostman.com/view/15450358/2s8YeuLquP) 

HTTP Methods | Endpoints | Action

POST | /signup/ | To sign up a new user account  
POST | /login/ | To login an existing user account  

GET | /projects/ | To retrieve all projects where the currently user is a contributor  
POST | /projects/ | To add a new project  
GET | /projects/{id}/ | To get an existing project  
PUT | /projects/{id}/ | To update an existing project  
DELETE | /projects/{id}/ | To delete an existing project and its issues and contributors  

GET | /projects/{id}/users/ | To retrieve all contributors of a project  
POST | /projects/{id}/users/ | To add a new contributor to a project  
GET | /projects/{id}/users/{id}/ | To get a contributor  
PUT | /projects/{id}/users/{id}/ | To update a contributor  
DELETE | /projects/{id}/users/{id}/ | To delete an existing contributor  

GET | /projects/{id}/issues/ | To retrieve all issues from a project  
POST | /projects/{id}/issues/ | To add a new issue  
GET | /projects/{id}/issues/{id}/ | To get an existing issue  
PUT | /projects/{id}/issues/{id}/ | To update an existing issue  
DELETE | /projects/{id}/issues/{id}/ | To delete an existing issue and its comments  

GET | /projects/{id}/issues/comments/ | To retrieve all comments from an issue  
POST | /projects/{id}/issues/comments/ | To add a new comment  
GET | /projects/{id}/issues/{id}comments/{id}/ | To get an existing comment  
PUT | /projects/{id}/issues/{id}comments/{id}/ | To update an existing comment  
DELETE | /projects/{id}/issues/{id}comments/{id}/ | To delete an existing comment  

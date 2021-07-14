# Full Stack API Final Project
Site Live at : https://casting-app2021.herokuapp.com

## Full Stack Capstone Project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

Models:
    Movies with attributes title and release date
    Actors with attributes name, age and gender

Endpoints:
    GET /actors and /movies
    DELETE /actors/ and /movies/
    POST /actors and /movies and
    PATCH /actors/ and /movies/

Roles:
    Casting Assistant
        Can view actors and movies
    Casting Director
        All permissions a Casting Assistant has and…
        Add or delete an actor from the database
        Modify actors or movies
    Executive Producer
    All permissions a Casting Director has and…
    Add or delete a movie from the database

Tests:
O   ne test for success behavior of each endpoint
    One test for error behavior of each endpoint
    At least two tests of RBAC for each role

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Running the server

From within the `starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
source setup.sh
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app.py` file to find the application.

## REST API Reference

### Getting Started
- Base URL: currently the backend flask server runs locally on http://127.0.0.1:5000/
- Authentication: Implemented using Auth0.
  This API uses Auth0 for authentication, you will need to setup Auth0 application and API. You will need to update Auth0 variables found in config.py.

The JWT tokens for the 3 roles are as  below and valid for next 24 hrs:

auth0_tokens = {
    "casting_assistant": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlotSmJLVzlGTTJJVHRpb1c2X0hvcSJ9.eyJpc3MiOiJodHRwczovL2pzYXNhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlYjM1NmMxNjFhODIwMDY4ZWE1NjRmIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNjI4MjEyMiwiZXhwIjoxNjI2MzY4NTIyLCJhenAiOiJYQ0gxVGJBbHZ4Y05BQ3IzSmtheTh5ZnRTaVF4cVlmciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.gpSDI_IVvFvzRmBFGB9aHIVcjeXRGzVbfNcZf2jB3HvxIekyjt-PMbG5TX25fcZwO9n13kiUL1OL8ITvI_iXqXBWvNG9bDYck3JPVKdfapNzXrmXLhKrhSyMbs_OQ6deC3ZrzLLtCNczgo58t47PCJltt8P6JvQKszlm6Ppuh7mUePFXZNHfyV-otEcQ66aLg-pLd_NcLdPSmY7qzON9wbodwo7k0eZrMkyBacnozWuuBu0wCyxvg9zoGKvOnmv2DhVUXXMrSK8qqa_I6k49gyfbBy2VBBG6dyGpWEr_gxPv46cRsOxFxmodcNShIsnoIzOLO4AoTRgdYVXUDRvK1g",

    "casting_director": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlotSmJLVzlGTTJJVHRpb1c2X0hvcSJ9.eyJpc3MiOiJodHRwczovL2pzYXNhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlYjM1NGJmYzVlOWIwMDZiYWM1MTljIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNjI4MjAzOCwiZXhwIjoxNjI2MzY4NDM4LCJhenAiOiJYQ0gxVGJBbHZ4Y05BQ3IzSmtheTh5ZnRTaVF4cVlmciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.UhpHbuEthUqsExxhFydCm6epm0ol-Lb-_CQTrr0wWPebao4tdphoGIBjuN0gBKhnDoTfLYXY02TEOU0aobjxfLgYtJrY8pMpSHpSmLmW6wSpp-9IhWytHZcG0vlRxyA7a94EZMqhGQcgSgymm1pB5d5nT0cZr0qF4cAz5-N6Ppr4ZJjH3E67tF5uEHbm6v4XVjlfd6DFbN8_yTzhJddXG-wuEN9oszwlBp5kw1ABa44SED7bHoGYhaHLbnKsBuvkSOx-5qXnMUflGUnYQnH1DmZKnYs_Uxbs8nBCzselRDMQQ7jRrSyDVTpQzbvAvWaGfoB7G9mLVtSjZbDv3P-2yA",

    "executive_producer": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlotSmJLVzlGTTJJVHRpb1c2X0hvcSJ9.eyJpc3MiOiJodHRwczovL2pzYXNhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlYjM1YWFmYzVlOWIwMDZiYWM1MTlmIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNjI4MjE4NSwiZXhwIjoxNjI2MzY4NTg1LCJhenAiOiJYQ0gxVGJBbHZ4Y05BQ3IzSmtheTh5ZnRTaVF4cVlmciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.tzKDM8_eAEk9KBDgw8LiHlH8dlM_NEwf6GIewKOVabAg9_qPtV5zDHLa-cerzHOXGSYM1nTR2F3OrQ0otwXBOpQLzRUQNTIXCDaNgz-rZE9a9nCi_u2wI4a9UVoUJhA54VKo4qYM5GLAzyVcx-hfJUEs93tiVfS-FFbR6fO1RT4S5LVbw9SHRnbpCb8a7I9goC7QenBo21u0jGIdxs7-Gf4JVtfYiLrpxQTTMLAo-Ehh_nIFAT0TNmULQJSrDxdGD4ttCbCLvxHd7tQhIC_evL4cDDRk7-eqszjmBvPkZvZq-mQpdMXnjp84PshfuZIBHrO_Uadm3bBwBK29ksb2HA"
}

They can also be generated using the following link
https://jsasan.us.auth0.com/authorize?audience=https://casting-agency&response_type=token&client_id=XCH1TbAlvxcNACr3Jkay8yftSiQxqYfr&redirect_uri=https://casting-app2021.herokuapp.com/tabs/user-page

And using the following username/passwd combos for the roles:
Producer:           producer@gmail.com/Casting2021
Casting-Director  : casting-director@gmail.com/Casting2021
Casting-Assistant : casting-assistant@gmail.com/Casting2021

### Error Handling

Flask's @app.errorhandler decorators are implemented for:

- 404: Resource not found
- 422: Unprocessable entity

Errors are returned as JSON objects in the following format:
```bash
{
    "success": False, 
    "error": 404,
    "message": "Resource not found"
}
```
### EndPoints
### Actors and Movies
This API supports two types of resources /actors and /movies. Each resource supports four HTTP methods; GET, POST, PATCH, DELETE

Notes

You need to update the ACCESS_TOKEN in the below requests with JWT valid token.
The below requests assume you are running the app locally, so you need to update the requests with the base URL or your URL after deployment.

#### GET /actors
- Fetches an array of actors in which the keys are the ids, and the value is the corresponding string of the actor
- Request Arguments: None
- @Return Value: The JSON response includes success status, and an array of actors { id: type } stored in the database.
- Example: ``` curl http://127.0.0.1:5000/actors```
```bash
{
    "actors": [
        {
            "age": 25,
            "gender": "Male",
            "id": 1,
            "name": "Jatin"
        },
        {
            "age": 26,
            "gender": "Male",
            "id": 2,
            "name": "Kabir"
        }
    ],
    "success": true
}
```

#### GET /movies
- Fetches an array of movies in which the keys are the ids, and the value is the corresponding string of the movie
- Request Arguments: None
- @Return Value: The JSON response includes success status, and an array of movies { id: type } stored in the database.
- Example: ``` curl http://127.0.0.1:5000/movies```
```bash
{
    "movies": [
        {
            "actors": [
                "Jatin",
                "Kabir"
            ],
            "date": "Wed, 05 Jun 1996 00:00:00 GMT",
            "id": 1,
            "title": "Dilwale Dulhania le jaayenge"
        },
        {
            "actors": [
                "Nitika"
            ],
            "date": "Tue, 13 Jul 2021 00:00:00 GMT",
            "id": 2,
            "title": "NewHorizon"
        }
    ],
    "success": true
}
```

#### DELETE  /actors/{actor_id}
- Deletes the actor of the given ID if it exists in the database.
- Request Arguments: <actor_id> of the question to be deleted
- @Return Value: The JSON response includes a success value, and the actor id of the deleted actor.
- Example: ``` curl -X DELETE -H 'Authorization: Bearer {{Token_id}}' http://127.0.0.1:5000/actors/2```

```bash
{
    "delete": 2,
    "success": true
}
```

#### DELETE  /movies/{movie_id}
- Deletes the movie of the given ID if it exists in the database.
- Request Arguments: <movie_id> of the question to be deleted
- @Return Value: The JSON response includes a success value, and the actor id of the deleted movie.
- Example: ``` curl -X DELETE -H 'Authorization: Bearer {{Token_id}}' http://127.0.0.1:5000/movies/2```

```bash
{
    "delete": 2,
    "success": true
}
```

#### POST /actors
- Allows user to post a new actor resource using the submitted Name, age, gender.
- Request Arguments: POST body expression containing name, age, gender.
- @Return Value: The JSON response includes a success value.
- Example 1: ``` curl http://127.0.0.1:5000/actors -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer {{Token_id}}' -d '{"name": "Test", "age": "21", "gender": "Male"}' ```

```bash
{
    "actors": {
        "age": 25,
        "gender": "Male",
        "id": 1,
        "name": "Jatin Sasan"
    },
    "success": true
}
```
- Example 2: ``` curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "name"}' ```

```bash

#### POST /movies
- Allows user to post a new movie resource using the submitted Title and release date.
- Request Arguments: POST body expression containing title and date.
- @Return Value: The JSON response includes a success value and the movie_id of the newly added movie.
- Example 1: ``` curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -H 'Authorization: Bearer {{Token_id}}' -d '{"title": "Test", "date": "07/13/2021"}' ```

```bash
{
    "movie": 3,
    "success": true
}
```

#### PATCH /actors/{actor_id}
- Allows user to update an existing actor resource using the new Name, age or gender.
- Request Arguments: POST body expression containing Name, age or gender.
- @Return Value: The JSON response includes a success value and the actor_id of the newly modified actor.
- Example 1: ``` curl http://127.0.0.1:5000/actors -X PATCH -H "Content-Type: application/json" -H 'Authorization: Bearer {{Token_id}}' -d '{"name": "Test", "age": "33"}' ```

```bash
{
    "actors": {
        "age": 33,
        "gender": "Male",
        "id": 1,
        "name": "Test"
    },
    "success": true
}
```

#### PATCH /movies/{movie_id}
- Allows user to edit an existing resource using the submitted Title and release date.
- Request Arguments: POST body expression containing title and date.
- @Return Value: The JSON response includes a success value and the movie_id of the newly added movie.
- Example 1: ``` curl http://127.0.0.1:5000/movies -X PATCH -H "Content-Type: application/json" -H 'Authorization: Bearer {{Token_id}}' -d '{"title": "Test", "date": "07/13/2021"}' ```

```bash
{
    "movies": {
        "actors": [
            "Jatin Sasan"
        ],
        "date": "Tue, 23 Mar 2010 00:00:00 GMT",
        "id": 1,
        "title": "SanJose_Memoirs"
    },
    "success": true
}
```

## Testing
To run the tests, run
```
python3 --verbose test_app.py
```

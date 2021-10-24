# FamilyTree

FamilyTree is an API for getting family details like list of siblings, children, grandparents etc.

## Endpoints

```json
- /api
    - signup/ (Accessible to everyone)
    - person/ (Authentication is required)
    - person/<int:pk>/ (Authentication)
    - relation/ (Authentication is required)
    - relation/<int:pk>/ (Authentication is required)
    - relation/<int:person>/<str:relation>/ (Authentication is required)

```

## api/signup/

This endpoint will help in adding new user to the database. The user can use basic or token authentication to login and start adding new person to make full families

## api/person/

- (POST) add new person to the database which can later be connected to another person with the help of `api/relation` endpoint.
- (GET) get the person details using id/pk passed in the url.
- (PUT) update the person details
- (DELETE) delete the person

## api/relation/

- (POST) create a new relative with the help of passed person id and the relation.
- (GET) get the list of all the relatives using person id and relation string (`like /api/relation/1/child/`)
- (PATCH) update the relation between two person
- (DELETE) delete the relation between two persons

---

## Assumptions

- every person have reverse `relation` also like `parent` <--> `child`.
- One user can add multiple families by adding multiple Person and forming relations between them.

---

## Installation

- use `pipenv` to create a new environment and install all the required package present in requirements.txt file
- refer `FamilyTree.postman_collection.json` to import collection in postman to test the api.
- run using simple locally running command `python manage.py runserver 8000`.
- make sure you migrate your db file before running the application.

# tesena-fastapi-homework

Sample project of a simple RESTful API built on the **FastAPI** framework that supports basic CRUD operations, complete with unit and integration tests

## Requestments

* Python 3.10+
* pip (Python package manager)

## Running locally

### **clone and enter the directory "
        ```bash
        git clone <repo url>
        cd tesena-fastapi-homework
        ```
### virtual env
    ```
    python -m venv venv
    # Linux/macOS:
    source venv/bin/activate
    # Windows:
    .\venv\Scripts\activate
    ```
### Dependencies
        pip install -r requirements.txt

### Running dev server
    ```
    uvicorn app.main:app --reload
    ```
The instance should run at localhost and 8000 port. Swagger is available as well at /docs or /redocs for Redoc documentation.

## End Points
- POST /items/ (new item created, returns HTTP 201)
- GET /items/ (get all items, returns 200 OK)
- GET items/{id} (get items detail, return 200 OK)
- PUT /items/{id} (update the item, returns 200 OK)
- DELETE /items/{id} (deleting the item, returns 204 No Content)

## Running tests
```
#all tests
pytest -v 
#unit tests
pytest tests/test_unit.py -v
#int tests
pytest tests/test_integration.py -v
```

## Run E2E
### Bash
```
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C047CFA7FA
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update && sudo apt-get install k6
```
### Windows
```
winget install grafana.k6
```
### Run dev server
```
source venv/bin/activate
uvicorn app.main:app --reload
k6 run k6/e2e_test.js # in parallel terminal
```

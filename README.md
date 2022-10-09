# virtual environment
Install virtualenv
```
pip install virtualenv
```
Create virtual environment
```
virtualenv venv
```
Activate virtual environment
```
activate: source .env/bin/activate
```
Deactivate virtual environment
```
deactivate: deactivate
```

# Postgres
Install postgres database and replace connnection string in .env file

# Flask Restx WEB API
[Flask Restx](https://flask-restx.readthedocs.io/en/latest/index.html)
## Features
- Flask-Bcrypt: A Flask extension that provides bcrypt hashing utilities for your application.
- Flask-Migrate: An extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are made available through the Flask command-line interface or through the Flask-Script extension.
- Flask-SQLAlchemy: An extension for Flask that adds support for SQLAlchemy to your application.
- PyJWT: A Python library which allows you to encode and decode JSON Web Tokens (JWT). JWT is an open, industry-standard (RFC 7519) for representing claims securely between two parties.
- Namespaces (Blueprints)
- [Flask-resttx](https://flask-restx.readthedocs.io/en/latest/index.html)
- UnitTest

## Project Setup and Organization
```
.
├── app
│   ├── __init__.py
│   ├── main
│   │   ├── controller
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── model
│   │   │   └── __init__.py
│   │   └── service
│   │       └── __init__.py
│   └── test
│       └── __init__.py
└── requirements.txt
```
## Install required packages
```
pip install -r requirements.txt
```
## Migration db
```
$ flask db init
$ flask db migrate -m "Initial migration."
$ flask db upgrade
```
## Run app
```
flask run
```

## Run debug
.vscode > launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "manage.py",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "1",
                "SECRET_KEY": "secret_key"
            },
            "args": [
                "run",
                "--no-debugger",
            ],
            "jinja": true
        },
    ]
}
```
# Development
## Create an User and upgrade to admin
1. Create an user 
```
curl -X 'POST' \
  'http://localhost:5000/user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "admin@eshop.com",
  "username": "admin",
  "password": "admin",
  "public_id": ""
}'
```
2. Update user to admin by execute sql script below
```sql
UPDATE "user" SET admin=true WHERE email='admin@eshop.com'
```
## SQLAlchemy ORM
[Flask SQLAlchemy document](https://flask-sqlalchemy.palletsprojects.com)

# Flask Restx MVC partern example
```python
from flask import Flask
from flask_restx import Api, Resource, fields
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="1.0", title="TodoMVC API", description="A simple TodoMVC API",)

ns = api.namespace("todos", description="TODO operations")

todo = api.model(
    "Todo",
    {
        "id": fields.Integer(readonly=True, description="The task unique identifier"),
        "task": fields.String(required=True, description="The task details"),
    },
)


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo["id"] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo["id"] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


DAO = TodoDAO()
DAO.create({"task": "Build an API"})
DAO.create({"task": "?????"})
DAO.create({"task": "profit!"})


@ns.route("/")
class TodoList(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @ns.doc("list_todos")
    @ns.marshal_list_with(todo)
    def get(self):
        """List all tasks"""
        return DAO.todos

    @ns.doc("create_todo")
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        """Create a new task"""
        return DAO.create(api.payload), 201


@ns.route("/<int:id>")
@ns.response(404, "Todo not found")
@ns.param("id", "The task identifier")
class Todo(Resource):
    """Show a single todo item and lets you delete them"""

    @ns.doc("get_todo")
    @ns.marshal_with(todo)
    def get(self, id):
        """Fetch a given resource"""
        return DAO.get(id)

    @ns.doc("delete_todo")
    @ns.response(204, "Todo deleted")
    def delete(self, id):
        """Delete a task given its identifier"""
        DAO.delete(id)
        return "", 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        """Update a task given its identifier"""
        return DAO.update(id, api.payload)


if __name__ == "__main__":
    app.run(debug=True)
```
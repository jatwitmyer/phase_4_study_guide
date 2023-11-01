# Phase 4 Code Challenge Study Guide
## 1. Set up your repository terminal
For this project, it's not necessary to set up the front-end server, but you must set up the back-end local host:

```console
pipenv install && pipenv shell
```

## 2. Set up your database
Use the following commands in the shell to create the initial database `app.db`: 

```console
export FLASK_APP=server/app.py
flask db init
flask db migrate
flask db upgrade
python server/seed.py
```
*The FLASK_APP line is required because debug mode is on.*

For any changes to the database structure (such as adding foreign key rows), run the following commands in the shell:

```console
flask db migrate
flask db upgrade
```

## 3. Editing models.py for a many to many relationship
For this study guide, I'll be defining a "many" class and a "join" class, which links the two "many" classes together.

### Many to Many Classes
Navigate to models.py to see examples of how to set up the classes.

Here are the steps to go through while creating models:
- properties
- db.relationship
- association_proxy
- serialization rules
- validations

## 4. Set up Postman
- Download the postman app to your computer.
- In the top-left corner, find the words "My Workspace." To the right of that, click "Import."
- In VS Code, right click on the "code-challenge-name.postman_collection.json" file and select "Reveal in File Explorer"
- Drag the file into the import window in Postman.

This will create a new collection with all of the tests of your routes you will need.

To be able to send fetch requests, get your server running with the following command:
```console
python server/app.py
```

## 5. Edit app.py
### Get All
```python
@app.route('/first_manys', methods=['GET'])
def first_manys():
  if request.method == 'GET':
    first_manys = FirstMany.query.all()
    response = [first_manys.to_dict() for first_many in first_manys]
    return make_response(response, 200)
```
### Post
```python
@app.route('/first_manys', methods=['POST'])
def first_manys():
  if request.method == 'POST':
    form_data = request.get_json()
    try:
      new_many = FirstMany(
        property = form_data['property']
      )
      db.session.add(new_many)
      db.session.commit()
      return make_response(new_many.to_dict(rules = ('-joins', )), 201)
    except ValueError:
      response = {"errors": ["validation errors"]}
      return make_response(response, 403)
```
### Get by ID
```python
@app.route('/first_manys/<int:id>', methods=['GET'])
def first_many_by_id(id):
  first_many = FirstMany.query.filter_by(id=id).first()
  if first_many is None:
    response = {"error": "FirstMany not found"}
    return make_response(response, 404)
  elif request.method == 'GET':
    response = first_many.to_dict()
    return make_response(response, 200)
```
### Patch
```python
@app.route('/first_manys/<int:id>', methods=['PATCH'])
def first_many_by_id(id):
  first_many = FirstMany.query.filter_by(id=id).first()
  if first_many is None:
    response = {"error": "FirstMany not found"}
    return make_response(response, 404)
  elif request.method == 'PATCH':
    form_data = request.get_json()
    try:
      for attr in form_data:
        setattr(first_many, attr, form_data.get(attr))
      db.session.commit()
      response = first_many.to_dict(rules = ('-joins', ))
      return make_response(response, 200)
    except ValueError:
      response = {"errors": ["validation errors"]}
      return make_response(response, 403)
```
### Delete
```python
@app.route('/first_manys/<int:id>', methods=['DELETE'])
def first_many_by_id(id):
  first_many = Activity.query.filter_by(id=id).first()
  if first_many is None:
    response = {"error": "Activity not found"}
    return make_response(response, 404)
  elif request.method == 'DELETE':
    db.session.delete(first_many)
    db.session.commit()
    response = {}
    return make_response(response, 200)
```
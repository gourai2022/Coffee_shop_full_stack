import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def drinks():
    drink = Drink()
    drink_data = drink.short()
    #drink = request.get_json()
    if drink_data:
        return jsonify({
            "success": True, 
            "drinks": drink_data
    }, 200)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def drinks_details():
    drink = Drink()
    drink_details_data = drink.long()
    if drink_details_data:
        return jsonify({
            "success": True, 
            "drinks": drink_details_data
    }, 200)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POSt'])
def new_drink():
    body = request.get_json()
    drink = Drink()
    try:
        if body is not None:
            req_title = body.get("title", None)
            req_recipe = body.get("recipe", None)
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
            new_drink_details_data = drink.long()
            return jsonify({
                "success": True, 
                "drinks": new_drink_details_data
            }, 200)
        else:
            return jsonify({
                "success": False, 
                "Message": "New drink is not inserted"
            }, 422)
    except Exception as e:
            print(f'Exception "{e}" in new_drink()')
            abort(422)
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
def edit_drink(id):
    body = request.get_json()
    try:
        if body is not None:
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = body.get("title", None)
            drink.recipe = body.get("recipe", None)
            drink.update()
            updated_drink_details_data = drink.long()
            return jsonify({
                "success": True, 
                "drinks": updated_drink_details_data
            }, 200)
        else:
            return jsonify({
                "success": False, 
                "Message": "New drink is not updated"
            }, 422)
    except Exception as e:
            print(f'Exception "{e}" in edit_drink()')
            abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['DELETE'])
def delete_drink(id):
    body = request.get_json()
    drink = Drink.query.filter(Drink.id == id).one_or_none()
    try:
        if drink is not None:
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = Drink.query.get(Drink.id == id).title
            drink.recipe = Drink.query.get(Drink.id == id).recipe
            drink.delete()
            deleted_drink_details_data = drink.long()
            return jsonify({
                "success": True, 
                "drinks": deleted_drink_details_data
            }, 200)
        else:
            return jsonify({
                "success": False, 
                "Message": "Drink is not deleted"
            }, 422)
    except Exception as e:
            print(f'Exception "{e}" in delete_drink()')
            abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404, 
        "message": "resource not found"
        }), 404

@app.errorhandler(405)
def invalid_method(error):  
    return jsonify({
        "success": False, 
        "error": 405, 
        "message": "Invalid method"
        }), 405

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500, 
        "message": "Internal server error"
        }), 500

@app.errorhandler(400)
def bad_request(error):        
    return jsonify({
        "success": False, 
        "error": 400, 
        "message": "Bad request"
        }), 400


@app.errorhandler(401)
def unauthorised_user(error):        
    return jsonify({
        "success": False, 
        "error": 401, 
        "message": "Unauthorized user"
        }), 401      
  
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404
'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

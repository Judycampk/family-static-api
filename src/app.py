"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

        request_body = request.get_json()
        members = jackson_family.get_all_members()
        response_body = {
            "family": members
        }
        return jsonify(response_body), 200

@app.route('/members', methods=['POST'])
def add_new():

    request_body = request.get_json()
    if isinstance(request_body, dict):
        members = jackson_family.add_member(request_body)
        response_body = {
        "family": members
        }
        return jsonify(response_body), 200
    else:
        return jsonify({"msg":"Bad Request"}), 400    

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    
    eliminado = jackson_family.delete_member(id)
    if eliminado:
        return jsonify({"msg":"El miembro ha sido eliminado"}), 200
    else:
        return jsonify({"msg":"El id no existe"}), 404

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    
    updatemember=request.get_json()
    modificado = jackson_family.update_member(id,updatemember)
    if modificado:
        return jsonify({"msg":"El miembro ha sido modificado"}), 200
    else:
        return jsonify({"msg":"Bag Request"}), 400


@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    
    member = jackson_family.get_member(id)
    if member != None: 
        return jsonify(member), 200
    else:
        return jsonify({"msg":"El id no existe"}), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

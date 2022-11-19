from flask import Blueprint, request, jsonify
from kardash_plus_inventory.helpers import token_required 
from kardash_plus_inventory.models import db, Kardashian, kardashian_schema, kardashians_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return { 'some' : 'value'}


@api.route('/kardashians', methods = ['POST'])
@token_required
def create_kardashian(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    relationship_to_kardashians = request.json['relationship_to_kardashians']
    industry = request.json['industry']
    net_worth = request.json['net_worth']
    age = request.json['age']
    birthday = request.json['birthday']
    known_for = request.json['known_for']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")

    kardashian = Kardashian(first_name, last_name, relationship_to_kardashians, industry, net_worth, age, birthday, known_for, user_token = user_token)

    db.session.add(kardashian)
    db.session.commit()

    response = kardashian_schema.dump(kardashian) 

    return jsonify(response) 

@api.route('/kardashians', methods = ['GET'])
@token_required
def get_kardashians(current_user_token):
    owner = current_user_token.token
    kardashians = Kardashian.query.filter_by(user_token=owner).all()
    response = kardashians_schema.dump(kardashians)
    return jsonify(response) 



@api.route('/kardashians/<id>', methods = ['GET'])
@token_required
def get_kardashian(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token: 
        kardashian = Kardashian.query.get(id)
        response = kardashian_schema.dump(kardashian)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


@api.route('kardashians/<id>', methods = ['POST', 'PUT'])
@token_required
def update_kardashian(current_user_token, id): 
    kardashian = Kardashian.query.get(id) 
    kardashian.first_name = request.json['first_name']
    kardashian.last_name = request.json['last_name']
    kardashian.relationship_to_kardashians = request.json['relationship_to_kardashians']
    kardashian.industry = request.json['industry']
    kardashian.net_worth = request.json['net_worth']
    kardashian.age = request.json['age']
    kardashian.birthday = request.json['birthday']
    kardashian.known_for = request.json['known_for']
    kardashian.user_token = current_user_token.token

    db.session.commit()
    response = kardashian_schema.dump(kardashian)
    return jsonify(response)


@api.route('/kardashians/<id>', methods = ["DELETE"])
@token_required
def delete_kardashian(current_user_token, id):
    kardashian = Kardashian.query.get(id)
    db.session.delete(kardashian)
    db.sessions.commit()
    response = kardashian_schema.dump(kardashian)
    return jsonify(response)
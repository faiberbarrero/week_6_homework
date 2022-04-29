from flask import Blueprint, request, jsonify

import anime_inventory
from anime_inventory.helpers import token_required
from anime_inventory.models import db, User, Anime, anime_schema, animes_schema

api = Blueprint('api', __name__, url_prefix ='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{'some':'value'}


# CREATE ANIME ENDPOINT
@api.route('/animes', methods = ['POST'])
@token_required
def create_drone(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    year_released = request.json['year_released']
    watch_time = request.json['watch_time']
    number_episodes = request.json['number_episodes']
    number_of_seasons = request.json['number_of_seasons']
    rating = request.json['rating']
    cost_of_production = request.json['cost_of_production']
    animation = request.json['animation']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    anime = Anime(name,description,price, year_released, watch_time, number_episodes, number_of_seasons, rating, cost_of_production, animation, user_token = user_token )

    db.session.add(anime)
    db.session.commit()

    response = anime_schema.dump(anime)
    return jsonify(response)




# RETRIEVE ALL ANIMES ENDPOINT
@api.route('/animes', methods = ['GET'])
@token_required
def get_drones(current_user_token):
    owner = current_user_token.token
    animes = Anime.query.filter_by(user_token = owner).all()
    response = animes_schema.dump(animes)
    return jsonify(response)


# RETRIEVE ONE Anime ENDPOINT
@api.route('/animes/<id>', methods = ['GET'])
@token_required
def get_anime(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        anime = Anime.query.get(id)
        response = anime_schema.dump(anime)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401


# UPDATE ANIME ENDPOINT
@api.route('/animes/<id>', methods = ['POST','PUT'])
@token_required
def update_anime(current_user_token,id):
    anime = Anime.query.get(id) # Grab anime instance

    anime.name = request.json['name']
    anime.description = request.json['description']
    anime.price = request.json['price']
    anime.year_released = request.json['year_released']
    anime.watch_time = request.json['watch_time']
    anime.number_episodes = request.json['number_episodes']
    anime.number_of_seasons = request.json['number_of_seasons']
    anime.rating = request.json['rating']
    anime.cost_of_production = request.json['cost_of_production']
    anime.animation = request.json['animation']
    anime.user_token = current_user_token.token

    db.session.commit()
    response = anime_schema.dump(anime)
    return jsonify(response)


# DELETE ANIME ENDPOINT
@api.route('/animes/<id>', methods = ['DELETE'])
@token_required
def delete_anime(current_user_token, id):
    anime = Anime.query.get(id)
    db.session.delete(anime)
    db.session.commit()
    response = anime_schema.dump(anime)
    return jsonify(response)
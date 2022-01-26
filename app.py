from flask import Flask, render_template, request
import requests
from os import getenv, path
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from dotenv import load_dotenv
from flask_restful import Api, Resource
import json
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


dist_dir = path.abspath('/dist')
static_dir = path.abspath('/static')

app = Flask(__name__, static_folder=static_dir, template_folder=dist_dir)

load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Pokemon = Base.classes.pokemons

auth = HTTPBasicAuth()

users = {
    str(getenv('USERNAME')): generate_password_hash(str(getenv('PASSWORD')))
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


api = Api(app)

class Pokemons(Resource):
    @auth.login_required
    def get(self):
        pokemons = db.session.query(Pokemon).all()
        poke_dict = {}
        for pokemon in pokemons:
            poke_dict[pokemon.id] = {
                'identifier': pokemon.identifier,
                'species_id': pokemon.species_id,
                'height': pokemon.height,
                'weight': pokemon.weight,
                'base_experience': pokemon.base_experience,
                'order': pokemon.order,
                'is_default': pokemon.is_default
            }
        return json.dumps(poke_dict)

class PokemonLookup(Resource):
    @auth.login_required
    def get(self, id):
        pokemon = db.session.query(Pokemon).filter_by(id=id).first()
        if pokemon:
            return json.dumps({
                'name': pokemon.identifier,
                'type': pokemon.species_id,
                'height': pokemon.height,
                'weight': pokemon.weight,
                'experience': pokemon.base_experience
            })
        else:
            return json.dumps({'error': 'Pokemon not found'})
    
    @auth.login_required
    def put(self, id):
        data = request.get_json()
        updates = data['load']
        filter = {updates[1]: updates[0]}
        pokemon = db.session.query(Pokemon).filter_by(id=id).first()
        if pokemon:
            setattr(pokemon, updates[1], updates[0])
            db.session.commit()
            if db.session.query(Pokemon).filter_by(**filter).first():
                return json.dumps({'success': f'{updates[1]} attribute of pokemon with the id={pokemon.id} have been updated with {updates[0]}'})
            else:
                return json.dumps({'error': 'Could not update the database'})
        else:
            return json.dumps({'error': 'Pokemon not found'})


api.add_resource(Pokemons, '/api/pokemons/')
api.add_resource(PokemonLookup, '/api/pokemons/<int:id>')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
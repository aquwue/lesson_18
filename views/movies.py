from flask_restx import Resource, Namespace
from flask import request
from models import Movie, MovieSchema
from setup_db import db


movies_ns = Namespace('movies')


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        rs = db.session.query(Movie).all()
        if director_id is not None:
            rs = rs.filter(Movie.director_id == director_id)
        if genre_id is not None:
            rs = rs.filter(Movie.genre_id == genre_id)
        if director_id is not None and genre_id is not None:
            rs = rs.filter(Movie.director_id == director_id, Movie.genre_id == genre_id)
        res = MovieSchema(many=True).dump(rs)
        return res, 200

    def post(self):
        r_json = request.json
        add_movie = Movie(**r_json)
        with db.session.begin():
            db.session.add(add_movie)
        return "", 201


@movies_ns.route('/<int:rid>')
class MovieView(Resource):
    def get(self, rid):
        r = db.session.query(Movie).get(rid)
        sm_d = MovieSchema().dump(r)
        return sm_d, 200

    def delete(self, rid: int):
        movie = db.session.query(Movie).get(rid)
        if not movie:
            return 'Not founded', 404
        else:
            db.session.delete(movie)
            db.session.commit()
            return '', 204

    def put(self, rid: int):
        movie = db.session.query(Movie).get(rid)
        req_json = request.json
        if not movie:
            return 'Not founded', 404
        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.rating = req_json.get("rating")
        db.session.add(movie)
        db.session.commit()
        return "", 204
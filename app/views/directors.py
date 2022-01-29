from flask_restx import Resource, Namespace

from app.models import Director, DirectorSchema
from app.setup_db import db


directors_ns = Namespace('directors')


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        rs = db.session.query(Director).all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200


@directors_ns.route('/<int:rid>')
class DirectorView(Resource):
    def get(self, rid):
        r = db.session.query(Director).get(rid)
        sm_d = DirectorSchema().dump(r)
        return sm_d, 200
from sqlalchemy import desc
from flask import Blueprint, jsonify, request, abort
from webargs import fields, validate
from webargs.flaskparser import parser
from requests_html import HTMLSession

from ..flask_extensions import db
from ..models.demons import Demon, Race
from ..models.fusions import Fusion
from ..models.skills import Skill
from ..utils.api import paginate, load_data

blueprint = Blueprint('demons', __name__)

@blueprint.route('/demons', methods=['GET'], strict_slashes=False)
@parser.use_args({
    'page': fields.Integer(missing=1),
    'order': fields.String(missing='level'),
    'desc': fields.Boolean(missing=False),
    'max_level': fields.Integer(min=1,max=100),
    'race': fields.String(validate=validate.OneOf([r.value for r in Race])),
    'name': fields.String(),
    'ids': fields.DelimitedList(fields.Integer(), delimiter=','),
}, location='query_and_json')
def get_all(args):
    query = db.session.query(Demon)

    if (ids := args.get('ids')):
        try:
            return jsonify([query.get(idx).to_dict() for idx in ids])
        except AttributeError:
            abort(404)

    order = desc(args['order']) if args['desc'] else args['order']
    query = query.order_by(order)

    if max_level := args.get('max_level'):
        query = query.filter(Demon.level <= max_level)

    if race := args.get('race'):
        query = query.filter(Demon.race == race)

    if name := args.get('name'):
        query = query.filter(Demon.name.ilike(f'%{name}%'))

    return jsonify(paginate(args['page'], query))

@blueprint.route('/demons/<int:demon_id>/lore', methods=['GET'], strict_slashes=False)
def lore_text(demon_id):
    demon_name = db.session.query(Demon).get(demon_id).name
    session = HTMLSession()

    wiki_url = f'https://megamitensei.fandom.com/wiki/{demon_name}'
    response_html = session.get(wiki_url).html

    text = [el.text for el in response_html.find('nav.toc + h2 + p, nav.toc + h2 + p + p')]
    return jsonify(text)



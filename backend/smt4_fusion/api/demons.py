from sqlalchemy import desc, alias
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

@blueprint.route('/', methods=['GET'], strict_slashes=False)
@parser.use_args({
    'page': fields.Integer(missing=1),
    'order': fields.String(missing='level'),
    'desc': fields.Boolean(missing=False),
    'max_level': fields.Integer(min=1,max=100),
    'race': fields.String(validate=validate.OneOf([r.value for r in Race])),
    'name': fields.String(),
    'ids': fields.DelimitedList(fields.Integer(), delimiter=','),
}, location='query_and_json')
def demon_query(args):
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

@blueprint.route('/<int:demon_id>/lore', methods=['GET'], strict_slashes=False)
def demon_lore(demon_id):
    demon_name = db.session.query(Demon).get(demon_id).name
    session = HTMLSession()

    wiki_url = f'https://megamitensei.fandom.com/wiki/{demon_name}'
    response_html = session.get(wiki_url).html

    text = [el.text for el in response_html.find('nav.toc + h2 + p, nav.toc + h2 + p + p')]
    return jsonify(text)


@blueprint.route('/<int:demon_id>/skills', methods=['GET'], strict_slashes=False)
def demon_skills(demon_id):
    learn_skills = db.session.query(Demon).get(demon_id).learn_skills

    innate_skills = [s.skill.to_dict() for s in learn_skills if s.level == 0]
    level_up_skills = { s.level: s.skill.to_dict() for s in reversed(learn_skills) if s.level > 0 }

    return jsonify({
        'level_up': level_up_skills,
        'innate': innate_skills,
    })

@blueprint.route('/<int:demon_id>/recipes', methods=['GET'], strict_slashes=False, defaults={'page': 1})
@blueprint.route('/<int:demon_id>/recipes/<int:page>', methods=['GET'], strict_slashes=False)
def demon_recipes(demon_id, page):
    recipes = db.session.query(Fusion) \
                        .join(Demon, Fusion.result) \
                        .filter(Demon.id == demon_id)

    return jsonify(paginate(page, recipes))

@blueprint.route('/<int:demon_id>/uses', methods=['GET'], strict_slashes=False, defaults={'page': 1})
@blueprint.route('/<int:demon_id>/uses/<int:page>', methods=['GET'], strict_slashes=False)
def demon_uses(demon_id, page):
    recipes = db.session.query(Fusion) \
                        .join(Demon, Fusion.ingredients) \
                        .filter(Demon.id == demon_id)

    return jsonify(paginate(page, recipes))

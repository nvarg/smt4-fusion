from flask import Blueprint, jsonify, request

from ..flask_extensions import db
from ..models.demons import Demon
from ..models.fusions import *
from ..models.skills import *

from ..utils.api import paginate

blueprint = Blueprint('demons', 'smt4_fusion')

@blueprint.route('/demons', methods=['GET'], strict_slashes=False)
def get_all():
    page = int(request.args.get('page', 1))
    demons = db.session.query(Demon)
    return jsonify(paginate(page, demons))

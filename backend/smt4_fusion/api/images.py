from io import BytesIO
from functools import lru_cache

from flask import Blueprint, abort, Response
from webargs import fields
from webargs.flaskparser import parser
from PIL import Image
from PIL.ImageColor import getrgb

from ..utils.api import freeze_args
from ..utils.api import load_data # registers "query_and_json" location
from ..utils.images import crop_to_content, replace_alpha, crop_largest_object

blueprint = Blueprint('images', __name__)

@blueprint.route('/images/<path:filename>', methods=['GET'], strict_slashes=False)
@parser.use_args({
    'max_height': fields.Integer(missing=200),
    'max_width': fields.Integer(missing=200),
    'background_color': fields.String(missing='#fff'),
}, location='query_and_json')
@freeze_args
@lru_cache(maxsize=128)
def get(args, filename):
    try:
        with Image.open(f'data/images/{filename}.png', mode='r') as image:
            cleaned_image = crop_largest_object(image)

            cleaned_image = crop_to_content(
                img=cleaned_image,
                bg_color=getrgb('#0000')
            )

            cleaned_image = replace_alpha(
                img=cleaned_image,
                color=getrgb(args['background_color']),
            )

            size = args['max_width'], args['max_height']
            cleaned_image.thumbnail(size, Image.ANTIALIAS)

            data = BytesIO()
            cleaned_image.save(data, 'JPEG')
            data.seek(0)
            return Response(response=data.read(), status=200, mimetype='image/jpg')
    except FileNotFoundError:
        abort(404)

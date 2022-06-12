from flask import Blueprint, render_template

bp = Blueprint('sites', __name__, url_prefix = '/sites', template_folder = 'templates/sites')

@bp.route('/', methods = ['GET'])
def create_site():
    return render_template('create.html')
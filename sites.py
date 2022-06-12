from flask import Blueprint, render_template

bp = Blueprint('sites', __name__, url_prefix = '/sites', template_folder = 'templates/sites')

@bp.route('/', methods = ['GET'])
def index():
    sites = [{'name': 'test'}]
    return render_template('sites_index.html', sites = sites)

@bp.route('/create', methods = ['GET'])
def create():
    return render_template('create.html')
from flask import Blueprint, render_template
import pulumi_aws as aws

bp = Blueprint('sites', __name__, url_prefix = '/sites', template_folder = 'templates/sites')

def create_program(content):
    index_document = 'index.html'
    bucket = aws.s3.Bucket(
        name = 'bucket',
        acl = 'public-read', # Access control list
        policy = (lambda path: open(path))('policy.json'),
        website = aws.s3.BucketWebsiteArgs(index_document = index_document)
    )
    aws.s3.BucketObject( # Creates the HTML document
        bucket = bucket.id,
        content = content,
        key = index_document
    )

@bp.route('/', methods = ['GET'])
def index():
    sites = [{'name': 'test'}]
    return render_template('sites_index.html', sites = sites)

@bp.route('/create', methods = ['GET'])
def create():
    return render_template('create.html')
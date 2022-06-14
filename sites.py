from flask import Blueprint, current_app, render_template
import json
import pulumi
import pulumi_aws as aws
import pulumi.automation as auto

bp = Blueprint('sites', __name__, url_prefix = '/sites', template_folder = 'templates/sites')

def create_program(content):
    index_document = 'index.html'
    bucket = aws.s3.Bucket(
        'bucket',
        acl = 'public-read', # Access control list
        website = aws.s3.BucketWebsiteArgs(index_document = index_document)
    )
    aws.s3.BucketPolicy(
        'bucket-policy',
        bucket = bucket.id,
        policy = bucket.id.apply(
            lambda id: json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{id}/*"],
                    },
                }
            )
        ),
    )
    aws.s3.BucketObject( # Creates the HTML document
        'index',
        bucket = bucket.id,
        content = content,
        key = index_document,
        content_type = 'text/html'
    )
    pulumi.export('url', bucket.website_endpoint)

@bp.route('/', methods = ['GET'])
def index():
    sites = []
    ws = auto.LocalWorkspace(
        project_settings = auto.ProjectSettings(
            name = current_app.config['PULUMI_ORGANISATION'],
            runtime = 'python'
        )
    )
    for stack_name in ws.list_stacks():
        stack = auto.select_stack(stack_name = stack_name)
        url = stack.outputs().get('url')
        sites.append({'name': stack_name, 'url': url})
    return render_template('sites_index.html', sites = sites)

@bp.route('/create', methods = ['GET'])
def create():
    def encapsulated_program():
        return create_program('Abcd')
    stack = auto.create_stack(
        stack_name = 'dev',
        project_name = current_app.config['PULUMI_PROJECT_NAME'],
        program = encapsulated_program
    )
    stack.set_config('aws:region', auto.ConfigValue('us-east-1'))
    stack.up(on_output = print)
    return render_template('create.html')
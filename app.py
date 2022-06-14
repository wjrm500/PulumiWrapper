from dotenv import load_dotenv
from flask import Flask, render_template
import sites

load_dotenv()
app = Flask(__name__)
app.register_blueprint(sites.bp)
app.config['PULUMI_ORGANISATION'] = 'wjrm500'
app.config['PULUMI_PROJECT_NAME'] = 'pulumi-wrapper'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
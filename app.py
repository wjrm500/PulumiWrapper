from flask import Flask, render_template
import sites

app = Flask(__name__)
app.register_blueprint(sites.bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
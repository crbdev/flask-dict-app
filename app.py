from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
#import flask_whooshalchemy as wa
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'char.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
#init db
db = SQLAlchemy(app)
#init ma
ma = Marshmallow(app)
#init whoosh
#wa.whoost_index(app, post)

#dict entry class/model
class Chardb(db.Model):
    __searchable__ = ['pinyin']

    id = db.Column(db.Integer, primary_key=True)
    char_simp = db.Column(db.String(200))
    char_trad = db.Column(db.String(100), unique=True)
    pinyin = db.Column(db.String(100))
    definition = db.Column(db.String(500))

    def __init__(self, char_trad, char_simp, pinyin, definition):
        self.char_simp = char_simp
        self.char_trad = char_trad
        self.pinyin = pinyin
        self.definition = definition

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/search_results')
def search_results():
    results = Chardb.query.all()

    return render_template('search_results.html', results=results)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query_parameters = request.args
    results = Chardb.query.filter_by(pinyin=query_parameters.get('query'))
    return render_template('search_results.html', results=results)

if __name__ =='__main__':
    app.run(debug=True)
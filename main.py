# save this as app.py
#from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime
#from flask_marshmallow import Marshmallow
#import os
import sys
sys.path.append('backend')
sys.path.append('static')
import backend.index
from backend.index import app
#from config import db

#CASA from sqlalchemy_imageattach.entity import Image, image_attachment



#app = Flask(__name__) # Variable app mit Info vom Flask Proyekt

#basedir = os.path.abspath(os.path.dirname(__file__))

#app.app_context().push()

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

#class Pflanze(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(40), nullable=True)
    #wissenschaft_name = db.Column(db.String(40), nullable=True)
    #familie = db.Column(db.String(40), nullable=True)
    #vegetationszone = db.Column(db.String(40), nullable=True)
    ## foto = db.Column(BLOB), nullable=True) foto = image_attachment('Foto')
    #will_sonne = db.Column(db.String(40), nullable=True)
    #gefahr = db.Column(db.String(40), nullable=True)
    #created_at = db.Column(db.DateTime(), default=datetime.utcnow)

#with app.app_context():
#    db.create_all()

#@app.route("/") # Rute hinzufügen / für start Seite, / contact für die Kontakt Seite, / legal für Impresum
#def start_page():
    #return "<h1>Hello, Hydroflora!</h1><a href='https://google.de'>Google</a>" # HTML Code für Titel und Link, Chat Messenger BEREIT
    #return render_template('index.html')

if __name__ == "__main__": # Ausführen
    app.run(debug=True) # Starten
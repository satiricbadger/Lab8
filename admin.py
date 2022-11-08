from pprint import pprint
from flask import Flask
from flask import request
from flask import abort, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import json


app = Flask(__name__)
app.secret_key = 'super secret key'

with app.app_context():
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gradebook.sqlite"
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='microblog', template_mode='bootstrap3')

    db = SQLAlchemy(app)
    

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        realname = db.Column(db.String, nullable = False)
        username = db.Column(db.String, unique=True, nullable=False)
        
        grade = db.Column(db.Float, nullable = False)
        email = db.Column(db.String, unique=True, nullable=False)
    db.create_all()
    admin.add_view(ModelView(User, db.session))
    User.query.filter_by(id = 1).delete()
    db.session.commit()
    db.session.add(User(username = "tester",realname = "Tester",grade=89.7, email = "tester@test.com"))
    db.session.commit()






if __name__ == "__main__":
    app.run()

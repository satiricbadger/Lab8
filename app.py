from pprint import pprint
from flask import Flask
from flask import request
from flask import abort,render_template
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

    class Student(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        name = db.Column(db.String, unique = True, nullable = False)
        grade = db.Column(db.Float, nullable = False)
    db.create_all()
    admin.add_view(ModelView(Student, db.session)) 
    #for name in ["Corn", "Tomato", "Potato"]:
    #   db.session.add(Student(name=name, grade=90.0))
    #db.session.add(Student(name = "Crotate",grade=89.7))
    #db.session.commit()


    @app.route('/grades', methods = ['GET'])
    def get_grades():
        print('Getting grades...')
        result = Student.query.all()
        grades = {}
        for r in result:
            grades[r.name] = r.grade
        return grades

    @app.route('/grades/<string:name>' , methods = ['GET']) 
    def get_student(name):
        result = Student.query.all()
        for r in result:
            if(name == r.name):
                return r.grade
    
    @app.route('/grades', methods = ['POST'])
    def add_grade():
        contents = request.get_json(silent = True)
        db.session.add(Student(name=contents["name"], grade=contents["grade"] ))
        db.session.commit()
        return "success!"

    @app.route('/grades/<string:rName>', methods =['PUT'])
    def editGrade(rName):
        result = Student.query.all()
        contents = request.get_json(silent = True)
        
        StudentName = Student.query.filter_by(name = rName).first()
        StudentName.grade = contents["grade"]
        db.session.commit()
        return "success!"
    
    @app.route('/grades/<string:rName>', methods =['DELETE'])
    def deleteGrade(rName):
        result = Student.query.all()
        contents = request.get_json(silent = True)
        deletedUser = Student.query.filter_by(name = rName).first()
        db.session.delete(deletedUser)
        db.session.commit() 
        return "success!"

    
    








if __name__ == "__main__":
    app.run()
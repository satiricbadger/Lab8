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
    

    class Student(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        userID = db.Column(db.String, unique=True, nullable=False)
        name = db.Column(db.String, unique = False, nullable = False)
    
    class Users( db.Model):
        id = db.Column(db.Integer, primary_key=True)
        userID = db.Column(db.String, unique = True, nullable = False)
        password = db.Column(db.String, unique = False, nullable = False)
        
    
    class Classes(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        classID = db.Column(db.String, unique = True, nullable = True)
        teacherName = db.Column(db.String, unique = False, nullable = True)
        enrolledNum = db.Column(db.Integer, unique = False, nullable = True)
        maxEnrollment = db.Column( db.Integer, unique = False, nullable = True)
        classTime = db.Column(db.Integer, unique = False, nullable = True)
    
    class Teacher(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        teacherName = db.Column(db.String, unique = False, nullable = True)
        userID = db.Column(db.String, unique = True, nullable = False)

    class Enrollment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        classID = db.Column(db.String, unique = True, nullable = True)
        userID = db.Column(db.String, unique = False, nullable = False)
        grade = db.Column(db.Float, unique = False, nullable = True)

    db.create_all()
    admin.add_view(ModelView(Student, db.session))
    admin.add_view(ModelView(Users, db.session))
    admin.add_view(ModelView(Teacher, db.session))
    admin.add_view(ModelView(Classes, db.session))
    admin.add_view(ModelView(Enrollment, db.session))

    #STUDENT FUNCTIONS

    @app.route('/<string:username>', methods = ['GET'])
    def get_studentID(username):
        student = Student.query.all()
        result = db.session.execute(db.select(Student.name).where(Student.userID == username))
        nameDictionary = [dict(r) for r in result.all()]
        for nameDict in nameDictionary:
            return nameDict["name"]
        return nameDict["name"]
            
    @app.route('/<string:username>/classes', methods = ['GET'])
    def get_class(username):
        print('Getting class...')
        enroll = Enrollment.query.all()
        #db.session.execute(db.select(Student).where(Student.name == name ))
        result = db.session.execute(db.select(Enrollment.classID).where(Enrollment.userID == username)) #Select the parts of enrollment where classID is the same as the ID of the student
        #print(type(result.all()))

        classDictionary = [dict(r) for r in result.all()]
        for classDict in classDictionary:
            classDict["classID"]
        return classDict["classID"]
    
    @app.route('/school/classes')
    def getAllClass():
        allClass = Classes.query.all()
        classes = {}
        for i in allClass:
            classes[i.id] = i.classID
        return classes

    @app.route('/<string:username>/edit', methods = ['POST'])
    def editGrades(username):
        teacher = Teacher.query.all()
        editStudent = Student.query.all()

        return "0"
    @app.route('/enroll', methods = ['PUT'])
    def editEnrollment():
        #Send json of user and class name
        #Load up all the categories we may use and edit
        
        targetStudent = Student.query.all()
        classUpdate = Classes.query.all()  
        updateEnroll = Enrollment.query.all()
        contents = request.get_json(silent = True)
        json.loads(contents)
        targetClassNum = db.session.execute(db.select(Classes.enrolledNum).where(Classes.classID == contents["classname"]))
        targetClassMax = db.session.execute(db.select(Classes.maxEnrollment).where(Classes.classID == contents["classname"]))
        #Check if we have space!
        if(targetClassNum <= targetClassMax):
            #Perform the logic here
            #Upon successful checking of space, we can now add the student to the class. This should be done in enrollment, where we have classID, userID, and grade.
            db.session.add(Enrollment(classID=contents["classname"], userID = contents["username"], grade = 100.0 ))
            #Now we need to update the enrollmentNum in Classes.
            #Retrieve the class by using classID as the filter.
            updatedNum = Classes.query.filter_by(classID = contents["classname"])
            updatedNum.enrollmentNum = updatedNum.enrollmentNum +1
            
        db.session.commit()
        return "check"
        

    





if __name__ == "__main__":
    app.run(debug = True)

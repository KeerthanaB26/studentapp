from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    usn = db.Column(db.String(20), nullable=False)
    branch = db.Column(db.String(20), nullable=False)
    semester = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.Date)
    age = db.Column(db.String(20), nullable=False)
    phno= db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    fathername = db.Column(db.String(20), nullable=False)
    fatherphno = db.Column(db.String(20), nullable=False)
    mothername = db.Column(db.String(20), nullable=False)
    motherphno= db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    students = Students.query.all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        usn = request.form['usn']
        branch = request.form['branch']
        semester = request.form['semester']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        age = request.form['age']
        phno = request.form['phno']
        email = request.form['email']
        address = request.form['address']
        fathername = request.form['fathername']
        fatherphno = request.form['fatherphno']
        mothername = request.form['mothername']
        motherphno = request.form['motherphno']
        print(f"nme is: {name}, usn is: {usn}, branch is: {branch}, semester is: {semester}, dob is: {dob}, age is: {age}, phno is: {phno}, email is: {email}, address is: {address}, fatheranme is: {fathername}, fatherphno is: {fatherphno}, motheranme is: {mothername}, motherphno is: {motherphno}")
        new_student = Students(name=name, usn=usn, branch=branch, semester=semester, dob=dob, age=age, phno=phno, email=email, address=address, fathername=fathername, fatherphno=fatherphno, mothername=mothername, motherphno=motherphno)
        print("new_task: {}".format(new_student))
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('add_student'))
    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Students.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.usn = request.form['usn']
        student.branch =request.form['branch']
        student.semester = request.form['semester']
        dob_str = request.form['dob'].strip()
        student.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        student.age = request.form['age']
        student.phno = request.form['phno']
        student.email = request.form['email']
        student.address = request.form['address']
        student.fathername = request.form['fathername']
        student.fatherphno = request.form['fatherphno']
        student.mothername = request.form['mothername']
        student.motherphno = request.form['motherphno']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Students.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
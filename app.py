from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import sqlite3
import html
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

@app.route('/')
def index():
    # RAW Query
    students = db.session.execute(text('SELECT * FROM student')).fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():

    name = request.form['name'].strip()
    age = request.form['age'].strip()
    grade = request.form['grade'].strip()

    # name = html.escape(request.form['name'].strip())
    # age = html.escape(request.form['age'].strip())
    # grade = html.escape(request.form['grade'].strip())
    
    Name validation
    if len(name) < 2 or len(name) > 100:
        return "Invalid name length", 400
    elif not re.match(r"^[A-Za-z0-9\s\-\'\.\,]+$", name):
        return "Name contains disallowed characters", 400

    # Age validation
    try:
        age_int = int(age)
        if age_int < 1 or age_int > 120:
            return "Invalid age range", 400
    except ValueError:
        return "Age must be a number", 400
    
    # Grade validation
        if len(grade) < 2 or len(grade) > 10:
            return "Invalid grade length", 400
        elif not re.match(r"^[A-Za-z0-9\s\-\'\.\,]+$", grade):
            return "Grade contains disallowed characters", 400

    connection = sqlite3.connect('instance/students.db')
    cursor = connection.cursor()

    # RAW Query
    # db.session.execute(
    #     text("INSERT INTO student (name, age, grade) VALUES (:name, :age, :grade)"),
    #     {'name': name, 'age': age, 'grade': grade}
    # )
    # db.session.commit()
    db.session.execute(
        text("INSERT INTO student (name, age, grade) VALUES (:name, :age, :grade)"), 
        {"name": name, "age": age, "grade": grade}
        )
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/delete/<string:id>') 
def delete_student(id):
    # RAW Query
    db.session.execute(text("DELETE FROM student WHERE id = :id"),{'id': id})
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        
        # name = html.escape(request.form['name'].strip())
        # age = html.escape(request.form['age'].strip())
        # grade = html.escape(request.form['grade'].strip())
        
        # Name validation
        if len(name) < 2 or len(name) > 100:
            return "Invalid name length", 400
        elif not re.match(r"^[A-Za-z0-9\s\-\'\.\,]+$", name):
            return "Name contains disallowed characters", 400

        # Age validation
        try:
            age_int = int(age)
            if age_int < 1 or age_int > 120:
                return "Invalid age range", 400
        except ValueError:
            return "Age must be a number", 400

        # Grade validation
        if len(grade) < 2 or len(grade) > 10:
            return "Invalid grade length", 400
        elif not re.match(r"^[A-Za-z0-9\s\-\'\.\,]+$", grade):
            return "Grade contains disallowed characters", 400

        # RAW Query
        db.session.execute(text("UPDATE student SET name=:name, age=:age, grade=:grade WHERE id=:id"),
            {'id': id, 'name': name, 'age': age, 'grade': grade})
        db.session.commit()
        return redirect(url_for('index'))
    else:
        # RAW Query
        student = db.session.execute(text(f"SELECT * FROM student WHERE id={id}")).fetchone()
        return render_template('edit.html', student=student)

# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True)


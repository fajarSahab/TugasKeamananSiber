from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
db = SQLAlchemy(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/unauthorized')
def unauthorized():
    return render_template('unauthorized.html'), 403

@app.route('/')
@login_required
def index():
    # RAW Query
    students = db.session.execute(text('SELECT * FROM student')).fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['POST'])
@login_required
def add_student():

    # strip agar input seperti spasi tidak masuk
    if not current_user.is_admin():
        return redirect(url_for('unauthorized'))
    
    name = request.form['name'].strip()
    age = request.form['age']
    grade = request.form['grade'].strip()
    
    # Name validation
    if len(name) < 2 or len(name) > 100:
        return "Invalid name length", 400

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
@login_required
def delete_student(id):
    if not current_user.is_admin():
        return redirect(url_for('unauthorized'))
    
    # RAW Query
    db.session.execute(text("DELETE FROM student WHERE id = :id"),{'id': id})
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_student(id):
    if not current_user.is_admin():
        return redirect(url_for('unauthorized'))
    
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        grade = request.form['grade']
        
        # Name validation
        if len(name) < 2 or len(name) > 100:
            return "Invalid name length", 400

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
        # Create default admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                password=generate_password_hash('password'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
    app.run(host='0.0.0.0', port=5000, debug=True)


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///class8D.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# موديل الطلاب
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    age = db.Column(db.Integer, nullable=False)

# موديل المدرسين
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    subject = db.Column(db.String(100), nullable=False)

# الصفحة الرئيسية
@app.route("/")
def home():
    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template("index.html", students=students, teachers=teachers)

# إضافة طالب
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        image = request.form.get("Img")
        description = request.form.get("description")

        new_student = Student(name=name , image=image, age=age, description=description)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("add_student.html")

# إضافة مدرس
@app.route("/add_teacher", methods=["GET", "POST"])
def add_teacher():
    if request.method == "POST":
        name = request.form["name"]
        subject = request.form["subject"]
        description = request.form.get("description")

        new_teacher = Teacher(name=name, subject=subject, description=description)
        db.session.add(new_teacher)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("add_teacher.html")
@app.route("/edit_all", methods=["GET", "POST"])
def edit_all():
    if request.method == "POST":
        user_type = request.form["type"]
        user_id = request.form["id"]

        if user_type == "student":
            user = Student.query.get(user_id)
            if user:
                user.name = request.form["name"]
                user.age = request.form["age"]
                user.description = request.form["description"]
                user.image = request.form["image"]
        elif user_type == "teacher":
            user = Teacher.query.get(user_id)
            if user:
                user.name = request.form["name"]
                user.subject = request.form["subject"]
                user.description = request.form["description"]

        db.session.commit()
        return redirect(url_for("edit_all"))

    students = Student.query.all()
    teachers = Teacher.query.all()
    return render_template("edit_all.html", students=students, teachers=teachers)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5003)

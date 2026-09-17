from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required
from sqlalchemy import or_
from models import Student, db


students_bp = Blueprint("students", __name__)


@students_bp.route("/")
def index():
    return redirect(url_for("students.dashboard"))


@students_bp.route("/dashboard")
@login_required
def dashboard():
    total = Student.query.count()
    courses = db.session.query(Student.course).distinct().count()
    recent_students = Student.query.order_by(Student.id.desc()).limit(5).all()
    return render_template(
        "dashboard.html", total=total, courses=courses, recent_students=recent_students
    )


@students_bp.route("/students")
@login_required
def list_students():
    search = request.args.get("q", "").strip()
    query = Student.query
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                Student.name.ilike(pattern),
                Student.roll_number.ilike(pattern),
                Student.email.ilike(pattern),
                Student.course.ilike(pattern),
            )
        )
    students = query.order_by(Student.id.desc()).all()
    return render_template("students.html", students=students, search=search)


@students_bp.route("/students/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        data = {key: request.form.get(key, "").strip() for key in [
            "roll_number", "name", "email", "phone", "course", "semester", "city"
        ]}
        if not data["roll_number"] or not data["name"] or not data["email"] or not data["course"]:
            flash("Roll number, name, email and course are required.", "danger")
            return render_template("add_student.html", student=data)
        try:
            semester = int(data["semester"])
            if semester < 1 or semester > 12:
                raise ValueError
        except ValueError:
            flash("Semester must be a number between 1 and 12.", "danger")
            return render_template("add_student.html", student=data)
        if Student.query.filter_by(roll_number=data["roll_number"]).first():
            flash("Roll number already exists.", "danger")
            return render_template("add_student.html", student=data)
        if Student.query.filter_by(email=data["email"]).first():
            flash("Email already exists.", "danger")
            return render_template("add_student.html", student=data)

        student = Student(
            roll_number=data["roll_number"], name=data["name"], email=data["email"],
            phone=data["phone"], course=data["course"], semester=semester, city=data["city"]
        )
        db.session.add(student)
        db.session.commit()
        flash("Student added successfully.", "success")
        return redirect(url_for("students.list_students"))
    return render_template("add_student.html", student={})


@students_bp.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = db.get_or_404(Student, student_id)
    if request.method == "POST":
        student.roll_number = request.form.get("roll_number", "").strip()
        student.name = request.form.get("name", "").strip()
        student.email = request.form.get("email", "").strip()
        student.phone = request.form.get("phone", "").strip()
        student.course = request.form.get("course", "").strip()
        student.city = request.form.get("city", "").strip()
        try:
            student.semester = int(request.form.get("semester", "0"))
        except ValueError:
            student.semester = 0
        if not student.roll_number or not student.name or not student.email or not student.course or not (1 <= student.semester <= 12):
            flash("Please enter valid values in all required fields.", "danger")
            return render_template("edit_student.html", student=student)
        duplicate_roll = Student.query.filter(Student.roll_number == student.roll_number, Student.id != student.id).first()
        duplicate_email = Student.query.filter(Student.email == student.email, Student.id != student.id).first()
        if duplicate_roll or duplicate_email:
            flash("Roll number or email already belongs to another student.", "danger")
            return render_template("edit_student.html", student=student)
        db.session.commit()
        flash("Student updated successfully.", "success")
        return redirect(url_for("students.list_students"))
    return render_template("edit_student.html", student=student)


@students_bp.post("/students/<int:student_id>/delete")
@login_required
def delete_student(student_id):
    student = db.get_or_404(Student, student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Student deleted successfully.", "success")
    return redirect(url_for("students.list_students"))

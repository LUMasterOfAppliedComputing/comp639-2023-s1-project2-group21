from flask import Blueprint, render_template

from queries import StudentQueries

studentRoute = Blueprint('StudentRoute', __name__)


@studentRoute.route('/student/getAll')
def get_users():
    students = StudentQueries.getAll()
    return render_template("studentPortal.html", students=students)

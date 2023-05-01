from flask import Blueprint, render_template

from queries import StudentProjectQueries

studentProjectRoute = Blueprint('StudentProjectRoute', __name__)


@studentProjectRoute.route('/studentProject/getAll')
def get_users():
    stuProjects = StudentProjectQueries.getAll()
    return render_template("studentProject.html", stuProjects=stuProjects)

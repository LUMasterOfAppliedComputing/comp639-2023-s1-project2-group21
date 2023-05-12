from flask import Blueprint, render_template

from queries import ProjectQueries

projectRoute = Blueprint('projectRoute', __name__)


@projectRoute.route('/projectRoute/getAll')
def get_users():
    projects = ProjectQueries.getAll()
    return render_template("project.html", projects=projects)



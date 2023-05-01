from flask import Blueprint, render_template

from queries import InterviewsQueries

interviewRoute = Blueprint('interviewRoute', __name__)


@interviewRoute.route('/interviewRoute/getAll')
def get_users():
    interviews = InterviewsQueries.getAll()
    return render_template("interviews.html", interviews=interviews)

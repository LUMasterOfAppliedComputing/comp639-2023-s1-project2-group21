from flask import Blueprint, render_template

from queries import QuestionQueries

questionRoute = Blueprint('questionRoute', __name__)


@questionRoute.route('/questionRoute/getAll')
def get_users():
    questions = QuestionQueries.getAll()
    return render_template("question.html", questions=questions)

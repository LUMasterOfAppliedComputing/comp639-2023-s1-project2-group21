import json

from flask import Blueprint, render_template

from queries import QuestionQueries

questionRoute = Blueprint('questionRoute', __name__)


@questionRoute.route('/questionRoute/getAll')
def get_users():
    questions = QuestionQueries.getAll()
    for que in questions:
        str = que['question'].replace('\r', '').replace('\n', '')
        strjson = json.loads(str)
        que['question']=strjson
    return render_template("question.html", questions=questions)

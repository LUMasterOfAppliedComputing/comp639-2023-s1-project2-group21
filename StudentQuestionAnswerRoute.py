from flask import Blueprint, render_template

from queries import QuestionAnswerQueries

studentQuestionsRoute = Blueprint('studentQuestionsRoute', __name__)


@studentQuestionsRoute.route('/studentQuestions/getAll')
def get_users():
    questionAnswers = QuestionAnswerQueries.getAll()
    return render_template("stuQuestion.html", questionAnswers=questionAnswers)

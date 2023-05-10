from flask import Blueprint, render_template, request, make_response, jsonify

from queries import QuestionAnswerQueries

studentQuestionsRoute = Blueprint('studentQuestionsRoute', __name__)


@studentQuestionsRoute.route('/studentQuestions/getAll')
def get_users():
    questionAnswers = QuestionAnswerQueries.getAll()
    return render_template("stuQuestion.html", questionAnswers=questionAnswers)


@studentQuestionsRoute.route('/studentQuestions/getByStudentId')
def getByStudentId():
    id = request.args.get("studentId")
    questionAnswers = QuestionAnswerQueries.getByStudentId(id)
    data = {"message": "ok", "code": "ok", "data": questionAnswers}
    return make_response(jsonify(data), 200)

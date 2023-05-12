import json

from flask import Blueprint, render_template, request, make_response, jsonify, session

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


@studentQuestionsRoute.route('/studentQuestions/addQuestionAnswer',methods=['post'])
def addQuestionAnswer():
    id = 166
    que_7 = request.form.getlist('que_7[]')
    otherQues = request.form
    que_8 = request.form.getlist('que_8[]')
    newDic = merge_dict_with_list(otherQues,que_7,"que_7[]")
    newDic = merge_dict_with_list(newDic,que_8,"que_8[]")

    questionAnswers = QuestionAnswerQueries.batchInsert(id,newDic)
    data = {"message": "ok", "code": "ok", "data": questionAnswers}
    return make_response(jsonify(data), 200)

def merge_dict_with_list(dictionary, key_list,name):
    new_dict = dictionary.copy()  # 创建一个旧字典的副本，以保留旧字典的内容
    key_list = [int(x) for x in key_list]

    for key in new_dict:
        if key ==name:
            new_dict.pop(key)
            new_dict[name[:-2]] = key_list

    return new_dict
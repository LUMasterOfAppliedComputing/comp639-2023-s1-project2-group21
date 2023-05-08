import functools

from flask import Blueprint, render_template, make_response, jsonify, request, session

from queries import StudentQueries

studentRoute = Blueprint('StudentRoute', __name__)


@studentRoute.route('/student/getAll')
def get_users():
    students = StudentQueries.getAll()
    return render_template("students.html", students=students)


@studentRoute.route('/student/getAllJson')
def get_students():
    students = StudentQueries.getAll()
    return make_response(jsonify(students), 200)

@studentRoute.route('/student/getStudentById')
def getStudentById():
    id = request.args.get("id")
    user = StudentQueries.getStudentById(id)
    if len(user) > 0: #if found a row return ok , if nothing found return error
        data = {"message": "ok", "code": "ok","data":user[0]['placement_status']}
    else:
        data = {"message": "user email doesn't exist", "code": "error"}
    return make_response(jsonify(data), 200)


def checkStudentProfileAndSurvey(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        userId = session['user_id']
        user = StudentQueries.getStudentById(userId)
        if len(user) > 0:
            if user[0]['placement_status'] != 0:
                return render_template("error.html",data='you have to complete our survey first!')
            else:
                print('start request')
                res = func(*args, **kwargs)
                return res
        else:
            return render_template("error.html", data='student doesn\'t exist!')

    return wrapper



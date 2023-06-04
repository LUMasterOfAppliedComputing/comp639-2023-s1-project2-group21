import functools

from flask import Blueprint, render_template, make_response, jsonify, request, session

from queries import StudentQueries, ProjectQueries,StudentWishlistQueries

studentRoute = Blueprint('StudentRoute', __name__)


@studentRoute.route('/student/getAll')
def get_users():
    pid = request.args.get("pid")
    return render_template("students.html",pid=pid)


@studentRoute.route('/student/getAllJson')
def get_students():
    pid = request.args.get("pid")
    if pid:
        students = StudentQueries.getAllRanked(pid)
    else:
        students = StudentQueries.getAll()
    return make_response(jsonify(students), 200)

@studentRoute.route('/student/getAllRanked')
def get_students_ranked():
    pid = request.args.get("pid")
    students = StudentQueries.getAllRanked(pid)
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

@studentRoute.route('/student/project')
def studentproject():
    # id=session['user_id']
    viewwishlist=request.form.get('viewwishlist')
    # addPreferArray = request.form.get('addPreferArray')
    # if addPreferArray != None:
    #    print(addPreferArray)
    if viewwishlist != None:
        projects = StudentWishlistQueries.showwishlist(id)
    else:
        projects = ProjectQueries.getProjectAll(None,None,None)
    return render_template("student/project.html", projects=projects)

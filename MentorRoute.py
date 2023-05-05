from flask import Blueprint, render_template, request, session, jsonify, make_response

from queries import UsersQueries, MentorQueries, ProjectQueries
from utils import MD5Helper

mentorRoute = Blueprint('mentorRoute', __name__)


@mentorRoute.route('/mentor/getAll')
def getAll():
    mentors = MentorQueries.getAll()
    return render_template("mentors.html", mentors=mentors)

@mentorRoute.route('/mentor/getAllJson')
def getAllJson():
    mentors = MentorQueries.getAll()
    return make_response(jsonify(mentors), 200)
#
# @mentorRoute.route('/mentor/getAll')
# def getAll():
#     mentors = MentorQueries.getAll()
#     return render_template("mentors.html", mentors=mentors)
#
# @mentorRoute.route('/mentor/getAllJson')
# def getAllJson():
#     mentors = MentorQueries.getAll()
#     return make_response(redirect(url_for('/mentors.html'), jsonify(mentors),200))

@mentorRoute.route('/mentor/delete/<id>')
def delete(id):
    deleteId = UsersQueries.delete(id)
    return render_template("users.html")

@mentorRoute.route('/mentor/addOrUpdate')
def addOrUpdate():
    mentorId = request.form.get("mentorId")
    phone = request.form.get("phone")
    summary = request.form.get("summary")
    id = MentorQueries.insert(mentorId, phone, summary)
    if id >0:
        return render_template("mentors.html")
    #  MentorQueries.update(mentorId, phone, summary)

    return render_template("mentors.html",errorMsg="add mentors wrong")

@mentorRoute.route('/mentor/project')
def mentorproject():
    projects = ProjectQueries.getAll()
    return render_template("mentor/project.html", projects=projects)



from flask import Blueprint, render_template, request, session

from queries import UsersQueries, MentorQueries, ProjectQueries
from utils import MD5Helper

mentorRoute = Blueprint('mentorRoute', __name__)


@mentorRoute.route('/mentor/getAll')
def getAll():
    users = UsersQueries.getAll()
    return render_template("users.html", users=users)


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

@mentorRoute.route('/mentor/profile')
def mentorprofile():
    id = session['user_id']
    profile = MentorQueries.getMentorinfo(id)
    return render_template("mentor/mentorprofile.html", profile=profile)

@mentorRoute.route('/mentor/updateprofile')
def mentorupdateprofile():
    id = session['user_id']
    profile = MentorQueries.getMentorinfo(id)
    return render_template("mentor/mentorUpdateprofile.html", profile=profile)

@mentorRoute.route('/mentor/Update',methods=["POST"])
def Update():
    id = request.form.get("mentorid")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    # password = request.form.get("password")
    email = request.form.get("email")
    phone = request.form.get("phone")
    summary = request.form.get("summary")
    UsersQueries.updateprofile(id, first_name, last_name, email)
    MentorQueries.update(id, phone, summary)

    profile = MentorQueries.getMentorinfo(id)
    return render_template("mentor/mentorprofile.html", profile=profile)



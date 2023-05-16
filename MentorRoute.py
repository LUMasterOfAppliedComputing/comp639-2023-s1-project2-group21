from flask import Blueprint, render_template, request, session,redirect, jsonify, make_response


from queries import UsersQueries, MentorQueries, ProjectQueries, CompanyQueries
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
    role = session['role']
    if role == 1:
        mentor=MentorQueries.getMentorinfo(session['user_id'])
        projects = ProjectQueries.getProjectAll(None,mentor[0]['company_id'],session['user_id'])
    else:
        projects = ProjectQueries.getProjectAll(None,None,None)
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


@mentorRoute.route('/mentor/getProjectAllJson')
def getProjectAllJson():
    role = session['role']
    if role == 1:
        mentor = MentorQueries.getMentorinfo(session['user_id'])
        projects = ProjectQueries.getProjectAll(None, mentor[0]['company_id'],session['user_id'])
    else:
        projects = ProjectQueries.getProjectAll(None, None,None)
    return make_response(jsonify(projects), 200)



@mentorRoute.route('/companyprofile')
def companyprofile():
    userid = session['user_id']
    company = CompanyQueries.getcompany(userid)
    print(company)
    return render_template("mentor/companyprofile.html", company=company)


@mentorRoute.route('/updatecompanyprofile',methods=['POST'])
def updatecompanyprofile():
    companyid = request.form.get("companyid")
    company_name = request.form.get("company_name")
    region = request.form.get("region")
    city = request.form.get("city")
    street = request.form.get("street")
    website = request.form.get("website")
    updateid = MentorQueries.updatecompany(company_name, region,city,street,website,companyid)
    if updateid >0:
        return redirect("/companyprofile")

    return redirect("/companyprofile",errorMsg="add mentors wrong")

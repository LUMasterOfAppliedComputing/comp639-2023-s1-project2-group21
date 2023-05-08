from flask import Blueprint, render_template, request, session,redirect

from queries import UsersQueries, MentorQueries, ProjectQueries, CompanyQueries
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





@mentorRoute.route('/companyprofile')
def companyprofile():
    company = CompanyQueries.getAll()
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

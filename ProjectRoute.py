
import functools

from flask import Blueprint, render_template, request, session, make_response, jsonify

from queries import ProjectQueries


projectRoute = Blueprint('projectRoute', __name__)


@projectRoute.route('/project/getAll')
def get_users():
    projects = ProjectQueries.getAll()
    return render_template("project.html", projects=projects)



@projectRoute.route('/project/getProjectByIds')
def getProjectByIds():
    idarr = request.args.get("idArr")
    print(idarr)
    projects = ProjectQueries.getProjectAll(idarr)
    data ={"message":'ok','code':'ok','data':projects}
    return make_response(jsonify(data), 200)

@projectRoute.route('/project/getAlltypeJson')
def getAlltypeJson():
    mentors = ProjectQueries.getAlltype()
    return make_response(jsonify(mentors), 200)

@projectRoute.route('/Project/addOrUpdate', methods=["post"])
def addOrUpdateProject():
    project_title = request.form.get("project_title")
    userId = request.form.get("user_id")
    description = request.form.get("description")
    Number_of_student = request.form.get("Number_of_student")

    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    projecttype = request.form.get("projecttype")


    try:
        
            userid = session['user_id']
            result = ProjectQueries.insert(project_title, description, Number_of_student, projecttype, start_date, end_date, Number_of_student,userid)
            print(result)
            data = {'message': 'Profile has been updated successfully', 'code': 'ok'}
    except:
            data = {'message': 'Something wrong, please try again later', 'code': 'ERROR'}

    return make_response(jsonify(data), 200)
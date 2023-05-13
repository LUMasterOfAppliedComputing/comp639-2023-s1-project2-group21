from flask import Blueprint, render_template, request, make_response, jsonify

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


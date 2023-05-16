from flask import Blueprint, render_template, request, session, make_response, jsonify

from queries import StudentProjectQueries

studentProjectRoute = Blueprint('StudentProjectRoute', __name__)


@studentProjectRoute.route('/studentProject/getAll')
def getAll():
    stuProjects = StudentProjectQueries.getAll()
    return render_template("studentProject.html", stuProjects=stuProjects)


@studentProjectRoute.route('/studentProject/add')
def addPreferProject():
    pidList = request.args.getlist("pidList[]")
    updatePids = StudentProjectQueries.getAllByStudentIdAndProjectId(session['user_id'], pidList)
    values = [str(value) for d in updatePids for value in d.values()]
    if len(updatePids) >0:
        StudentProjectQueries.delete(session['user_id'],values)

    StudentProjectQueries.batchInsert(session['user_id'], pidList)



@studentProjectRoute.route('/studentProject/getPreferredProject')
def getPreferredProject():
    projects = StudentProjectQueries.preferredProject(session['user_id'])
    data = {"message": "ok", "code": "ok", "data": projects}
    return make_response(jsonify(data), 200)


def remove_elements(a, b):
    a[:] = [int(item) for item in a if int(item) not in b]
    return a;

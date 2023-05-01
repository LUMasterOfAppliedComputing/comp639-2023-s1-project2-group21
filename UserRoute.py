from flask import Blueprint, render_template, request, session

from queries import UsersQueries
from utils import MD5Helper

userRoute = Blueprint('userRoute', __name__)


@userRoute.route('/users/getAll')
def get_users():
    users = UsersQueries.getAll()
    return render_template("users.html", users=users)


@userRoute.route('/users/delete/<id>')
def deleteUser(id):
    deleteId = UsersQueries.delete(id)
    return render_template("users.html")



@userRoute.route('/users/addOrUpdate')
def addOrUpdateUser():
    firstname = request.form.get("firstname")
    userId = request.form.get("userId")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")
    role = request.form.get("role")
    encrypted = MD5Helper.md5_encrypt(password);
    if not userId:
        id = UsersQueries.insert(firstname, lastname, encrypted, email, role)
        if id >0:
            return render_template("users.html")
    else:
        UsersQueries.update(userId,firstname, lastname, encrypted, email, role)

    return render_template("users.html",errorMsg="add user wrong")


# user login, email and role need to be passed, to match the database stored data.
@userRoute.route("/users/login", methods=["post"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    userData = UsersQueries.getUserByEmail(email)  # check if the email and role is matched
    if len(userData) > 0:
        data = userData[0]
        checkResult = MD5Helper.check_match(data['password'], password)
        if not checkResult:
            return render_template("users.html", errorMsg="Login details incorrect. Please try again")
        session['user_id'] = data['user_id']  # if matched, put the user on session variable.
        session['name'] = data['first_name'] +" "+ data['last_name']
        role = data['role']
        session['role'] = role
        session['email'] = data['email']
        match role:  # render different page by role
            case 0:
                # staff
                return render_template('staff/staffbase.html')
            case 1:
                # Mentor
                return render_template('mentor/mentorbase.html')
            case 2:
                # Student
                return render_template('student/studentbase.html')


    else:  # if not matched, pop-up return error message
        return render_template("users.html", errorMsg="Login details incorrect. Please try again")

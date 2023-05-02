import os

from flask import Flask
from flask import render_template
from CompanyRoute import companyRoute
from UserRoute import userRoute
from InterviewRoute import interviewRoute
from StudentProjectRoute import studentProjectRoute
from ProjectRoute import projectRoute
from ProjectSkillRoute import projectSkillRoute
from ProjectTypeRoute import projectTypeRoute
from QuestionRoute import questionRoute
from StudentQuestionAnswerRoute import studentQuestionsRoute
from StudentRoute import studentRoute
from TechSkillRoute import techSkillRoute
from StudentSkillRoute import studentSkillRoute
from MentorRoute import mentorRoute
app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)
app.register_blueprint(companyRoute)
app.register_blueprint(userRoute)
app.register_blueprint(interviewRoute)
app.register_blueprint(studentRoute)
app.register_blueprint(mentorRoute)
app.register_blueprint(techSkillRoute)
app.register_blueprint(studentQuestionsRoute)
app.register_blueprint(questionRoute)
app.register_blueprint(projectTypeRoute)
app.register_blueprint(projectSkillRoute)
app.register_blueprint(projectRoute)
app.register_blueprint(studentProjectRoute)
app.register_blueprint(studentSkillRoute)



@app.route("/")  # home page
def home():
    return render_template("index.html")

@app.route("/register")  # home page
def register():
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("/about.html")

@app.route("/contact")
def contact():
    return render_template("/contact.html")

@app.route("/login")
def login():
    return render_template("/login.html")

@app.route("/project")
def project():
    return render_template("/project.html")

@app.route("/student")
def student():
    return render_template("student/studentbase.html")

@app.route("/mentor")
def mentor():
    return render_template("mentor/mentorbase.html")

@app.route("/staff")
def staff():
    return render_template("staff/staffbase.html")

if __name__ == '__main__':
    app.run(debug=True)

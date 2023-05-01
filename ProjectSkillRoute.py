from flask import Blueprint, render_template

from queries import ProjectSkillQueries

projectSkillRoute = Blueprint('ProjectSkillRoute', __name__)


@projectSkillRoute.route('/projectSkillRoute/getAll')
def get_users():
    projectSkills = ProjectSkillQueries.getAll()
    return render_template("projectSkill.html", projectSkills=projectSkills)

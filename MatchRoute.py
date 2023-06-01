import json

import pandas as pd
from flask import Blueprint, render_template

import db
from queries import MatchQueries

matchRoute = Blueprint('matchRoute', __name__)


@matchRoute.route('/match/getMatch')
def getAllMatchs():
    data_two_d_array = combine_lists2D()
    return render_template("mentors.html", mentors=data_two_d_array)


def combine_lists2D():
    cursor = db.DBConnect()
    cursor.execute("""SELECT
                        id,
                        concat(first_name," ",last_name) as name
                        FROM student stu 
                        LEFT JOIN user u ON u.user_id = stu.id
                        where stu.placement_status = 0
                        """)
    students = cursor.fetchall()

    cursor.execute("SELECT * FROM project")
    projects = cursor.fetchall()

    matrix = [[0 for _ in range(len(projects))] for _ in range(len(students))]

    student_id_to_index = {student[0]: i for i, student in enumerate(students)}
    project_id_to_index = {project[0]: i for i, project in enumerate(projects)}

    cursor.execute("""SELECT
                        sp.project_id,
                        sp.student_id,
                        sp.will
                    FROM
                        student_project sp
                        INNER JOIN  student stu ON sp.student_id = stu.id 
                        AND stu.placement_status = 0
                        """)
    student_projects = cursor.fetchall()

    for student_project in student_projects:
        project_id = student_project[0]
        student_id = student_project[1]
        will_value = student_project[2]
        student_index = student_id_to_index[student_id]
        project_index = project_id_to_index[project_id]
        matrix[student_index][project_index] = will_value

    cursor.execute("SELECT * FROM mentor_student")
    mentor_projects = cursor.fetchall()

    for mentor_project in mentor_projects:
        student_id = mentor_project[0]
        project_id = mentor_project[3]
        will_value = mentor_project[2]
        student_index = student_id_to_index[student_id]
        project_index = project_id_to_index[project_id]
        matrix[student_index][project_index] += will_value

    df = pd.DataFrame(matrix, index=[student[1] for student in students], columns=[project[1] for project in projects])
    print(df)
    json_data = df.to_json(orient='split')
    print(json_data)

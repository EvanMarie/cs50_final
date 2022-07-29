import os

from click import get_current_context

from homeschool import db, app
from flask import Flask, request, flash, redirect, render_template, request, url_for, render_template_string, session
from flask_security import auth_required, roles_required, hash_password
from flask_login import current_user
from datetime import datetime, date, time
from tempfile import mkdtemp
from homeschool.db_api import add_link, add_upcoming, app_state, assign_user_to_student, create_user_for_student, decrement_school_day, delete_assignment, delete_link, delete_student, delete_upcoming, edit_assignment, edit_student, get_all_students, get_assignment_by_id,\
    get_assignments, get_current_school_day, get_links, get_upcoming, get_user_by_email, \
    add_new_student, get_student, add_user, increment_school_day, new_assignment, search_assignments, search_students
from sqlalchemy.exc import NoResultFound, IntegrityError

from homeschool.models import Assignment, Link
logger = app.logger


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, message='Page not found.'), 404


@app.errorhandler(500)
def application_error(error):
    return render_template('error.html', error_code=500, message='Application error.'), 500


@app.route("/", methods=['POST', 'GET'])
@auth_required()
def home():
    if request.method == 'GET':

        current_day = get_current_school_day()
        
        student_id = request.args.get('student_id')
        logger.info(f'loading index page for student: {student_id}')
        if student_id:
            student = get_student(id=student_id)
        else:
            try:
                student = current_user.student.one()
            except NoResultFound:
                return redirect(url_for('teacher_portal'))

        logger.info('getting assigments')
        day_assignments = get_assignments(current_day, student.id)
        logger.info('got assignments')
        upcoming = get_upcoming(student.id, current_day)
        links = get_links(student.id)
    return render_template("index.html", day_number=current_day,
                           day_assignments=day_assignments,
                           upcoming=upcoming,
                           student_id=student_id,
                           links=links)


@app.route('/remove_upcoming', methods=["GET"])
@roles_required('teacher')
def remove_upcoming():
    upcoming = request.args.get('upcoming_id')
    student_id = request.args.get('student_id')
    delete_upcoming(upcoming)
    return redirect(url_for('home', student_id=student_id))


@app.route('/remove_link', methods=["GET"])
@roles_required('teacher')
def remove_link():
    link = request.args.get('link_id')
    student_id = request.args.get('student_id')
    delete_link(link)
    return redirect(url_for('home', student_id=student_id))


@app.route("/notes", methods=['POST', 'GET'])
@auth_required()
def notes():
    if request.method == 'GET':

        student_id = request.args.get('student_id')
        logger.info(f'loading index page for student: {student_id}')
        if student_id:
            notes = get_notes(student_id)
        else:
            try:
                student = current_user.student.one()
                notes = get_notes(student.id)
            except NoResultFound:
                notes

        notes = get_notes(student.id)
    return render_template("notes.html", student_id=student_id,
                           day_number=day_number,
                           assignment=assignment,
                           author=author_id,
                           content=content)


@app.route("/new_note", methods=['POST', 'GET'])
@auth_required()
def new_note():
    if request.method == 'GET':
        return render_template("new_note.html")

    if request.method == 'POST':
        assignment = request.args.get("assignment")
        school_day = request.args.get('school_day')
        student = request.args.get('student_id')
        content = request.form.get('new_note_content')
        add_note(student_id=student.id,
                 school_day=school_day,
                 assignment=assignment_id,
                 content=content)
        return redirect(url_for('notes', student_id=student_id))


@app.route("/search_notes", methods=['POST', 'GET'])
@auth_required()
def search_notes():
    if request.method == 'GET':
        return render_template("search_notes.html")


@app.route("/search_students", methods=['POST', 'GET'])
@auth_required()
def search_students_form():
    if request.method == 'GET':
        student_name = request.args.get('student_name')
        if student_name:
            student = search_students()
            return render_template("update_student.html")

    if request.method == "POST":
        student_name = request.form.get('search_student_name')
        return redirect(url_for('search_students', student_name=student_name))


@app.route("/teacher_portal", methods=['POST', 'GET'])
@roles_required('teacher')
def teacher_portal():
    logger.info(f'User ID: {current_user.id}')
    logger.info(
        f'User role names {[role.name for role in current_user.roles]}')
    if request.method == 'GET':
        increment = request.args.get('increment')
        if increment:
            increment_school_day()
            
        else:
            decrement = request.args.get('decrement')
            if decrement:
                decrement_school_day()
            
        return render_template('teacher_portal.html', 
                               students=get_all_students(), 
                               day_number=get_current_school_day())


    if request.method == 'POST':
        post_type = request.args.get('post_type')
        if post_type == 'upcoming':
            student_name = request.form.get('student_upcoming')
            schoolday = request.form.get('day_upcoming')
            upcoming_content = request.form.get("assignment_upcoming")
            student = search_students(student_name=student_name)
            add_upcoming(student.id, schoolday, upcoming_content)

        if post_type == 'link':
            student_name = request.form.get('student_link')
            student = search_students(student_name=student_name)
            link_url = request.form.get('link_url')
            link_description = request.form.get('link_description')
            add_link(student.id, link_url, link_description)

        logger.info('adding upcoming assignment')

        logger.info('upcoming assignment added')
        return redirect(url_for('teacher_portal', students=get_all_students()))


@app.route("/add_assignment", methods=['POST'])
@roles_required('teacher')
def add_assignment():
    if request.method == 'POST':
        day = request.form.get("add_assignment_day")
        student_name = request.form.get("add_assignment_student")
        subject = request.form.get("add_assignment_class")
        assignment = request.form.get("assignment")

        student = search_students(student_name)
        new_assignment(student_id=student.id,
                       school_day=day,
                       subject=subject,
                       content=assignment,
                       assigned_by_id=current_user.id)
        return redirect(url_for('teacher_portal'))


@app.route("/new_student", methods=['POST', 'GET'])
@roles_required('teacher')
def new_student():
    if request.method == 'POST':
        first_name = request.form.get('new_student_firstname')
        last_name = request.form.get('new_student_lastname')
        note = request.form.get('new_student_note')
        new_student_email = request.form.get('new_student_email')

        add_new_student(first_name, last_name, note)

        student = get_student(first_name, last_name)
        try:
            create_user_for_student(student, new_student_email)
        except IntegrityError:
            db.session.rollback()
            user = get_user_by_email(new_student_email)
            assign_user_to_student(student, user.id)
        # todo: send email with instructions

        return redirect(url_for('teacher_portal'))

    if request.method == 'GET':
        return render_template("new_student.html")


@app.route("/update_student", methods=['POST', 'GET'])
@auth_required()
def update_student():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        student = get_student(id = student_id)
        return render_template("update_student.html",
                                student = student)
        
    if request.method == 'POST':
        first_name = request.form.get('update_student_firstname')
        last_name = request.form.get('update_student_lastname')
        email = request.form.get('update_student_email')
        note = request.form.get('update_student_note')
        student_id = request.args.get('student_id')
        edit_student(student_id = student_id,
                     first_name = first_name,
                     last_name = last_name,
                     email = email,
                     note = note)
                     
    return redirect(url_for('home'))
    

@app.route("/remove_student", methods = ['GET'])
@roles_required('teacher')
def remove_student():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        delete_student(int(student_id))
        return redirect(url_for('home'))

@app.route("/update_note", methods=['POST', 'GET'])
@auth_required()
def update_note():
    if request.method == 'GET':
        assignment_id = request.args.get('assignment_id')
        assignment = Assignment.query.get(int(assignment_id))
        return render_template("update_note.html",
                               assignment=assignment)

    if request.method == 'POST':
        note = request.form.get('note_content')
        assignment_id = request.args.get('assignment_id')
        edit_assignment(new_note = note)
        return redirect(url_for('home'))
        
        

@app.route("/update_assignment", methods=['POST', 'GET'])
@roles_required('teacher')
def update_assignment():
    if request.method == 'GET':
        student_id = request.args.get('student')
        assignment_id = request.args.get('assignment')
        assignment = get_assignment_by_id(assignment_id)
        student = get_student(id=student_id)
        return render_template("update_assignment.html",
                               assignment=assignment,
                               student=student)
    if request.method == 'POST':
        student = request.form.get('update_assignment_student')
        day = request.form.get('update_assignment_day')
        subject = request.form.get('update_assignment_class')
        content = request.form.get('update_assignment')
        note = request.form.get('update_note')
        assignment_id = request.args.get('assignment_id')

        edit_assignment(assignment_id=assignment_id,
                        new_content=content,
                        new_subject=subject,
                        new_school_day=day,
                        new_note=note)
        return redirect(url_for('teacher_portal'))

@app.route("/remove_assignment", methods = ['GET'])
@roles_required('teacher')
def remove_assignment():
    assignment_id = request.args.get('assignment_id')
    delete_assignment(int(assignment_id))
    return redirect(url_for('home'))
                                    


@app.route("/lookup_assignments", methods=['POST', 'GET'])
@auth_required()
def lookup_assignments():
    if request.method == 'GET':
        return render_template("lookup_assignments.html",
                               assignment_query=())

    if request.method == 'POST':
        student = request.form.get('lookup_student')
        day = request.form.get('lookup_day')
        subject = request.form.get('lookup_class')
        keyword = request.form.get('lookup_keyword')

        assignment_query = search_assignments(
            student=student,
            day=day,
            subject=subject,
            keyword=keyword)

        return render_template('lookup_assignments.html',
                               assignment_query=assignment_query or ())


@app.route("/complete_assignment", methods = ['GET'])
@auth_required()
def complete_assignment():
    assignment_id = request.args.get('assignment_id')
    assignment = get_assignment_by_id(assignment_id)
    logger.info(f'assignment completed: {assignment.completed}')
    new_completed = not assignment.completed
    logger.info(f'not assignment completed: {new_completed}')
    
    edit_assignment(assignment_id, new_completed = new_completed )
    assignment = get_assignment_by_id(assignment_id)
    logger.info(f'new assignment completed: {assignment.completed}')
    
    return redirect(url_for('home'))  

@app.route("/view_assignment", methods = ['GET'])
@auth_required()
def view_assignment():
    assignment_id = request.args.get('assignment_id')
    assignment = get_assignment_by_id(assignment_id)
    return render_template('view_assignment.html', assignment = assignment)
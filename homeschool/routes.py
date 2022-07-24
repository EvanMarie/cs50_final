import os

from homeschool import db, app
from flask import Flask, request, flash, redirect, render_template, request, url_for, render_template_string
from flask_security import auth_required, hash_password
from datetime import datetime, date, time
from tempfile import mkdtemp
from homeschool.db_api import get_assignments, lookup_assignments

logger = app.logger

@app.route("/", methods = ['POST' , 'GET'])
@auth_required()
def home():
    if request.method == 'GET':
        day_number = 1
        logger.info('getting assigments')
        day_assignments = get_assignments(day_number, 1)
        logger.info('got assignments')
    return render_template("index.html", day_number = day_number,
                                         day_assignments = day_assignments)


@app.route("/notes", methods = ['POST' , 'GET'])
@auth_required()
def notes():
        if request.method == 'GET':
            return render_template("notes.html")


@app.route("/new_note", methods = ['POST' , 'GET'])
@auth_required()
def new_note():
        if request.method == 'GET':
            return render_template("new_note.html")

@app.route("/search_notes", methods = ['POST' , 'GET'])
@auth_required()
def search_notes():
        if request.method == 'GET':
            return render_template("search_notes.html")
        
@app.route("/messages", methods = ['POST' , 'GET'])
@auth_required()
def messages():
        if request.method == 'GET':
            return render_template("messages.html")

@app.route("/search_messages", methods = ['POST' , 'GET'])
@auth_required()
def search_messages():
        if request.method == 'GET':
            return render_template("search_messages.html")
        
@app.route("/search_students", methods = ['POST' , 'GET'])
@auth_required()
def search_students():
        if request.method == 'GET':
            return render_template("search_students.html")

@app.route("/new_message", methods = ['POST' , 'GET'])
@auth_required()
def new_message():
        if request.method == 'GET':
            return render_template("new_message.html")

@app.route("/teacher_portal", methods = ['POST' , 'GET'])
@auth_required()
def teacher_portal():
        if request.method == 'GET':
            return render_template("teacher_portal.html")

@app.route("/add_assignments", methods = ['POST' , 'GET'])
@auth_required()
def add_assignments():
        if request.method == 'GET':
            return render_template("add_assignments.html")
        
@app.route("/new_student", methods = ['POST' , 'GET'])
@auth_required()
def new_student():
        if request.method == 'GET':
            return render_template("new_student.html")
        
@app.route("/update_student", methods = ['POST' , 'GET'])
@auth_required()
def update_student():
        if request.method == 'GET':
            return render_template("update_student.html")
        
@app.route("/update_note", methods = ['POST' , 'GET'])
@auth_required()
def update_note():
        if request.method == 'GET':
            return render_template("update_note.html")
        
@app.route("/update_assignment", methods = ['POST' , 'GET'])
@auth_required()
def update_assignment():
        if request.method == 'GET':
            return render_template("update_assignment.html")

@app.route("/lookup_assignments", methods = ['POST' , 'GET'])
@auth_required()
def lookup_assignments():
        if request.method == 'GET':
            return render_template("lookup_assignments.html",
                                    assignment_query = None)
        
        if request.method == 'POST':
            student = request.form.get('lookup_student')
            day = request.form.get('lookup_day')
            subject = request.form.get('lookup_class')
            keyword = request.form.get('lookup_keyword') 
            
            assignment_query = lookup_assignments(
                               student = student,
                               day = day,
                               subject = subject,
                               keyword = keyword)
            return render_template('lookup_assignments.html',
                                    assignment_query = assignment_query)    

                    
                
                        
                    
                
                    
                    
from multiprocessing.sharedctypes import Value
from sys import get_coroutine_origin_tracking_depth
from termios import TCOFLUSH
from homeschool.models import Link, Upcoming, User, Student, SchoolDay, Assignment, Note, AppState
from homeschool import db, app, user_datastore
from datetime import datetime, date, time
from flask_security import hash_password
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import or_, and_, func

logger = app.logger
def app_state():
    appstate = AppState.query.get(1)
    if not appstate:
        db.session.add(AppState(current_day = 1))
        db.session.commit()
        return app_state()
    return appstate 
        
    

def set_current_school_day(day_number):
    
    try:
        _state = app_state()
        _state.current_day = day_number
    except:
        db.session.add(AppState(current_day = day_number))
        _state = app_state()
    
    db.session.commit()
    db.session.refresh(_state)
    logger.info(f'current day is now {_state.current_day}')
    logger.info(f'current day is now {get_current_school_day()}')

def get_current_school_day():
    
    return app_state().current_day

def increment_school_day():
    """Increment school day and set the date for the new day.
    """
    set_current_school_day(get_current_school_day() + 1)
    current_day_dbrec = SchoolDay.query.get(get_current_school_day())
    if current_day_dbrec:
        current_day_dbrec.calendar_date = date.today()
    else:
        db.session.add(SchoolDay(day_number = get_current_school_day(),
                                 calendar_date = date.today()))
    db.session.commit()
    
def decrement_school_day():
    """Oops, you pushed increment too soon?  You can go back now.
    """
    set_current_school_day(get_current_school_day() - 1)
            

####################### GEN: ROLES & USERS ##############################
    
def init_roles():
    user_datastore.create_role(name='teacher')
    user_datastore.create_role(name='student')
    teacher = User.query.get(app_state().teacher_id)
    user_datastore.add_role_to_user(teacher, 'teacher')
    db.session.commit()
    
    
def set_date(schoolday_id, date_assignment):
    schoolday = SchoolDay.query.filter_by(id=schoolday_id).one()
    schoolday.calendar_date = date_assignment
    db.session.commit()


def add_user(email, password, roles=[]):
    user_datastore.create_user(
        email=email, password=hash_password(password), roles=roles)
    db.session.commit()
    
    
def create_user_for_student(student, new_student_email):
    add_user(email=new_student_email, password=hash_password('changemenow'), roles=['student'])
            
    user = User.query.filter_by(email=new_student_email).one()
    student.user_id = user.id
    db.session.commit()


def assign_user_to_student(student: Student, user_id):
    Student.user_id = user_id
    
    db.session.commit()

def get_user_by_email(email):
    return User.query.filter_by(email = email).one()


def new_schoolday(day_number=None):
    if day_number is None:
        previous_day_number = Schoolday.query.order_by(
            Schoolday.day_number.desc()).one_or_none()
        previous_day_number = previous_day_number or 0
    day_number = day_number or previous_day_number + 1
    db.session.add(SchoolDay(day_number=day_number))
    db.session.commit()
    
def set_date(schoolday_id, date_assignment):
    schoolday = SchoolDay.query.filter_by(id=schoolday_id).one()
    schoolday.calendar_date = date_assignment
    db.session.commit()

  ########################## STUDENTS ###################################

def add_new_student(first_name, last_name, note, user_id=None):
    db.session.add(Student(first_name=first_name,
                   last_name=last_name, user_id=user_id, note=note))
    db.session.commit()
    
def get_student(first_name=None, last_name=None, id=None):
    
    if id:
        return Student.query.get(id)
    
    return Student.query.filter_by(first_name = first_name,
                                       last_name = last_name).one()

def search_students(student_name = None):
    query = Student.query
    if student_name:
        try:
            first_name, last_name = student_name.split(' ')
            query = query.filter(func.lower(Student.first_name) == first_name.lower())
            query = query.filter(func.lower(Student.last_name) == last_name.lower())
        except ValueError:
            query = query.filter(or_(func.lower(Student.first_name) == student_name.lower(),
                                     func.lower(Student.last_name) == student_name.lower()))

    return query.one_or_none()
        
def get_all_students():
    return Student.query


def delete_student(student_id):
    student = Student.query.filter_by(id=student_id).one()
    db.session.delete(student)
    db.session.commit()

def edit_student(student_id, first_name = None, last_name = None, email = None, note = None):
    student = Student.query.get(student_id)
    if first_name:
        student.first_name = first_name
    if last_name:
        student.last_name = last_name
    if email:
        student.user.email = email
    if note:
        student.note = note
    db.session.commit()

    ########################### ASSIGNMENTS ##################################

def new_assignment(school_day,
                   subject,
                   content,
                   assigned_by_id,
                   student_first_name = '',
                   student_last_name = '',
                   student_id = None,
                   note=None):
    
    if student_first_name:
        student = search_students(student_first_name + ' ' + student_last_name)
        student_id = student.id
    
    assignment = Assignment(school_day=school_day,
                            student=student_id,
                            subject=subject,
                            content=content,
                            assigned_by = assigned_by_id)
    db.session.add(assignment)
    db.session.commit()
    

def get_assignment_by_id(assignment_id):
    return Assignment.query.get(assignment_id)


def get_assignments(day_number, student_id):
    assignments = (Assignment.query.filter_by(school_day=day_number,
                                             student=student_id)
                   .where(Assignment.content != '')
                   .order_by(Assignment.completed))
    return assignments


def edit_assignment(assignment_id, new_content=None, new_school_day=None, new_subject=None, 
                    new_student=None, new_note=None, new_completed=None):
    assignment = Assignment.query.filter_by(id=assignment_id).one()
    if new_content:
        assignment.content = new_content
    if new_school_day:
        assignment.school_day = new_school_day
    if new_subject:
        assignment.subject = new_subject
    if new_student:
        assignment.student = new_student
    if new_note:
        assignment.note = new_note
    if new_completed is not None:
        assignment.completed = new_completed
    
    db.session.commit()



def delete_assignment(assignment_id):
    assignment = Assignment.query.filter_by(id=assignment_id).one()
    db.session.delete(assignment)
    db.session.commit()


def search_assignments(student, day, subject, keyword):
    query = db.session.query(Assignment, Student).join(Student)

    if student:
        try:
            first_name, last_name = student.split(' ')
            query = query.filter(func.lower(Student.first_name) == first_name.lower())
            query = query.filter(func.lower(Student.last_name) == last_name.lower())
        except ValueError:
            query = query.filter(or_(func.lower(Student.first_name) == student.lower(),
                                               func.lower(Student.last_name) == student.lower())) 

    if day:
        day = int(day)
        query = query.where(Assignment.school_day == day)

    if subject:
        query = query.where(Assignment.subject.like(f'%{subject}%'))

    if keyword:
        query = query.where(or_(Assignment.subject.like(f'%{keyword}%'),
                                Assignment.content.like(f'%{keyword}%'),
                                Assignment.note.like(f'%{keyword}%')))

    return query


    ######################## UPCOMING and LINKS #####################################

    
def add_upcoming(student, day, content):
    db.session.add(Upcoming(student = student,
                            day = day,
                            content = content))
    db.session.commit()

def get_upcoming(student, day):
    return Upcoming.query.filter_by(student = student).where(Upcoming.day >= day).order_by(Upcoming.day.asc())

def delete_upcoming(upcoming):
    try:
        db.session.delete(upcoming)
    except UnmappedInstanceError:
        db.session.delete(Upcoming.query.get(upcoming))
    db.session.commit()
    

def add_link(student, link, description):
    db.session.add(Link(student = student,
                            link = link,
                            description = description))
    db.session.commit()

def get_links(student):
    return Link.query.filter_by(student = student)

def delete_link(link):
    try:
        db.session.delete(link)
    except UnmappedInstanceError:
        db.session.delete(Link.query.get(link))
    db.session.commit()

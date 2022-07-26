from multiprocessing.sharedctypes import Value
from termios import TCOFLUSH
from homeschool.models import Link, Upcoming, User, Student, SchoolDay, Assignment, Note, Message
from homeschool import db, app, user_datastore
from datetime import datetime, date, time
from flask_security import hash_password
from sqlalchemy.orm.exc import UnmappedInstanceError
from sqlalchemy import or_, and_, func

def init_roles(teacher_email = None):
    user_datastore.create_role(name='teacher')
    user_datastore.create_role(name='student')
    if teacher_email:
        teacher = User.query.filter_by(email = teacher_email).one()
        user_datastore.add_role_to_user(teacher, 'teacher')
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
    

def add_new_student(first_name, last_name, user_id=None):
    db.session.add(Student(first_name=first_name,
                   last_name=last_name, user_id=user_id))
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


def new_assignment(student_id,
                   school_day,
                   subject,
                   content,
                   assigned_by_id,
                   note=None):
    
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
    assignments = Assignment.query.filter_by(school_day=day_number,
                                             student=student_id).where(Assignment.content != '')
    return assignments


def add_note(content, author_id, school_day=None, assignment=None, student=None):
    db.session.add(Note(author_id = author_id,
                        school_day=school_day,
                        assignment=assignment,
                        student=student,
                        content=content))
    db.session.commit()


def edit_note(note_id, new_content, new_school_day=None, new_assignment=None, new_student=None):
    note = Note.query.filter_by(id=note_id).one()
    if new_content:
        note.content = new_content
    if new_school_day:
        note.school_day = new_school_day
    if new_assignment:
        note.assignment = new_assignment
    if new_student:
        note.student = new_student
    db.session.commit()


def edit_assignment(assignment_id, new_content, new_school_day=None, new_subject=None, new_student=None):
    assignment = Assignment.query.filter_by(id=assignment_id).one()
    if new_content:
        assignment.content = new_content
    if new_school_day:
        assignment.school_day = new_school_day
    if new_subject:
        assignment.subject = new_subject
    if new_student:
        assignment.student = new_student
    db.session.commit()


def delete_assignment(assignment_id):
    assignment = Assignment.query.filter_by(id=assignment_id).one()
    db.session.delete(assignment)
    db.session.commit()


def set_date(schoolday_id, date_assignment):
    schoolday = SchoolDay.query.filter_by(id=schoolday_id).one()
    schoolday.calendar_date = date_assignment
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
                                Assignment.content.like(f'%{keyword}%')))

    return query

def search_notes(author_id, day, content, assignment, keyword, student, search_date):
    query = Note.query
 
    if assignment:
        query = query.join(Assignment).where(Assignment.id == assignment)

    if day:
        day = int(day)
        query = query.join(SchoolDay).where(SchoolDay.day_number == day)
 
    if author_id:
        query = query.where(Note.author_id == author_id)

    if search_date:
        query = query.where(Note.date == search_date)
    
    if student:
        first_name, last_name = student.split(' ')
        query = query.join(Student).where(Student.first_name.lower()
                            == first_name.lower())
        if last_name:
            query = query.join(Student).where(
                Assignment.last_name.lower() == last_name.lower())

    if keyword:
        query = query.where(or_(Note.content.like(f'%{keyword}%'),
                                Note.assignment.like(f'%{keyword}%')))
    return query


def delete_note(note_id):
    note = Note.query.filter_by(id=note_id).one()
    db.session.delete(note)
    db.session.commit()
    

def send_message(sender, receiver, message_date, subject, content):
    db.session.add(Message(sender = sender,
                           receiver = receiver, 
                           date = message_date,
                           subject = subject,
                           content = content))
    db.session.commit()
    
    
def search_messages(owner, 
                    receiver = None, 
                    sender = None, 
                    message_date = None, 
                    keyword = None):
     
    if sender:
        sender = int(sender)
        query = Message.query.join(User, onclause = 'user.id == sender').where(and_(User.id == int(owner), 
                                                    Message.sender == int(sender)))
         
    elif receiver:
        receiver = int(receiver)
        query = Message.query.join(User, onclause = 'user.id == receiver').where(and_(User.id == int(owner),
                                                    Message.receiver == int(receiver)))
      
    if message_date:
        query = query.where(Message.date == message_date)
        
    if keyword:
        query = query.where(Message.subject.like("%keyword%") |
                            Message.content.like("%keyword%"))
        
    return query
        
    

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
            query = query.where(Student.first_name == first_name)
        except ValueError:
            query = query.where(Student.first_name == student_name)
            last_name = None

        if last_name:
            query = query.where(
                Student.last_name == last_name)
    return query.one()
        
def get_all_students():
    return Student.query

    
def add_upcoming(student, day, content):
    db.session.add(Upcoming(student = student,
                            day = day,
                            content = content))
    db.session.commit()

def get_upcoming(student, day):
    return Upcoming.query.filter_by(student = student).where(Upcoming.day >= day)

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
    
    
def send_message(sender, receiver, subject, content):
    db.session.add(Message( sender = sender,
                            receiver = receiver,
                            subject = subject,
                            content = content))
    db.session.commit()

def get_messages_for_user(user_id):
    received_messages = search_messages(owner = user_id,
                                        receiver = user_id)
    sent_messages = search_messages(owner = user_id,
                                    sender = user_id)
    return received_messages, sent_messages

def delete_message(message):
    try:
        db.session.delete(message)
    except UnmappedInstanceError:
        db.session.delete(Message.query.get(message))
    db.session.commit()

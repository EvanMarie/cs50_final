from termios import TCOFLUSH
from homeschool.models import User, Student, SchoolDay, Assignment, Note, Message
from homeschool import db, app, user_datastore
from datetime import datetime, date, time
from flask_security import hash_password


def add_user(email, password, roles=[]):
    user_datastore.create_user(
        email=email, password=hash_password(password), roles=roles)
    db.session.commit()


def add_student(first_name, last_name, user_id=None):
    db.session.add(Student(first_name=first_name,
                   last_name=last_name, user_id=user_id))
    db.session.commit()


def assign_user_to_student(student: Student, user_id):
    Student.user_id = user_id
    db.session.commit()


def new_schoolday(day_number=None):
    if day_number is None:
        previous_day_number = Schoolday.query.order_by(
            Schoolday.day_number.desc()).one_or_none()
        previous_day_number = previous_day_number or 0
    day_number = day_number or previous_day_number + 1
    db.session.add(SchoolDay(day_number=day_number))
    db.session.commit()


def new_assignment(student_first_name,
                   student_last_name,
                   school_day,
                   subject,
                   content,
                   notes=None):
    student = Student.query.filter_by(first_name=student_first_name,
                                      last_name=student_last_name).one()
    assignment = Assignment(school_day=school_day,
                            student=student.id,
                            subject=subject,
                            content=content)
    db.session.add(assignment)
    db.session.commit()
    db.session.refresh(assignment)
    add_note(content=notes,
             assignment=assignment.id,
             student=student.id,
             school_day=school_day)


def get_assignments(day_number, student_id):
    assignments = Assignment.query.filter_by(school_day=day_number,
                                             student=student_id).where(Assignment.content != '')
    return assignments


def add_note(content, school_day=None, assignment=None, student=None):
    db.session.add(Note(school_day=school_day,
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


def lookup_assignments(student, day, subject, keyword):
    query = Assignment.query

    if student:
        first_name, last_name = student.split(' ')
        query = query.join(Student).where(Student.first_name.lower()
                            == first_name.lower())
        if last_name:
            query = query.join(Student).where(
                Student.last_name.lower() == last_name.lower())

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
    owner = User.get(int(owner))   
    if sender:
        sender = int(sender)
        query = owner.received_messages.where(Message.sender == sender) 
    elif receiver:
        receiver = int(receiver)
        query = owner.received_messages.where(Message.receiver == receiver)
    
    elif message_date:
        query = owner.received_messages.where(Message.date == message_date)
        
    elif keyword:
        query = owner.re

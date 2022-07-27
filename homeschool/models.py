from homeschool import db, app
from datetime import date, datetime, time
from flask_security.models import fsqla_v2 as fsqla


class Role(db.Model, fsqla.FsRoleMixin):
    pass


class User(db.Model, fsqla.FsUserMixin):
    student = db.relationship('Student', lazy = 'dynamic', backref='user')
    
    
class AppState(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), default= 1)
    current_day = db.Column(db.Integer, db.ForeignKey('school_day.day_number'), default=1)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), default = None)
    first_name = db.Column(db.String(32), index=True)
    last_name = db.Column(db.String(32), index=True)
    note = db.Column(db.String(2048), index = True)
    assignments = db.relationship('Assignment', lazy='dynamic', backref='assigned_to')


class SchoolDay(db.Model):
    day_number = db.Column(db.Integer, primary_key = True)
    calendar_date = db.Column(db.Date, default=None)


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    school_day = db.Column(db.Integer, db.ForeignKey("school_day.day_number"), default=None)
    student = db.Column(db.Integer, db.ForeignKey("student.id"))
    subject = db.Column(db.String(64), index = True)
    content = db.Column(db.String(256), index = True)
    completed = db.Column(db.Boolean, default = False)
    assigned_by = db.Column(db.Integer, db.ForeignKey("user.id"))
    note = db.Column(db.String(2048), default = '', index = True)


class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    school_day = db.Column(db.Integer, db.ForeignKey("school_day.day_number"), default = None)
    assignment = db.Column(db.Integer, db.ForeignKey("assignment.id"), default = None)
    student = db.Column(db.Integer, db.ForeignKey("student.id"), default = None)
    content = db.Column(db.String(1024))
    date = db.Column(db.Date, default = date.today)


class Upcoming(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    day = db.Column(db.Integer, db.ForeignKey("school_day.day_number"), default = None)
    student = db.Column(db.Integer, db.ForeignKey("student.id"), default = None)
    content = db.Column(db.String(128), default = None)

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    student = db.Column(db.Integer, db.ForeignKey("student.id"), default = None)
    link = db.Column(db.String(128), default = None)
    description = db.Column(db.String(256), default = None)


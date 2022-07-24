from homeschool import app, db
from homeschool.models import Role, User, Student, SchoolDay, Assignment, Note

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Student': Student,
        'Schoolday': SchoolDay,
        'Assignment': Assignment,
        'Note': Note
        }


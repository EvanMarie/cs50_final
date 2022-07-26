from homeschool import app, db
from homeschool.models import Role, Upcoming, User, Student, SchoolDay, Assignment, Note
from homeschool.utils import import_lesson_plans

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Student': Student,
        'Schoolday': SchoolDay,
        'Assignment': Assignment,
        'Note': Note,
        'Upcoming': Upcoming,
        'import_lesson_plans': import_lesson_plans
        }


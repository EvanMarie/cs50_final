from csv import DictReader
from homeschool.db_api import new_schoolday, new_assignment
from homeschool import db
from sqlalchemy.exc import IntegrityError


subject_mapping = {
    'lang' : 'Language',
    'chem' : 'Chemistry',
    'psych' : 'PsySocio',
    'comp' : 'Computer',
    'geom' : 'Geometry',
    'math' : '5th Gr Math',
    'german' : 'German'
}

postfix_mapping = {
    'class' : 'Classwork',
    'ww' : 'Wordly Wise',
    'spell' : 'Spelling',
    'seat' : 'Seatwork',
    'text' : 'Textbook',
    'sheet' : 'Worksheets',
    'vid' : 'Video',
    'summary' : 'Ch. Questions',
    'wkbk' : 'Workbook',
    'probs' : '1,001 Problems',
    'bfn' : 'Big Fat Notebook',
    'emma': ''
}

def import_lesson_plans(file_path):
    only_emma = 'math'
    only_michael = 'geom'
    with open(file_path) as lesson_plan_csv:
        reader = DictReader(lesson_plan_csv)
        for row in reader:
            day = int(row.pop('Day'))
            if day > 5:
                break
            try:
                new_schoolday(day)
            except IntegrityError:
                db.session.rollback()
            for subject in row.keys():
                try:
                    subject_, postfix = subject.split('_')
                    subject_text = "{} {}".format(subject_mapping[subject_], postfix_mapping[postfix])
                except ValueError:
                    subject_text = subject
                # Create an Emma assignment
                if not subject.startswith(only_michael):
                    new_assignment(student_first_name = 'Emma',
                                   student_last_name = 'Stefanuk',
                                   school_day = day,
                                   subject = subject_text,
                                   content = row[subject],
                                   assigned_by_id = 1)
                if not subject.startswith(only_emma):
                    new_assignment(student_first_name = 'Michael',
                                   student_last_name = 'Stefanuk',
                                   school_day = day,
                                   subject = subject_text,
                                   content = row[subject],
                                   assigned_by_id = 1)


def get_http_strings(content: str):
    """This will return a list of http strings in the given string,
    along with the number of characters that preceded that string
    """

    findhttp = lambda string_a: string_a[string_a.find('http'):]

    links = []
    string_with_links = findhttp(content)
    if len(string_with_links) > 4:
        start_index = len(content) - len(string_with_links)
        space_index = string_with_links.find(' ')
        if space_index > 10:
            links.append((string_with_links[:space_index], start_index))
            links += get_http_strings(string_with_links[space_index:])
        else:
            links.append((string_with_links, start_index))
    return links

def convert_links(content):
    links = get_http_strings(content)
    new_content = ''
    current_index = 0
    for link, start_index in links:
        new_content += content[current_index:start_index]
        new_content += f'<a href ="{link}" target="_blank">{link}</a><br>'
        current_index += start_index + len(link)

    if new_content == '':
        new_content = content

    return new_content






    # content[0:links[0][1]] + <a href=
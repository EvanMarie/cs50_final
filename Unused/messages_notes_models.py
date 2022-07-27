class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    sender = db.Column(db.Integer, db.ForeignKey("user.id"))
    receiver = db.Column(db.Integer, db.ForeignKey("user.id"))
    date = db.Column(db.Date, default = date.today)
    subject = db.Column(db.String(128), default = '')
    content = db.Column(db.String(4096), default = '')
    
    
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
        



@app.route("/new_message", methods = ['POST' , 'GET'])
@auth_required()
def new_message():
        if request.method == 'GET':
            return render_template("new_message.html")
        
        if request.method == 'POST':
            sender = current_user.id
            receiver_email = request.form.get('message_to')
            subject = request.form.get('message_subject')
            content = request.form.get('new_message')
            receiver = get_user_by_email(receiver_email)
            send_message(sender = sender,
                         receiver = receiver.id,
                         subject = subject,
                         content = content)
            return redirect(url_for('messages'))


@app.route("/search_messages", methods = ['POST' , 'GET'])
@auth_required()
def message_search():
        if request.method == 'GET':
            return render_template("search_messages.html")
        
        if request.method == "POST":
            sender = request.form.get('search_messages_sender')
            receiver = request.form.get('search_messages_receiver')
            message_date = request.form.get('search_messages_date')
            keyword = request.form.get('search_messages_keyword')
            messages = search_messages(owner = current_user.id,
                                       sender = sender,
                                       receiver = receiver,
                                       message_date = message_date,
                                       keyword = keyword)
            return render_template('search_messages.html', messages = messages)
      
      
      @app.route("/messages", methods = ['POST' , 'GET'])
@auth_required()
def messages():
        if request.method == 'GET':
            messages_type = request.args.get('messages_type') or 'received'
            received, sent = get_messages_for_user(current_user.id)
            if messages_type == 'received':
                messages = received
            else:
                messages = sent
            return render_template("messages.html", messages_type = messages_type, 
                                                    messages = messages)




    ########################### NOTES ##################################
    
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


def delete_note(note_id):
    note = Note.query.filter_by(id=note_id).one()
    db.session.delete(note)
    db.session.commit()
    
def get_notes_by_student(student_id):
    note = Note.query.filter_by(student=student_id).where(and_(Note.content != '', ).order_by(Note.school_day.desc).limit(20)
    return note

def get_notes_by_author(author_id):
    note = Note.query.filter_by(student=student_id).where(Note.content != '').order_by(Note.school_day.desc).limit(20)
    
  
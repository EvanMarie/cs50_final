# cs50_final

# App Name: Homeschool Today! A homeschool planning and daily tasks tool for adventurous teachers and their students.

#### Video Demo:  <http://www.YouTube.com>

#### TECHNOLOGIES USED: Python, flask, flask_security, SQLAlchemy, Jinja, HTML, CSS, and CSS Grid.

#### Description:
# -- BACKSTORY ------------------------
As a homeschooling and working mom, it seems like there are never enough hours in the day for the multitudes of tasks requiring attention and completion. And usually every one of them seems quite urgent. It also feels like there is always an unbelievable amount of pressure to make sure that my children are getting the guidance and help they need completing their homeschool work, which is admittedly at a very advanced level for a rising 5th grader and high schooler. On top of all that, mom now decides to set off on a transition from opera singer and voice teacher to software and web development?! Who on earth felt like that was a good idea? Don't you have enough to do already? Apparently not!

So this app was born out of necessity. It will give my children, my dear students, the structure they need to complete their work alongside me, while I work on mine toward a whole new career. It is something I have always wished I could find as a homeschool mom but never could. So I am overjoyed to have been able to create it myself. 

Homeschool Today! is a fully responsive site, each page and aspect designed to be fully functional and to look great on everything from small mobile device dimensions to full desktop.

# -- PURPOSE and FUNCTIONALITY -----------------------
The first aspect a user experiences when they visit Homeschool Today! is the smooth, user-friendly flask_security interface. It makes registering, logging in, changing passwords, and the various other security measures easy and worry-free.

When the user is logged in, their user-id is given a role of either student or teacher, which makes their homepage, their portal, either the student portal or the teacher portal. Students will only ever see the student portal, which is the index page of the app, as well as the page where they can view their assignments in more detail, including notes their teacher has made to each assignment. Homeschool Today! is streamlined, in that both students and teachers have their main portal from which they can do most of their work. The only navigation items necessary are "home", "password", and "logout". For the student, they will remain on their portal page, except for when they are viewing the details of an assignment. The teacher portal has a few extra parts for administrative purposes. 

Let's take a look!


# --THE STUDENT PORTAL-----------------------

The student portal has three main parts: the current school day's assignments, upcoming deadlines, and important links. The daily assignment table is a list of a student's daily school work, which can be checked off as each is completed. From the assignment list, students can open links associated with their assignments in a new tab and view all the details about each assignment they are to complete by clicking on the binoculars icon beside each. After completed, the student can click on the check box beside the assignment, which will move it to the bottom of the list and strike through it. This can also be undone, should the student mistakenly check it off. After the school day is finished and the student has completed all that day's assignments, the list can be populated with the next school day's assignments.

The upcoming table is where the teacher posts deadlines that are not just daily tasks, but ones that the student needs to prepare for and make note of, such as longer-term projects, papers and tests, stay aware as as deadlines approach. When a deadline has passed, the upcoming deadline automatically disappears from the list.

The "My Links" portion of the student portal is a list to which the teacher posts important external links for students such as important websites, video links, Google documents (my children keep a Google document notebook of notes for each class they take, for example), etc. Each link opens in a new tab, allowing the student to freely switch back and forth between Homeschool Today! and their work.


# --THE TEACHER PORTAL-----------------------

This is where things get truly exciting. But of course I think that! I am the teacher. 

The teacher portal contains 5 different applications, each of which can be accessed from the main page, or portal. First, there is the table of students, from which the teacher can click on a student's name and be taken to that particular student's homepage / portal. On a student's portal, the teacher can view the assignments, upcoming deadlines, and personalized links for each student. From the student portal, a teacher is able to remove upcoming deadlines and links. And they can remove assignments by clicking on the details of the assignment and deleting within that page. (Only users with the teacher role are able to delete.) There is also a link to update the student's information on the student table, which takes the teacher to each student's information page, where they can update their name, email, and a note file on each student. From this portion of the portal, a teacher can also add a new student into the database.

Below the student table is the add assignment form. From there, the teacher can add as many assignments as they wish, giving the student's name, the school day associated, the subject of the assignment, the content or information including links, and a note for each task. This allows the teacher to easily populate the students' lists for each school day, or entire CSV files of lesson plans can be imported as well.

On the top right of the teacher portal is where a teacher can search student assignments that are already in the database by student name, school day, subject, or keyword within the assignment and / or its corresponding note. The assignment search from the main portal page will take the teacher to a table of assignments matching their search, where they can view, update, or remove the assignments.

Below the assignment search is the Add Upcoming portion of the teacher portal. From here, the teacher can add upcoming deadlines that are longer-term than daily assignments, such as tests, papers, or projects by inputting the student's name, the school day that is the deadline for the task, and the information about the task itself. Each time a teacher submits a task to the Add Upcoming form, the deadline will appear on the appropriate student's list of upcoming tasks. Only users with teacher roles can go into a student's portal and remove the task from the student's list.

And finally, the Add Link portion of the teacher portal allows the teacher to add important links to each student's portal by providing the student name, the link, and a description of the link. The link will then appear on the student's list of "My Links" as the clickable description, which opens the link in new window when the student clicks. Like the upcoming deadline table, only a teacher can remove a link from a student's table.

# -- FILES and TEMPLATES -----------------------

* Models.py - defines the database tables. SQLAlchemy is implemented, and flask_security provides a user datastore that is integrated into the database. 
* db.api.py - the interface to the database. In order to protect access to the database, the web routes make no calls directly to the models but rather use the functions here.
* routes.py - the flask routes file that links to the makes db.api calls and produces the web pages.
* utils.py - tools that are mainly used for importing an existing lesson plan in CSV format.
* __init.py - the init file in the homeschool directory. This is where everything gets started, the flask app, as well as the database and the user datastore routes and models. 
* style.css - the style page for the entire web app aside from the security features, which used security_styles.css. The entire site is designed to be responsive at min-1200px, min-800px and min-400px. The teacher portal is a grid within grid network, thus taking up so very much space. The design is as thorough and precise as I could get it and still create a visibly attractive, exciting, and dynamic user experience.
* security_styles.css - This contains the simple styles for the security pages of the site, including the login, register, change password, verification, and other pages.
*  index.html - the main portal for students, including their daily tasks, upcoming deadlines, and links tables.
* teacher_portal.html - the main portal for teachers, including their table of students, Add Assignment form, Search Assignments form, Add Upcoming form, and Add Link form.
* lookup_assignments.html - the table that is populated based on a teacher's assignment search, from which they can view, edit, and remove assignments.
* new_student.html - the page a teacher goes to when they click on Add Student under their student table.
* update_assignment.html - the page a teacher goes to when they click on the update icon beside an assignment in the lookup assignments table, where they can edit an assignment.
* update_student.html - the page a teacher goes to when they click on the update icon beside a student on their student table, where they can update student information.
* view_assignments.html - the uneditable page students and teachers are taken to when they click on the binoculars icon on a student's daily assignments table or on the lookup assignments, where they can find the full details of each assignment.
* error.html - for when things go awry.
* login_user.html, register_user.html, change_password.html, and other flask_security pages - all customized and stylized versions of the flask_security feature of this app. 

# -- THE ART -----------------------
Homeschool Today! features art by my ten-year-old daughter, Emma. She designed and created Sundae, the Homeschool Today mascot, who appears on the login, register, password change, and other security pages. She also designed the Homeschool Today! logo. This site also features a well-loved and popular painting by Wassily Kandinsky in a subdued fashion as the backdrop of all of the app pages.



#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *
import os
import openai
import os
from flask import send_file
import pdfkit
from flask import Response, render_template_string

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
#db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''
#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')

@app.route('/plan')
def plan():
    subject = request.args.get('subject')
    grade = request.args.get('grade')
    duration = request.args.get('duration')
    title = request.args.get('title')
    objectives = request.args.get('objectives')
    teacher = "TDS Education Team"
    date = "14/06/2023"
    lesson_plan = create_lesson_plan(subject, grade, duration, title, objectives, teacher, date)
    return render_template('pages/plan.html', subject=subject, grade=grade, duration=duration, title=title, objectives=objectives, lesson_plan=lesson_plan)


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)

@app.route('/download_text')
def download_text():
    plan = request.args.get('plan', '')
    filename = 'lesson_plan.txt'
    content = plan

    # Create a Flask response with the file content and appropriate headers
    response = Response(content, mimetype='text/plain')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'

    return response

# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

def create_lesson_plan(subject, grade, duration, title, objectives, teacher, date):
    try:
        guide = "The lesson plan requires every item to be filled with either (short) text that should be clear and concise and (Med) which should give more details and explain it well. Lesson title (short): This refers to the name or title of the lesson that the teacher is planning to teach. Teacher name (short): This is the name of the teacher who will be teaching the lesson. Subject (short): This is the subject that the lesson is focused on. Grade (short): This refers to the grade level of the students that the lesson is intended for. Date (short): This is the date on which the lesson is scheduled to take place. Duration (short): This refers to how long the lesson is planned for in terms of actual teaching or learning time. In this competition we will stick to one hour only) Key vocabulary (short): This is a short list of essential words that the students will familiarize themselves with. Supporting material: Additional tools that can help the teachers convey the topic better. Learning outcome (short): Knowledge: This refers to what the teacher wants the students to learn. It includes a list of key areas of knowledge (e.g. main bones in the human body and how to keep them healthy for a lesson on human skeleton). Skills: Skills they want students to be proficient in: This includes topic-specific skills that are being developed and taken from the curriculum. For example, understanding that the bones of the human skeleton make up a system, muscles, ligaments, and blood circulation. Understanding: <DS: add the understanding section here> Differentiation (Med): This component encourages the teacher to think about how they will make the lesson different for students who may have different learning needs. This can include extra text, simplified text, video or diagrams, allowing one child to lead while another receives support, breaking the task into steps, or providing a framework with questions. This also should target fast learners differently than slower learners who may need more resources. Learning experiences (Med): This component is divided into sixsections that describe the different stages of the lesson: prepare, plan, investigate, apply, connect, and evaluate and reflect. It includes a few activities that engage the students with the topic and provide a plan of the activities that the students will do during the lesson. Prepare: This section of the lesson plan is focused on preparing the students for the topic that will be covered. Educators can use this time to introduce the topic, ask general questions to assess the students prior knowledge, and engage the students with activities that will spark their interest in the topic. For example, if the topic is the human skeleton, the educator might ask the students what they know about bones, and then have them draw a human skeleton and label the bones. Plan: In the planning section, educators will lay out the activities that they will do with the students during the lesson. This will give the students a clear understanding of what to expect, and help the educator to structure the lesson in a logical way. If its a longer lesson, the educator might break the activities down into sections to help students stay engaged and focused. Investigate: During this part of the lesson, the students will be actively engaged in the topic. This might involve watching a video, conducting an experiment, or participating in a group discussion. If the topic is the human skeleton, the educator might have the students watch a video that explains the different bones in the body, and ask them to take notes on each bone. Apply: Once the investigation is complete, the students will use the knowledge they have gained to create something. This might involve creating a poster, a presentation, or a written report. For example, if the topic is the human skeleton, the students might create a poster that shows all the different bones in the body and how they fit together. Connect: In this section, educators will help the students make connections between the topic they are studying and the world around them. This might involve discussing current events or exploring how the topic relates to different cultures or regions. For example, if the topic is the human skeleton, the students might discuss how  bone health and growth is affected by diet and nutrition in different parts of the world. Evaluate and reflect: Finally, students willreflect on what they have learned. This might include thinking about what they enjoyed, what new skills and knowledge they gained, and what they could have done better. Educator assessment: This component is focused on how the teacher will assess what the students have learned. This might involve quizzes, rubrics, or other forms of  summative end-of-lesson assessments. For example, if the topic is the human skeleton, the educator might ask the students to take a quiz on the different bones in the body, and then ask them to reflect on what they learned and how they could improve their understanding in the future. Educator reflection: This component encourages the teacher to reflect on the content of the lesson, whether it was at the right level, whether there were any issues, and whether the pacing was appropriate. It also encourages the teacher to reflect on whether there was enough differentiation for students with different learning needs."
        openai.api_key = "API_KEY"

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=2000,
            messages=[
                {"role": "system", "content": "You are a teacher who creates lesson plans."},
                {"role": "user", "content": f"Create a lesson plan for the topic: {title} with objectives: {objectives}, grade level: {grade}, subject: {subject}, teacher: {teacher}, duration: {duration} date: {date}, follow this guideline: {guide}, remove (short) and (Med)"}
            ],
        )

        return completion.choices[0].message.content
    except openai.error.AuthenticationError as e:
        print("OpenAI unknown authentication error")
        print(e.json_body)
        print(e.headers)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

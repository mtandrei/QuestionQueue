from flask import render_template, request, jsonify
from queue import app, db
from queue.models import Question
from twilio.rest import TwilioRestClient

TWILIO_NUMBER = "609-917-7253"
AUTH_TOKEN = "851847dd101f9f1e605ab3643492763d"
SID="AC64cff1b438f8d1947ab340172e9fb902"
MAX_QUESTION_LEN = 100
MAX_USER_LEN = 15
INSTRUCTIONS = "Text the number of the question that you would like to have answered to ".join(TWILIO_NUMBER)
client = TwilioRestClient(SID, AUTH_TOKEN)
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # Grab fields from form
        user = request.form['username']
        question = request.form['question']
        
        # If blank question or username, return error
        if user == "":
            return render_template('index.html', error="Error: You put in a blank username!")

        if question == "":
            return render_template('index.html', error="Error: You put in a blank question!")

        # Check length of question and username
        if len(user) > MAX_USER_LEN:
           return render_template('index.html',
                    error="Error: Username exceeds".join(str(MAX_USER_LEN)).join("  characters"))

        if len(question) > MAX_QUESTION_LEN:
            return render_template('index.html',
                    error="Error: Question exceeds".join(str(MAX_QUESTION_LEN)).join(" characters"))

        # Create and add database record of question
        question = Question(question=question, username=user,votes=1)
        db.session.add(question)
        db.session.commit()

        # Return successful POST request to homepage
        return render_template('index.html', message="Success! Your Question was submitted")

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'GET':
        question_list = Question.query.limit(15).all()
        return render_template('questions.html', question_list=question_list)

    if request.method == 'POST':
       #TODO Make it so that people can vote (integrate twilio api)
    
       q_id = request.values['BODY']
       print q_id

       if q_id == -1:
           return render_template('questions.html')

       q = Question.query.filter_by(q_id)
       q.votes+=1
       db.session.commit()


       return render_template('questions.html')

@app.route('/results', methods=['GET'])
def results():
    if(request.method == 'GET'):
        questions = Question.query.order_by(Question.votes).limit(10)
        return render_template('results.html', questions=questions)
    return render_template('results.html')



def parse_info(message):
    q_id = 0
    try:
        q_id = int(message)
    except ValueError: #invalid reply
        return -1
    return q_id

from flask import render_template, request, jsonify
from queue import app, db
from queue.models import Question
from twilio.rest import TwilioRestClient
from sqlalchemy import desc

TWILIO_NUMBER = "609-917-7253"
AUTH_TOKEN = "851847dd101f9f1e605ab3643492763d"
SID="AC64cff1b438f8d1947ab340172e9fb902"
MAX_QUESTION_LEN = 100
INSTRUCTIONS = "Text the question that you would like to have answered to " + TWILIO_NUMBER

client = TwilioRestClient(SID, AUTH_TOKEN)

@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html', instructions=INSTRUCTIONS)
@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if request.method == 'GET':
        question_list = Question.query.limit(15).all()
        return render_template('questions.html', question_list=question_list)

    if request.method == 'POST':
        q_id = -1
        #Try/Catch that handles if int or string
        try:
            q_id = int(client.messages.list()[0].body) #gets most recent
        except ValueError:
            question = client.messages.list()[0].body
            
            # If blank question, return error
            if question == "":
                return render_template('index.html', error="Error: You put in a blank question!")

            # Check length of question
            if len(question) > MAX_QUESTION_LEN:
                return render_template('index.html',
                        error="Error: Question exceeds".join(str(MAX_QUESTION_LEN)).join(" characters"))

            # Create and add database record of question
            question = Question(question=question, votes=1)
            db.session.add(question)
            db.session.commit()

            return render_template('questions.html')

        if q_id == -1:
            return render_template('questions.html')
        
        q = Question.query.filter_by(id=q_id).first()
        if q is not None:
            q.votes+=1
            db.session.commit()
        return render_template('questions.html')
        


@app.route('/results', methods=['GET'])
def results():
    if request.method == 'GET':
        questions = Question.query.order_by(desc(Question.votes)).limit(10).all()
        return render_template('results.html', questions=questions)
    return render_template('index.html', error="ERROR: Bad request!")

@app.route('/clear', methods=['POST'])
def clear():
    if request.method == 'POST':
        db.session.query(Question).delete()
        db.session.commit()
        return render_template('index.html', delete="Questions deleted succesfully!")
    return render_template('index.html', error="ERROR: Bad request!")

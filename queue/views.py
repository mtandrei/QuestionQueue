from flask import render_template, request, jsonify
from queue import app, db
from queue.models import Question 

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        # Grab fields from form
        user = request.form['username']
        question = request.form['question']
        
        # If blank message or username, return error
        if user == "":
            return render_template('index.html', error="Error: You put in a blank username!")

        if question == "":
            return render_template('index.html', error="Error: You put in a blank question!")

        # Check length of message and username
        if len(user) > 15:
           return render_template('index.html',
                    error="Error: Username exceeds 15 characters")

        if len(message) > 500:
            return render_template('index.html',
                    error="Error: Question exceeds 500 characters")

        # Create and add database record of message
        question = Question(question=question, username=user)
        db.session.add(question)
        db.session.commit()

        # Return successful POST request to homepage
        return render_template('index.html', message="Success! Your Question was submitted")

    # If bad request, render error page
    return render_template('error.html', error='ERROR: Bad request!')

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    if(request.method == 'GET'):
        #TODO Grab messages from db, return to front end
        return 
    if(request.method == 'POST'): 
        #TODO Make it so that people can vote (integrate twilio api)

from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
@app.route("/list")
def main():
    questions = 
    return render_template('list.html', questions=questions)

@app.route("/new_question" method = [GET, POST])
def new_question(): 
    return render_template('new_question.html')

@app.route("/question/<question_id>" method = [GET, POST])
def question(question_id): 

    return render_template('question.html')

@app.route("/question/<question_id>/edit" method = [GET, POST])
def edit_question(question_id): 

    return render_template('question.html')

@app.route("/question/<question_id/delete>" method = [GET, POST])
def delete_question(question_id): 

    return render_template('question.html')

@app.route("/question/<question_id>/new-answer" method = [GET, POST])
def add_answer(question_id): 

    return render_template('question.html')

@app.route("/answer/<answer_id/delete>" method = [GET, POST])
def delete_answer(question_id): 

    return render_template('list.html')

@app.route("/question/<question_id>/vote-up")
def vote_up(question_id): 

    return render_template('question.html')

@app.route("/question/<question_id>/vote-down")
def vote_down(question_id): 

    return render_template('question.html')






if __name__ == '__main__':
    app.run (debug=True)
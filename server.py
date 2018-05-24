from flask import Flask, render_template
import logic

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def main():
    questions = logic.get_all_data("q")
    answers = logic.get_all_data("a")
    return render_template('list.html', questions=questions, answers=answers)


@app.route("/new_question", methods=['GET', 'POST'])
def new_question():
    return render_template('new_question.html')


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def question(question_id):

    return render_template('question.html')


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):

    return render_template('question.html')


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):

    return render_template('question.html')


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):

    return render_template('question.html')


@app.route("/answer/<answer_id>/delete", methods=['GET', 'POST'])
def delete_answer(question_id):

    return render_template('list.html')


@app.route("/question/<question_id>/vote-up")
def vote_up(question_id):

    return render_template('question.html')


@app.route("/question/<question_id>/vote-down")
def vote_down(question_id):

    return render_template('question.html')


if __name__ == '__main__':
    app.run(debug=True)

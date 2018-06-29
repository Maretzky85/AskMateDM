from flask import Flask, render_template, request, redirect
import logic

app = Flask(__name__)


@app.route("/")
def main():
    questions = logic.get_all_data("q")[:5]
    return render_template('list.html', questions=questions)


@app.route("/list")
def show_all():
    questions = logic.get_all_data("q")
    return render_template('list.html', questions=questions)


@app.route("/new_question", methods=['GET'])
def new_question():
    return render_template('new_question.html')


@app.route("/search", methods=["GET", "POST"])
def search_questions():
    search_phrase = request.form.get('search_phrase')
    result = logic.get_all_ids_with_phrase(search_phrase)
    return render_template ('list.html', questions=result, search_phrase=search_phrase)


@app.route("/new_question", methods=['POST'])
def post_new_question():
    form = request.form
    if len(form["message"]) == 0 or len(form["title"]) == 0:
        return new_question()
    logic.post_new_question(form)
    return redirect("/")


@app.route("/question/<question_id>", methods=['GET', 'POST'])
def question(question_id):
    logic.count_views(question_id)
    questions = [logic.find_by_id("q", question_id)]
    answers = logic.get_all_data("a")
    return render_template('list.html', questions=questions, answers=answers, question_id=question_id)


@app.route("/question/<question_id>/edit", methods=['GET'])
def edit_question(question_id):
    question = logic.find_by_id("q", question_id)
    return render_template('new_question.html', title=question["title"], message=question["message"], id_=question_id)


@app.route("/question/<question_id>/edit", methods=['POST'])
def save_edited_question(question_id):
    form = request.form
    logic.update_by_id("q", question_id, form)
    return redirect("/")


@app.route("/question/<question_id>/delete", methods=['GET', 'POST'])
def delete_question(question_id):
    logic.delete_by_id("q", question_id)
    return redirect('/')


@app.route("/question/<question_id>/new-answer", methods=['GET'])
def add_answer(question_id, warning=""):
    id_number = question_id
    question = (logic.find_by_id("q", id_number)["title"]+"\n"+logic.find_by_id("q", id_number)["message"])
    return render_template('new_answer.html', question_id=id_number, question=question, warning=warning)


@app.route("/question/<question_id>/new-answer", methods=['POST'])
def save_answer(question_id):
    form = request.form
    if len(form["message"]) == 0:
        return add_answer(question_id, "Title and message must be at least 10 signs")
    logic.post_new_answer(question_id, form)
    return question(question_id)


@app.route("/answer/<answer_id>/delete", methods=['GET'])
def delete_answer(answer_id):
    question_id = logic.find_by_id("a", answer_id)["question_id"]
    logic.delete_by_id("a", answer_id)
    return question(question_id)


@app.route("/answer/<answer_id>/vote-up")
def answer_vote_up(answer_id):
    logic.manage_vote("a", answer_id, 1)
    question_id = logic.find_by_id("a", answer_id)["question_id"]
    return question(question_id)


@app.route("/answer/<answer_id>/vote-down")
def answer_vote_down(answer_id):
    logic.manage_vote("a", answer_id, -1)
    question_id = logic.find_by_id("a", answer_id)["question_id"]
    return question(question_id)


@app.route("/question/<question_id>/vote-up")
def vote_up(question_id):
    logic.manage_vote("q", question_id, 1)
    return question(question_id)


@app.route("/question/<question_id>/vote-down")
def vote_down(question_id):
    logic.manage_vote("q", question_id, -1)
    return question(question_id)

@app.route("/sorted/")
def sorted_condition():
    condition = request.args.get('condition')
    order = request.args.get('order')
    questions = logic.order_by(condition, order)
    return render_template('list.html', questions=questions)




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect
import logic, data_manager, datetime

app = Flask(__name__)


@app.route("/")
def main():
    questions = logic.get_all_data("q", 5)
    return render_template('list.html', questions=questions)


@app.route("/list")
def show_all():
    questions = logic.get_all_data("q")
    return render_template('list.html', questions=questions)


@app.route("/new_question", methods=['GET'])
def new_question():
    users = logic.get_users()
    return render_template('new_question.html', title="", message=[""], users = users)

@app.route("/new_question", methods=['POST'])
def post_new_question():
    form = request.form
    for key, element in form.items():
        print("key - {}, element - {}".format(key, element))
    if len(form["message"]) < 10 or len(form["title"]) < 5:
        return new_question()
    logic.post_new_question(form)
    return redirect("/")


@app.route("/question/<question_id>", methods=['GET'])
def question(question_id):
    logic.count_views(question_id)
    questions = [logic.find_by_id("q", question_id)]
    answers = logic.get_all_data("a")
    comments = logic.get_all_comments()
    return render_template('list.html', questions=questions, answers=answers, comments=comments, question_id=question_id)


@app.route("/question/<question_id>/edit", methods=['GET'])
def edit_question(question_id):
    question = [logic.find_by_id("q", question_id)]
    return render_template('new_question.html',question=question, id_=question_id)


@app.route("/question/<question_id>/edit", methods=['POST'])
def save_edited_question(question_id):
    form = request.form
    logic.update_by_id("q", question_id, form)
    return question(question_id)


@app.route("/question/<question_id>/delete", methods=['GET'])
def delete_question(question_id):
    logic.delete_by_id("q", question_id)
    return redirect('/')


@app.route("/question/<question_id>/new-answer", methods=['GET'])
def add_answer(question_id, warning=""):
    id_number = question_id
    question = [logic.find_by_id("q", id_number)]
    users = logic.get_users()
    return render_template('new_answer.html', question_id=id_number, question=question, warning=warning, users = users)


@app.route("/question/<question_id>/new-answer", methods=['POST'])
def save_answer(question_id):
    form = request.form
    if len(form["message"]) == 0:
        return add_answer(question_id, "Title and message must be at least 10 signs")
    logic.post_new_answer(question_id, form)
    return question(question_id)


@app.route("/question/<question_id>/vote-up")
def vote_up(question_id):
    logic.manage_vote("q", question_id, 1)
    return question(question_id)


@app.route("/question/<question_id>/vote-down")
def vote_down(question_id):
    logic.manage_vote("q", question_id, -1)
    return question(question_id)


@app.route("/answer/<answer_id>/delete", methods=['GET'])
def delete_answer(answer_id):
    question_id = logic.find_by_id("a", answer_id)["question_id"]
    logic.delete_by_id("a", answer_id)
    return question(question_id)


@app.route("/answer/<answer_id>/edit", methods=['GET'])
def edit_answer(answer_id):
    question = [logic.find_by_id("q",logic.find_by_id("a", answer_id)["question_id"])]
    answer = logic.find_by_id("a", answer_id)
    return render_template("new_answer.html", question = question, answer = answer, answer_id=answer_id)


@app.route("/answer/<answer_id>/edit", methods=['POST'])
def save_edited_answer(answer_id):
    question_id = logic.find_by_id("a", answer_id)["question_id"]
    form = request.form
    logic.update_by_id("a", answer_id, form)
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


@app.route("/search", methods=['POST'])
def search_questions():
    search_phrase = request.form.get('search_phrase')
    result = logic.get_all_ids_with_phrase(search_phrase)
    warning = None
    if not result:
        warning = "Nope, please try again."
    return render_template('list.html', questions=result, search_phrase=search_phrase, warning=warning)


@app.route("/sorted/")
def sorted_condition():
    condition = request.args.get('condition')
    order = request.args.get('order')
    questions = logic.order_by(condition, order)
    return render_template('list.html', questions = questions)


@app.route("/user/<user_id>")
def user_page(user_id):
    user_data = logic.get_user_by_id(user_id)
    questions = logic.get_questions_by_user_id(user_id)
    answers = logic.get_answers_by_user_id(user_id)
    print(answers)
    return render_template("user_page.html", users = user_data, questions = questions, answers = answers)


@app.route("/list_users")
def list_users():
    data = logic.get_users()
    return render_template('user_list.html', users = data)

@app.route("/register", methods=["GET"])
def register_page():
    return render_template('register_page.html')


@app.route("/registered", methods=['POST'])
def new_user():
    login = request.form
    name = login.get('nick')
    registration_alert = None
    date = str(datetime.datetime.now()) 
    if logic.check_if_login_exists(name) == True or len(name) == 0:
        registration_alert = "This nickname already exists. Choose another one"
        return render_template("register_page.html", registration_alert=registration_alert)   
    data_manager.add_user(name, date)
    return render_template("after_reg.html", name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
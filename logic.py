import data_manager
import datetime


def get_all_data(qa="q", limit=None):
    '''
        Args:
        qa - str - "q" or "a", q for question, a for answer
        "q" - get all questions from database
        "a" - get all answers from database
        returns list of dicts
    '''
    if qa == "q":
        data = data_manager.import_data_from_db("q", limit)
        data = message_splitter(data)
        data = gen_answer_count(data)
    if qa == "a":
        data = data_manager.import_data_from_db("a", limit)
        data = message_splitter(data)
    if qa == "c":
        data = data_manager.import_comments_from_db()
        data = message_splitter(data)
    return data


def get_all_comments():
    data = data_manager.import_comments_from_db()
    return data


def post_new_question(form):
    '''
    saves new question to database
    Args:
        form - dict
    '''
    header = ["view_number", "vote_number", "image"]
    new_post = {}
    for item in header:
        new_post[item] = 0
    for key, entry in form.items():
        new_post[key] = entry
    new_post["image"] = None
    new_post["submission_time"] = str(datetime.datetime.now())[:-7]
    new_post["message"] = new_post["message"].replace("\r", "")
    data_manager.export_data_to_db("q", new_post)


def post_new_answer(question_id, form):
    '''
    saves new answer to database
    Args:
        question_id - int - ID number for question answered
        form - dict
    '''
    new_post = {}
    for key, entry in form.items():
        new_post[key] = entry
    new_post["image"] = None
    new_post["vote_number"] = 0
    new_post["submission_time"] = str(datetime.datetime.now())[:-7]
    new_post["question_id"] = question_id
    data_manager.export_data_to_db("a", new_post)


def post_new_comment(question_id, form):
    '''
    saves new comment to file
    Args:
        form - list of dicts
    '''

    new_comment = {}
    for key, entry in form.items():
        new_comment[key] = entry
    new_comment['question_id'] = question_id
    new_comment['answer_id'] = None
    new_comment['submission_time'] = str(datetime.datetime.now())[:-7]
    new_comment['edited_count'] = None
    data_manager.export_data_to_db("c", new_comment)


def post_new_comment_to_answer(answer_id, form):
    '''
    saves new comment to file
    Args:
        form - list of dicts
    '''

    new_comment = {}
    for key, entry in form.items():
        new_comment[key] = entry
    new_comment['question_id'] = None
    new_comment['answer_id'] = answer_id
    new_comment['submission_time'] = str(datetime.datetime.now())[:-7]
    new_comment['edited_count'] = None
    data_manager.export_data_to_db("c", new_comment)


def delete_by_id(qa, id_):
    '''
    Deletes post by id
    Args:
        qa - str - "q" or "a" , q for question, a for answer
        id - str or int - id of element to delete
    '''
    if qa == "q":
        data_manager.delete_by_id("q", id_)
    if qa == "a":
        data_manager.delete_by_id("a", id_)
    if qa == "c":
        data_manager.delete_by_id("c", id_)


def update_by_id(qa, id_, data):
    '''
    Update entry identified by ID number by data
    Args:
        qa - str - "q" or "a", q for question, a for answer
        id_ - ID number for question or answer
        data - dict containing ["title"] and ["message"]
    '''
    if qa == "q":
        data_manager.update_by_id("q", id_, data)
    if qa == "a":
        data_manager.update_by_id("a", id_, data)
    if qa == "c":
        new_data = {}
        for key, val in data.items():
            new_data[key] = val
        new_data["submission_time"] = str(datetime.datetime.now())[:-7]
        if not find_by_id("c", id_)["edited_count"]:
            new_data["edited_count"] = 1
        else:
            new_data["edited_count"] = find_by_id("c", id_)["edited_count"] + 1
        data_manager.update_by_id("c", id_, new_data)


def find_by_id(qa, _id):
    '''
        Args:
        qa - str - "q" or "a", q for question, a for answer
        "q" - get all questions from database
        "a" - get all answers from database
        _id - int - id of question or answer
        returns dict
    '''
    if qa == "q":
        data = data_manager.import_data_from_db("q")
        data = message_splitter(data)
        for question in data:
            question["answer_number"] = number_of_answers(question["id"])
    if qa == "a":
        data = data_manager.import_data_from_db("a")
        data = message_splitter(data)
    if qa == "c":
        data = data_manager.import_data_from_db("c")
        data = message_splitter(data)
    for item in data:
        if item["id"] == int(_id):
            return item

def get_user_id_by_question_id(question_id):
    user_id = data_manager.find_author_by_question_id(question_id)

    return user_id[0]["user_id"]

def get_user_id_by_answer_id(answer_id):
    user_id = data_manager.find_author_by_answer_id(answer_id)
    return user_id[0]["user_id"]


def manage_vote(qa, id_, value):
    if qa == "a":
        user_id = get_user_id_by_answer_id(id_)
        data_manager.manage_reputation(user_id, reputation_calc(qa, value))
    if qa == "q":
        user_id = get_user_id_by_question_id(id_)
        data_manager.manage_reputation(user_id, reputation_calc(qa, value))
    data_manager.vote_edit(qa, id_, value)
    return None


def reputation_calc(qa, value):
    if value < 0:
        return -2
    if value > 0:
        if qa == "a":
            return 10
        if qa == "q":
            return 5

def number_of_answers(question_id):
    number = data_manager.count_answer(question_id)
    return number["count"]


def count_views(question_id):
    data_manager.count_views(question_id)
    return None


def get_all_ids_with_phrase(search_phrase):
    data = data_manager.search_by_input(search_phrase)
    data = message_splitter(data)
    data = gen_answer_count(data)
    return data


def order_by(condition, order):
    data = data_manager.import_data_from_db("q", "all", condition, order)
    data = gen_answer_count(data)
    data = message_splitter(data)
    return data


def message_splitter(data):
    for message in data:
        message["message"] = message["message"].replace('\r', "").split('\n')
    return data


def gen_answer_count(data):
    for question in data:
        question["answer_number"] = number_of_answers(question["id"])
    return data


def get_users():
    data = data_manager.get_users()
    return data


def check_if_login_exists(name):
    data = data_manager.get_users()
    for item in data:
        for key, value in item.items():
            if value == name:
                return True
    return False


def add_user(name):
    name = name
    date = str(datetime.datetime.now())
    data_manager.add_user(name, date)


def get_user_by_id(user_id):
    user_data = data_manager.get_user_by_id(user_id)
    return user_data


def get_questions_by_user_id(user_id):
    data = data_manager.get_question_by_user(user_id)
    data = gen_answer_count(data)
    data = message_splitter(data)
    return data


def get_answers_by_user_id(user_id):
    data = data_manager.get_answer_by_user(user_id)
    data = message_splitter(data)
    return data

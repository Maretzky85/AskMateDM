import data_manager
import datetime


def get_all_data(qa="q"):
    '''
        Args:
        qa - str - "q" or "a", q for question, a for answer
        "q" - get all questions from database
        "a" - get all answers from database
        returns list of dicts
    '''
    if qa == "q":
        data = data_manager.import_data_from_db("q")
        data = message_splitter(data)
        for question in data:
            question["answer_number"] = number_of_answers(question["id"])
    if qa == "a":
        data = data_manager.import_data_from_db("a")
        data = message_splitter(data)
    return data


def find_by_id(qa, _id):
    '''
        Args: 
        qa - str - "q" or "a", q for question, a for answer
        "q" - get all questions from database
        "a" - get all answers from database
        _id - int - id of question or answer
        returns list of dict (compatibility)
    '''
    if qa == "q":
        data = data_manager.import_data_from_db("q")
        data = message_splitter(data)
        for question in data:
            question["answer_number"] = number_of_answers(question["id"])
    if qa == "a":
        data = data_manager.import_data_from_db("a")
        data = message_splitter(data)
    for item in data:
        if item["id"] == int(_id):
            return [item]


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


def manage_vote(qa, id_, value):
    data_manager.vote_edit(qa, id_, value)
    return None


def number_of_answers(question_id):
    number = data_manager.count_answer(question_id)
    return number["count"]


def count_views(question_id):
    data_manager.count_views(question_id)
    return None


def get_all_ids_with_phrase(search_phrase):
    data = data_manager.search_by_input(search_phrase)
    data = message_splitter(data)
    for question in data:
        question["answer_number"] = number_of_answers(question["id"])
    return data


def order_by(condition, order):
    data = data_manager.import_data_from_db("q", condition, order)
    return data


def message_splitter(data):
    for message in data:
        message["message"] = message["message"].replace('\r',"").split('\n')
    return data
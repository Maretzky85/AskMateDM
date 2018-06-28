import data_manager
import datetime


def get_all_data(qa="q"):
    if qa == "q":
        data = data_manager.import_data_from_db("q")
        for question in data:
            question["answer_number"] = number_of_answers(question["id"])
    if qa == "a":
        data = data_manager.import_data_from_db("a")
    return data


def find_by_id(qa, _id):
    if qa == "q":
        data = data_manager.import_data_from_db("q")
    if qa == "a":
        data = data_manager.import_data_from_db("a")
    for item in data:
        if item["id"] == int(_id):
            return item


def make_new_id(filename):
    data = data_manager.import_data_from_file(filename)
    return int(data[-1]["id"]) + 1


def post_new_question(form):
    '''
    saves new question to file
    Args:
        form - list of dicts
    '''
    header = ["view_number", "vote_number", "image"]
    new_post = {}
    for item in header:
        new_post[item] = 0
    for key, entry in form.items():
        new_post[key] = entry
    new_post["image"] = None
    new_post["submission_time"] = str(datetime.datetime.now())[:-7]
    data_manager.export_data_to_db("q", new_post)


def post_new_answer(question_id, form):
    '''
    saves new answer to file
    Args:
        form - list of dicts
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
        qa - str q or a, q for question, a for answer
        id - str or int - id of element to delete
    '''
    if qa == "q":
        data_manager.delete_by_id("q", id_)
    if qa == "a":
        data_manager.delete_by_id("a", id_)


def update_by_id(qa, id_, data):
    if qa == "q":
        data_manager.update_by_id("q", id_, data)
    if qa == "a":
        data_manager.update_by_id("a", id_, data)


def get_results(search_phrase):
    result = data_manager.search_by_input(search_phrase)
    return result


def manage_vote(qa, id_, value):
        data_manager.vote_edit(qa, id_, value)


def number_of_answers(question_id):
    number = data_manager.count_answer(question_id)
    return number[0]["count"]

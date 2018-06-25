import data_manager
from time import time


def get_all_data(qa="q"):
    if qa == "q":
        data = data_manager.import_data_from_db("q")
    if qa == "a":
        data = data_manager.import_data_from_db("a")
    return data


def find_by_id(qa, _id):
    if qa == "q":
        data = data_manager.import_data_from_file("sample_data/question.csv")
    if qa == "a":
        data = data_manager.import_data_from_file("sample_data/answer.csv")
    for item in data:
        if item["id"] == _id:
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
    header = data_manager.import_header("sample_data/question.csv")
    new_post = {}
    for item in header:
        new_post[item] = 0
    for key, entry in form.items():
        new_post[key] = entry
    new_post[" submisson_time"] = time()
    new_post["id"] = make_new_id("sample_data/question.csv")
    questions = data_manager.import_data_from_file("sample_data/question.csv")
    questions.append(new_post)
    data_manager.export_data_to_file("sample_data/question.csv", questions)


def post_new_answer(question_id, form):
    '''
    saves new answer to file
    Args:
        form - list of dicts
    '''
    header = data_manager.import_header("sample_data/answer.csv")
    new_post = {}
    for item in header:
        new_post[item] = 0
    for key, entry in form.items():
        new_post[key] = entry
    new_post["submisson_time"] = time()
    new_post["id"] = make_new_id("sample_data/answer.csv")
    new_post["question_id"] = question_id
    answers = data_manager.import_data_from_file("sample_data/answer.csv")
    answers.append(new_post)
    data_manager.export_data_to_file("sample_data/answer.csv", answers)


def delete_by_id(qa, id):
    '''
    Deletes post by id
    Args:
        qa - str q or a, q for question, a for answer
        id - str or int - id of element to delete
    '''
    if qa == "q":
        data = data_manager.import_data_from_file("sample_data/question.csv")
    if qa == "a":
        data = data_manager.import_data_from_file("sample_data/answer.csv")
    id_index_number = None
    for counter, entry in enumerate(data):
        if str(entry['id']) == str(id):
            id_index_number = counter
    del data[id_index_number]
    if qa == "q":
        data_manager.export_data_to_file("sample_data/question.csv", data)
    if qa == "a":
        data_manager.export_data_to_file("sample_data/answer.csv", data)

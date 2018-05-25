import data_manager
from time import time


def get_all_data(qa="q"):
    if qa == "q":
        data = data_manager.import_data_from_file("sample_data/question.csv")
    if qa == "a":
        data = data_manager.import_data_from_file("sample_data/answer.csv")
    return data


def make_new_id(filename):
    data = data_manager.import_data_from_file(filename)
    return int(data[-1]["id"]) + 1


def post_new_question(form):
    # id, submisson_time, view_number, vote_number, title, message, image
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

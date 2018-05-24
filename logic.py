import data_manager


def get_all_data(qa="q"):
    if qa == "q":
        data = data_manager.import_data_from_file("sample_data/question.csv")
    if qa == "a":
        data = data_manager.import_data_from_file("sample_data/answer.csv")
    return data

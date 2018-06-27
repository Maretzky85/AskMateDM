import csv
import connection_handler


def import_data_from_file(filename):
    '''
    Opens file defined in filename
    Returns list of dicts
    '''
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                data.append(row)
        csvfile.close()
        return data
    except FileNotFoundError:
        print("File not found")
        return {"message": "File not found"}
    except OSError:
        print("OS Error")
        return {"message": "OS Error"}


@connection_handler.connection_handler
def import_data_from_db(cursor, qa):
    if qa == "q":
        cursor.execute("""
                        SELECT * from question
                        """)
        data = cursor.fetchall()
        return data
    if qa == "a":
        cursor.execute("""
                        SELECT * from answer
                        """)
        data = cursor.fetchall()
        return data


def import_header(filename):
    '''
    Opens file and import header for csv dictwriter
    '''
    try:
        with open(filename) as datafile:
            lines = []
            for data in datafile:
                lines.append(data)
        return lines[0].strip("\n").split(",")
    except FileNotFoundError:
        print("File not found")
        return {"message": "File not found"}
    except OSError:
        print("OS Error")
        return {"message": "OS Error"}


def export_data_to_file(filename, data):
    '''
    Opens file to write, and writes data as csv file
    Args:
    filename - patch and filename
    data - list of dicts
    '''
    fieldnames = import_header(filename)
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for line in data:
                writer.writerow(line)
    except FileNotFoundError:
        print("File not found")
        return {"message": "File not found"}
    except OSError:
        print("OS Error")
        return {"message": "OS Error"}


@connection_handler.connection_handler
def export_data_to_db(cursor, qa, data):

    if qa == "q":
        cursor.execute("""
                        INSERT into QUESTION (submission_time, view_number, vote_number, title,image, message)
                        VALUES (%(submission_time)s, %(view_number)s,%(vote_number)s,%(title)s,%(image)s, %(message)s)
                        """, {"submission_time": data["submission_time"],
                        "view_number": data["view_number"],
                        "vote_number": data["vote_number"],
                        "title": data["title"],
                        "image": data["image"],
                        "message": data["message"]})
    if qa == "a":
        cursor.execute("""
                        INSERT into ANSWER (submission_time, vote_number, question_id,image, message)
                        VALUES (%(submission_time)s, %(vote_number)s,%(question_id)s,%(image)s, %(message)s)
                        """, {"submission_time": data["submission_time"],
                        "vote_number": data["vote_number"],
                        "question_id": data["question_id"],
                        "image": data["image"],
                        "message": data["message"]})
        return None


@connection_handler.connection_handler
def delete_by_id(cursor, qa, id_):
    if qa == "q":
        cursor.execute("""
                        DELETE from COMMENT
                        WHERE question_id = %(id_)s;
                        DELETE from ANSWER
                        WHERE question_id = %(id_)s;
                        DELETE from QUESTION
                        WHERE id = %(id_)s
                        """, {"id_": id_})
    if qa == "a":
        cursor.execute("""
                        DELETE from COMMENT
                        WHERE answer_id = %(id_)s;
                        DELETE from ANSWER
                        WHERE id = %(id_)s
                        """, {"id_": id_})


@connection_handler.connection_handler
def update_by_id(cursor, qa, id_, data):
    if qa == "q":
        cursor.execute("""
                        UPDATE QUESTION
                        SET title = %(title)s, message = %(message)s
                        WHERE id = %(id_)s
                        """, {"title": data["title"], "message": data["message"], "id_": id_})
    if qa == "a":
        cursor.execute("""
                        UPDATE ANSWER
                        SET title = %(title)s, message = %(message)s
                        WHERE id = %(id_)s
                        """, {"title": data["title"], "message": data["message"], "id_": id_})


@connection_handler.connection_handler
def search_by_input(cursor, search_phrase ):
    cursor.execute("""SELECT DISTINCT submission_time,
                                    view_number,
                                    vote_number,
                                    title,
                                    image,
                                    message
                    FROM question
                    JOIN answer ON (question_id = question_id)
                    WHERE title, message = %(search_phrase)s
                    """, {"search_phrase":search_phrase})
                                 

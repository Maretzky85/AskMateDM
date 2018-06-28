import csv
import connection_handler


@connection_handler.connection_handler
def import_data_from_db(cursor, qa):
    if qa == "q":
        cursor.execute("""
                        SELECT * from question
                        ORDER BY submission_time desc
                        """)
        data = cursor.fetchall()
        return data
    if qa == "a":
        cursor.execute("""
                        SELECT * from answer
                        ORDER BY submission_time desc
                        """)
        data = cursor.fetchall()
        return data


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
def search_by_input(cursor, search_phrase):
    print ("hura!!!!", search_phrase)
    cursor.execute("""SELECT DISTINCT question.id, question.submission_time, question.view_number, question.vote_number, question.title, question.message, question.image
                     FROM question
                    JOIN answer ON(question.id = answer.question_id)
                    WHERE question.title LIKE "%{}%"
                    OR answer.message LIKE "%{}%" """.format(search_phrase,search_phrase))
    data = cursor.fetchall()
    return data

@connection_handler.connection_handler
def vote_edit(cursor, qa, id_, value):
    if qa == "q":
        cursor.execute("""
                        UPDATE question
                        SET vote_number = vote_number + %(value)s
                        WHERE id = %(id)s;
                        """, {"qa": qa, "value": value, "id": id_})
    if qa == "a":
        cursor.execute("""
                        UPDATE answer
                        SET vote_number = vote_number + %(value)s
                        WHERE id = %(id)s;
                        """, {"value": value, "id": id_})

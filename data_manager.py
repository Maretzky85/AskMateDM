import csv
import connection_handler
from psycopg2.extensions import AsIs


@connection_handler.connection_handler
def import_data_from_db(cursor, qa, limit="ALL", condition="submission_time", order="desc"):
    if qa == "q":
        cursor.execute("""
                        SELECT question.id,
                                question.submission_time,
                                question.view_number,
                                question.vote_number,
                                question.title,
                                question.message,
                                question.image,
                                tag.name AS tag,
                                users.user_name AS user_name,
                                users.id AS user_id
                        FROM question
                        LEFT JOIN question_tag ON id=question_id
                        LEFT JOIN tag ON question_tag.tag_id=tag.id
                        LEFT JOIN users ON question.user_id = users.id
                        ORDER BY question.%(condition)s %(order)s
                        LIMIT %(limit)s""",
                         {"condition": AsIs(condition), "order": AsIs(order), "limit": AsIs(limit)})
        data = cursor.fetchall()
        return data
    if qa == "a":
        cursor.execute("""
                        SELECT 
                        answer.id,
                        answer.submission_time,
                        answer.vote_number,
                        answer.question_id, 
                        answer.message,
                        answer.image,
                        answer.user_id,
                        answer.accepted,
                        users.user_name AS user_name,
                        users.id AS user_id
                        FROM answer
                        LEFT JOIN users ON answer.user_id = users.id
                        ORDER BY submission_time desc
                        """)
        data = cursor.fetchall()
        return data
    if qa == "c":
        cursor.execute("""
                    SELECT * from comment
                    ORDER BY submission_time desc
                    """)
        data = cursor.fetchall()
    return data   


@connection_handler.connection_handler
def import_comments_from_db(cursor):
    cursor.execute("""
                    SELECT * from comment
                    ORDER BY submission_time desc
                    """)
    data = cursor.fetchall()
    return data



@connection_handler.connection_handler
def export_data_to_db(cursor, qa, data):

    if qa == "q":
        cursor.execute("""
                        INSERT into QUESTION (submission_time, view_number, vote_number, title,image, message, user_id)
                        VALUES (%(submission_time)s,
                        %(view_number)s,
                        %(vote_number)s,
                        %(title)s,
                        %(image)s, 
                        %(message)s, 
                        %(user_id)s)
                        """, {"submission_time": data["submission_time"],
                        "view_number": data["view_number"],
                        "vote_number": data["vote_number"],
                        "title": data["title"],
                        "image": data["image"],
                        "message": data["message"],
                        "user_id": data["user_id"]})
    if qa == "a":
        cursor.execute("""
                        INSERT into ANSWER (submission_time, vote_number, question_id,image, message, user_id)
                        VALUES (%(submission_time)s, 
                        %(vote_number)s,
                        %(question_id)s,
                        %(image)s, 
                        %(message)s,
                        %(user_id)s)
                        """, {"submission_time": data["submission_time"],
                        "vote_number": data["vote_number"],
                        "question_id": data["question_id"],
                        "image": data["image"],
                        "message": data["message"],
                        "user_id": data["user_id"]})
        return None
    if qa == "c":
        cursor.execute("""
                        INSERT into COMMENT (submission_time, question_id, answer_id, message, edited_count)
                        VALUES (%(submission_time)s, %(question_id)s,%(answer_id)s, %(message)s, %(edited_count)s)
                        """, {"submission_time": data["submission_time"],
                        "question_id": data["question_id"],
                        "answer_id": data["answer_id"],
                        "message": data["message"],
                        "edited_count": data["edited_count"],
                        "user_id": data["user_id"]})
        return None


@connection_handler.connection_handler
def delete_by_id(cursor, qa, id_):
    if qa == "q":
        cursor.execute("""
                        DELETE from COMMENT
                        WHERE question_id = %(id_)s;
                        DELETE from ANSWER
                        WHERE question_id = %(id_)s;
                        DELETE from comment
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
                        SET message = %(message)s
                        WHERE id = %(id_)s
                        """, {"message": data["message"], "id_": id_})


@connection_handler.connection_handler
def search_by_input(cursor, search_phrase):
    cursor.execute("""SELECT DISTINCT question.id,
                                     question.submission_time,
                                     question.view_number,
                                     question.vote_number,
                                     question.title,
                                     question.message,
                                     question.image
                    FROM question
                    FULL OUTER JOIN answer ON(question.id = answer.question_id)
                    WHERE question.title LIKE '%{}%'
                    OR answer.message LIKE '%{}%' """.format(search_phrase, search_phrase))
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


@connection_handler.connection_handler
def count_answer(cursor, q_id):
    cursor.execute("""
                    SELECT COUNT (id) FROM answer
                    WHERE question_id= %(q_id)s
                    """, {"q_id": q_id})
    data = cursor.fetchone()
    return data


@connection_handler.connection_handler
def count_views(cursor, question_id):
    cursor.execute("""
                UPDATE question
                SET view_number = view_number +1
                WHERE id= %(q_id)s
                ;
                """, {"q_id": question_id})


@connection_handler.connection_handler
def get_users(cursor):
    cursor.execute("""
                    SELECT * FROM users
                        """)
    data = cursor.fetchall()
    return data
    

@connection_handler.connection_handler
def get_question_by_user(cursor, user_id):
    cursor.execute("""
                SELECT *
                FROM  question
                WHERE user_id = %(user_id)s;
                """,{"user_id": user_id})
    data = cursor.fetchall()
    return data

@connection_handler.connection_handler
def add_user(cursor, name, date):
    cursor.execute("""
                INSERT INTO users
                (user_name, registration_date, rank)
                VALUES (%(name)s, %(date)s, 0)
                ;
                """, 
                {"name": name, "date": date,})


@connection_handler.connection_handler
def get_answer_by_user(cursor, user_id):
    cursor.execute("""
                SELECT *
                FROM  answer
                WHERE user_id = %(user_id)s;
                """,{"user_id": user_id})
    data = cursor.fetchall()
    return data


@connection_handler.connection_handler
def get_user_by_id(cursor, user_id):
    cursor.execute("""
                    SELECT * FROM users
                    WHERE id = %(user_id)s
                        """, {"user_id": user_id})
    user_id = cursor.fetchall()
    return user_id

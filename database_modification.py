import connection_handler

@connection_handler.connection_handler
def add_table_users(cursor):
    cursor.execute("""
                    DROP TABLE IF EXISTS users CASCADE;
                    CREATE TABLE users (
                    id serial not null
                    constraint pk_user_id primary key,
                    user_name text,
                    registration_date date NOT NULL DEFAULT CURRENT_DATE,
                    rank integer
                    );
                    
                    INSERT INTO users (user_name, registration_date, rank)
                    VALUES ('Bartek', '2018-07-01', 10);
                
                    INSERT INTO users (user_name, registration_date, rank)
                    VALUES ('Daria', '2018-07-02', 10);
                
                    INSERT INTO users (user_name, registration_date, rank)
                    VALUES ('Sebastian', '2018-07-03', 10);
                
                    INSERT INTO users (user_name, registration_date, rank)
                    VALUES ('Marek', '2018-07-04', 10);
                    
                    INSERT INTO users (user_name, registration_date, rank)
                    VALUES ('Mietek', '2018-07-05', 10);
                    
                    INSERT INTO users (user_name, registration_date, rank)
                    VALUES ('Katarzyna', '2018-07-06', 10);
                    
                    """)


@connection_handler.connection_handler
def update_questions_table(cursor):
    cursor.execute(""" 
                    ALTER TABLE question 
                    ADD user_id INTEGER;
                    
                    ALTER TABLE question 
                    ADD CONSTRAINT fk_user_id
                    FOREIGN KEY (user_id)
                    REFERENCES users (id)
                    ON DELETE SET NULL;
                   """)


@connection_handler.connection_handler
def update_answer_table(cursor):
    cursor.execute(""" 
                    ALTER TABLE answer 
                    ADD user_id INTEGER;
                    
                    ALTER TABLE answer 
                    ADD CONSTRAINT fk_user_id
                    FOREIGN KEY (user_id)
                    REFERENCES users (id)
                    ON DELETE SET NULL;
                  """)


@connection_handler.connection_handler
def update_comment_table(cursor):
    cursor.execute(""" 
                    ALTER TABLE comment 
                    ADD user_id INTEGER;
                    
                    ALTER TABLE comment 
                    ADD CONSTRAINT fk_user_id
                    FOREIGN KEY (user_id)
                    REFERENCES users (id)
                    ON DELETE SET NULL;
                   """)



@connection_handler.connection_handler
def update_question_accepted_table(cursor):
    cursor.execute(""" 
                    ALTER TABLE answer 
                    ADD accepted BOOLEAN NOT NULL DEFAULT false;
                    
                   """)


add_table_users()
update_questions_table()
update_answer_table()
update_comment_table()
update_question_accepted_table()

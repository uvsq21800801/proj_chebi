import sqlite3
from sqlite3 import Error
from unittest import expectedFailure

# tutorial to create db
# https://www.sqlitetutorial.net/sqlite-python/creating-database/
# 
# tutorial to insert
# https://pynative.com/python-sqlite-insert-into-table/

# print all the entity table
def print_table(connection_obj, cursor_obj):
    with connection_obj:
        cursor_obj.execute("SELECT * FROM ENTITIES")
        print(cursor_obj.fetchall())

def create_connection(db_file):
    #####
    # 1 - create database and table
    #####
    # create a database connection to a SQLite database
    connection_obj = sqlite3.connect(db_file)
    
    # creation of a cursor object
    # (I assume its purpose is to iterate through the db)
    cursor_obj = connection_obj.cursor()
    
    #####
    # 2 - fill the table
    #####

    ##### the code underneath is here to test
    ##### After testing, the user should have the choice to
    ##### reinitialise the database or keep the precedent
    ##### (or with more simplicity it could be a IF EXIST)
    # Drop the ENTITIES table if already exists
    cursor_obj.execute("DROP TABLE IF EXISTS ENTITIES")
    
    # call the function that create the table to get an empty table
    # (IF EXIST not added yet for the purpose of testing)
    table = create_table()

    cursor_obj.execute(table)

    # first print
    print("first print")
    print_table(connection_obj, cursor_obj)

    insert_entity(cursor_obj)

    # second print
    print("second print")
    print_table(connection_obj, cursor_obj)

    insert_entity(cursor_obj)

    # third print
    print("third print")
    print_table(connection_obj, cursor_obj)

    #####
    # 3 - User request something that uses the db
    #####

    # todo



    # Close the connection
    connection_obj.close()

# to complete if needed
def create_table():
    # Creating table by writing its SQL code
    table = """ CREATE TABLE ENTITIES (
                id INT NOT NULL,
                name VARCHAR(255) NOT NULL,
                filepath VARCHAR(25) NOT NULL
            ); """
    ##### Afterwards, we can add more parameters and types
    ##### so we can then filter or search of the database

    return table
            
# todo
def insert_entity(cursor_obj): # it should then have the args directly in the params

    # the code below is an example
    insert_query = """INSERT INTO ENTITIES
                   (id, name, filepath) 
                   VALUES 
                   (51321,'nitrogen','file/path/to/nitrogen')"""

    cursor_obj.execute(insert_query)

    

# todo/ not sure if we should be doing it like that
def extract_all():
    print('extract all')

# idea
# 
# def extract_[type/by certain caracteristic]():
#   //code    

if __name__ == '__main__':
    create_connection(r"db_folder/pythonsqlite.db")

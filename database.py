import sqlite3
from sqlite3 import Error
from unittest import expectedFailure
import os

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

# constuction de la base de donnée la première fois 
# qu'on lance le programme
### DOIT ETRE LANCÉ APRÈS LE PARSING ###
def db_init():
    
    # récupération du chemin de l'utilisateur
    current_path = os.path.abspath("database.py")
    path_len = len(current_path)
    len_to_delete = len("database.py")
    db_path = current_path[:path_len-len_to_delete]

    # si la bdd n'existe pas la créer
    if not os.path.exists(os.path.join(db_path, 'index.db')):
        file = os.path.join(db_path, 'index.db')
        try:
            conn = sqlite3.connect(file)
            print("Base de Données index.db crée")
        except:
            print("echec de création de la Base de Données") 

    # chargement des des noms et ID de molécules dans la table
    # non filtrée
    load_id_and_name() 

    # chargement de tables par nombre d'atomes
    # TODO

    # chargement de la table de chaines
    # TODO

    # chargement de tables par type d'atomes présent
    # TODO

    #...

def load_id_and_name():
    sqliteConnection = sqlite3.connect('index.db')

    c = sqliteConnection.cursor()
    # creation de la table des entités
    c.execute("""CREATE TABLE IF NOT EXISTS entity (
                    e_id integer NOT NULL, 
                    name text,
                    PRIMARY KEY (e_id)
                )""")

    # insertion des valeurs
    dir = os.path.abspath("Molecules")
    for filename in os.listdir(dir):
        
        try: 
            f = os.path.join(dir, filename)
            text_file = open(f, "r")
            lines = text_file.read().split('\n')
            
            if not lines[1][:len('Erreur')] == 'Erreur':
                
                #print(filename[:len(filename)-4])
                e_id = int(filename[:len(filename)-4])
                #print(filename)
                name = lines[7]
                
                c.execute("INSERT INTO entity VALUES(:e_id,:name)",{'e_id':e_id, 'name':name})
        
        except:
            print('erreur insert (exist peut-être déjà)'+str(filename))
            # apparemment ya un fichier appelé ErreurMolecule lol what?

    sqliteConnection.commit()
    sqliteConnection.close()

# attrappe le filepath et le nom de l'entité
def get_entity_from_id(e_id):

    sqliteConnection = sqlite3.connect('index.db')

    c = sqliteConnection.cursor()
    
    c.execute("SELECT * FROM entity WHERE e_id=:e_id", {'e_id': e_id})

    id, name = c.fetchall()[0]

    filepath = os.path.abspath(str(id)+".txt")

    sqliteConnection.close()

    return filepath, name

# attrappe le filepath et l'id de l'entité
def get_entity_from_name(name):
    sqliteConnection = sqlite3.connect('index.db')

    c = sqliteConnection.cursor()
    
    c.execute("SELECT * FROM entity WHERE name=:name", {'name': name})

    id, name = c.fetchall()[0]

    filepath = os.path.abspath(str(id)+".txt")

    sqliteConnection.close()

    return filepath, name



def load_taille():

    print('todo')


def load_chaines():

    print('todo')

def load_atom_present():

    print('todo')


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
            
# obselete
def insert_entity_old(cursor_obj): # it should then have the args directly in the params

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

    
    # intitialisation de la base de donnée
    db_init()


    # test select

    filepath_1400082 , name_1400082 = get_entity_from_id(140082)
    print("filepath_1400082 = "+str(filepath_1400082))
    print("name_1400082 = "+str(name_1400082))
    
    filepath_glucoalyssin, name_glucoalyssin = get_entity_from_name('glucoalyssin')
    print("filepath_glucoalyssin = "+str(filepath_glucoalyssin))
    print("name_glucoalyssin = "+str(name_glucoalyssin))

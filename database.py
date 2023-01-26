import sqlite3
from sqlite3 import Error
from unittest import expectedFailure
import os
import networkx as nx

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
    min, max = load_taille()

    # chargement de la table de chaines
    load_structures()

    # chargement de tables par type d'atomes présent
    # TODO

    # écriture d'un fichier config_bd
    # qui permet de sauvegarder les données liées aux tables
    txt = str(min)+'\n'+str(max)+'\n'
    #for l in split_txt:
    #    txt += l+'\n'

    # écriture dans le fichier
    if not os.path.isfile("config_bd.txt"):
        f = open("config_bd.txt", "x")
    else:
        f = open("config_bd.txt", "w")

    f.write(txt)

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
            
            if (not lines[1][:len('Erreur')] == 'Erreur') and (not lines[0] == '') and (not filename == 'ErreurMolecule'):
                
                e_id = int(filename[:len(filename)-4])
                name = lines[6]
                
                c.execute("INSERT INTO entity VALUES(:e_id,:name)",{'e_id':e_id, 'name':name})
        
        except:
            print('erreur insert, existe déjà si 2e exe '+str(filename))
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
    # recherche du min et max de taille de molécule
    min = -1
    max = -1
    dir = os.path.abspath("Molecules")
    for filename in os.listdir(dir):
        try: 
            f = os.path.join(dir, filename)
            text_file = open(f, "r")
            lines = text_file.read().split('\n')
            
            if (not lines[1][:len('Erreur')] == 'Erreur') and (not lines[0] == '') and (not filename == 'ErreurMolecule'):
                #lst_type = lines[5].split(' ')
                if min == -1:
                    min = int(lines[0])
                    max = int(lines[0])
                else:
                    if int(lines[0])>max:
                        max = int(lines[0])
                    elif int(lines[0])<min:
                        min = int(lines[0])
                
        except:
            print("error min_max loading")
    
    print("min: "+str(min))
    print("max: "+str(max))

    
    sqliteConnection = sqlite3.connect('index.db')
    c = sqliteConnection.cursor()
    # creation de la table des entités
    for i in range(min, max+1):
        table_name = 'taille_'+str(i)
        c.execute("""CREATE TABLE IF NOT EXISTS {tab} (e_id integer NOT NULL, name text, PRIMARY KEY (e_id))"""
        .format(tab=table_name))

    # insertion des valeurs dans les tables
    dir = os.path.abspath("Molecules")
    for filename in os.listdir(dir):
        try: 
            f = os.path.join(dir, filename)
            text_file = open(f, "r")
            lines = text_file.read().split('\n')
            if (not lines[1][:len('Erreur')] == 'Erreur') and (not lines[0] == '') and (not filename == 'ErreurMolecule'):
                #lst_type = lines[5].split(' ')
                table_name = 'taille_'+lines[0]
                e_id = int(filename[:len(filename)-4])
                c.execute("""INSERT INTO {tab} VALUES(:e_id, :name)""".format(tab=table_name),{'e_id':e_id,'name': lines[6]})
                
            
        except:
            print('erreur insert dans taille')

    
    sqliteConnection.commit()
    sqliteConnection.close()

    return min, max

def load_structures():
    sqliteConnection = sqlite3.connect('index.db')

    c = sqliteConnection.cursor()
    # creation de la table des chaines
    c.execute("""CREATE TABLE IF NOT EXISTS chaines (
                    e_id integer NOT NULL, 
                    PRIMARY KEY (e_id)
                )""")

    # creation de la table des structures contenant des cycles élémentaires
    c.execute("""CREATE TABLE IF NOT EXISTS contains_cycle_elem (
                    e_id integer NOT NULL, 
                    t_3 integer,
                    t_4 integer,
                    t_5 integer,
                    t_6 integer,
                    t_8 integer,
                    PRIMARY KEY (e_id)
                )""")

    # creation de la table des structures qui sont des arbres
    c.execute("""CREATE TABLE IF NOT EXISTS arbre (
                    e_id integer NOT NULL, 
                    PRIMARY KEY (e_id)
                )""")

    # création d'une table contenant les molécules non classifiées
    c.execute("""CREATE TABLE IF NOT EXISTS non_class (
                    e_id integer NOT NULL, 
                    t_min integer,
                    t_max integer,
                    nb_c integer,
                    PRIMARY KEY (e_id)
                )""")

    dir = os.path.abspath("Molecules")
    for filename in os.listdir(dir):
        try: 
            f = os.path.join(dir, filename)
            text_file = open(f, "r")
            lines = text_file.read().split('\n')
            if (not lines[1][:len('Erreur')] == 'Erreur') and (not lines[0] == '') and (not filename == 'ErreurMolecule'):
                
                e_id = int(filename[:len(filename)-4])
                # chaine
                if int(lines[0]) == int(lines[1])+1:
                    c.execute("""INSERT INTO {tab} VALUES(:e_id)""".format(tab="chaines"),{'e_id':e_id})
                
                else: # cycle
                    degres = lines[2].split(' ')
                    degres.remove('')
                    degres = [int(i) for i in degres]
                
                    voisins = lines[4].split(' ')
                    voisins.remove('')
                    voisins = [int(i) for i in voisins]

                    G = nx.Graph()
                    iteration = 0
                    for i in range(len(degres)):
                        for j in range(degres[i]):
                            G.add_edge(i, voisins[iteration+j])
                        iteration += degres[i]
                    cycle = nx.cycle_basis(G)
                    # arbre
                    if len(cycle)==0:
                        c.execute("""INSERT INTO {tab} VALUES(:e_id)""".format(tab="arbre"),{'e_id':e_id})
                
                    # inserer dans cycle
                    else:
                        cycle_elem = False
                        
                        #for i in cycle:
                        #    if len(i)>2 and len(i)<7:
                        #        cycle_elem = True
                        #if cycle_elem:
                        t_3=0 
                        t_4=0
                        t_5=0
                        t_6=0 
                        t_8 = 0
                        for i in cycle:
                            if len(cycle) == 3:
                                t_3 += 1
                            if len(cycle) == 4:
                                t_4 += 1
                            if len(cycle) == 5:
                                t_5 += 1
                            if len(cycle) == 6:
                                t_6 += 1
                            if len(cycle) == 8:
                                t_8 += 1
                        if t_3 == 0 and t_4== 0 and t_5== 0 and t_6== 0 and t_8== 0:
                            len_cycle = []
                            for i in cycle:
                                len_cycle.append(len(i))
                            
                            c.execute("""INSERT INTO {tab} VALUES(:e_id, :t_min, :t_max, :nb_c)""".format(tab="non_class"),{'e_id':e_id, 't_min':min(len_cycle), 't_max': max(len_cycle) , 'nb_c': len(cycle)})

                        else:
                            c.execute("""INSERT INTO {tab} VALUES(:e_id, :t_3, :t_4, :t_5, :t_6, :t_8)""".format(tab="contains_cycle_elem"),{'e_id':e_id, 't_3':t_3, 't_4':t_4, 't_5':t_5, 't_6':t_6, 't_8':t_8})

                
        except:
            print('erreur insert dans structure')
        #break


    sqliteConnection.commit()
    sqliteConnection.close()


def load_atom_present():

    print('todo')



if __name__ == '__main__':

    
    # intitialisation de la base de donnée
    db_init()


    # test select

    #filepath_1400082 , name_1400082 = get_entity_from_id(140082)
    #print("filepath_1400082 = "+str(filepath_1400082))
    #print("name_1400082 = "+str(name_1400082))
    
    #filepath_glucoalyssin, name_glucoalyssin = get_entity_from_name('glucoalyssin')
    #print("filepath_glucoalyssin = "+str(filepath_glucoalyssin))
    #print("name_glucoalyssin = "+str(name_glucoalyssin))

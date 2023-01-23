import os
import numpy

# prends chacun des fichiers de molécules et répertorie
# chacun des types d'atome puis le met dans un fichier, 
# associé à un identifiant
def register_atom_types():
    # set des types
    atom_types = []
    
    dir = os.path.abspath("Molecules")
    for filename in os.listdir(dir):
        
        try: 
            f = os.path.join(dir, filename)
            text_file = open(f, "r")
            lines = text_file.read().split('\n')
            
            if not lines[1][:len('Erreur')] == 'Erreur' and filename != 'ErreurMolecule':
                
                atomes = lines[5].split(' ')

                for a in atomes:
                    if a not in atom_types:
                        atom_types.append(str(a))
                        #print('nouveau type d\'atome '+ str(a)+' fichier: '+str(filename))
                
        except:
            print('erreur enregistrement des atomes')

    print(atom_types)

    # compte le nombre de chaque atome
    # initie count à 0 pour chaque type
    count =  [0] * len(atom_types)
    # for i in range(len(count)):
    #    count[i] = 0

    for filename in os.listdir(dir):
        
        try: 
            f = os.path.join(dir, filename)
            text_file = open(f, "r")
            lines = text_file.read().split('\n')
            
            if not lines[1][:len('Erreur')] == 'Erreur' and filename != 'ErreurMolecule':
                
                atomes = lines[5].split(' ')

                for a in atomes:
                    #if a not in atom_types:
                    #print(atom_types.index(str(a)))
                    count[atom_types.index(a)] += 1
                        #atom_types.add(str(a))
                        
        except:
            print('erreur comptage des atomes')

    print('count aaaaaaaaaaaaaa')
    print(count)

    # sorting, on sort par compte pour minimiser la 
    # chance d'avoir beaucoup de molécules avec
    # énormément de sommets voisins qui ne servent
    # qu'à indiquer la couleur
    atom_types = numpy.array(atom_types) 
    count = numpy.array(count)
    ids_sorted_by_count = count.argsort()
    ids_sorted_by_count = ids_sorted_by_count[::-1]
    sorted_atom_types = atom_types[ids_sorted_by_count]

    print('ids_sorted_by_count')
    print(ids_sorted_by_count)
    print('sorted_atom_types')
    print(sorted_atom_types)


    # maintenant on créer un fichier pour classifier 
    # les types d'atomes
    if not os.path.isfile("store_colours.txt"):
        f = open("store_colours.txt", "x")
    else:
        f = open("store_colours.txt", "w")
    i = 1
    txt = ''
    for a in sorted_atom_types:
        txt += str(a) + ' ' + str(i) + '\n'
        i+= 1

    f.write(txt)


    print('######################')

# prends chacun des fichiers de molécules et ajoute 
# pour chaque atome un nombre de voisin qui correspond à
# son type voir #######
def add_color_nodes():

    # ouvre le fichier de classification
    f = open("store_colours.txt", "r")
    type_et_num = f.read().split('\n')
    print(type_et_num)

    dir = os.path.abspath("Molecules")
    for filename in os.listdir(dir):
        
        try: 
            f = os.path.join(dir, filename)
            text_file = open(f, "r")
            lines = text_file.read().split('\n')
            
            if not lines[1][:len('Erreur')] == 'Erreur':
                
                new_file = lines[0]+lines[1]     
                #print(filename[:len(filename)-4])
                e_id = int(filename[:len(filename)-4])
                #print(filename)
                name = lines[6]


                #################
                # pas fini
                
                
        except:
            print('erreur add_color_nodes '+str(filename))
        

register_atom_types()
add_color_nodes()
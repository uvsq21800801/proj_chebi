import ctypes
import os

def interface():

    # programme temporaire simple
    # ce serait cool de le remplacer avec une barre
    # de recherche qui utilise la bdd
    # input
    id_1 = input("Entrez une PREMIERE id de molecule chebi: ")
    id_2 = input("Entrez une SECONDE id de molecule chebi: ")

    # output
    #print(id_1)
    #print(id_2)

    if not os.path.isfile("store_colours.txt"):
        f = open("appel_sparce_c.sh", "x")
    else:
        f = open("appel_sparce_c.sh", "w")
    txt =''
    if not os.path.isfile("sparse_run"):
        txt = 'gcc -o sparse_run Sparse_colors.c nauty2_8_6/nausparse.h nauty2_8_6/nauty.a\n'
    txt += './sparse_run '+str(id_1)+' '+str(id_2)
    txt += '\npython3 interface_u.py'
    txt += '\nbash appel_sparce_c.sh'
    f.write(txt)

    # ce serait aussi bien d'afficher les molécules séléctionnées


    print('interface avec appel de nauty TODO')

    # demande deux id/noms aux utilisateurs avec boucles de faux dans le cas
    # ou ça n'est pas trouvé dans la bdd

    # possiblement une interface plus tards

    # appelle nauty avec les deux ids et vérifie l'isomorphisme


    # il serait aussi bien que l'affichage des deux entités
    # appellées soient faites quelquepart


interface()
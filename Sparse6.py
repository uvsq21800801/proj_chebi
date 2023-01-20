import networkx as nx
from Bib import *



def parsing():
    i = j = 1 #Compteur de molécules
    infoerror = "Molécules non lues: \n"
    cpterror = 0
    numeroligne = 0 #compteur de lignes pour retrouver les noms de molécules et id chebi
    num=0

    creation_dossier_molSparse6()
    #telechargement()
    suppl = Chem.SDMolSupplier('ChEBI_lite_3star.sdf', sanitize = False) #Lecture fichier sdf et transformation en tableau de mol
    fichier = open('ChEBI_lite_3star.sdf', 'r') #Ouverture fichier sdf pour récupérer ids chebi et noms molécules
    lines=fichier.readlines()
    fichier.close()
    

    fichier = open('ChEBI_lite_3star.sdf', 'r') #Ouverture fichier sdf pour récupérer ids chebi et noms molécules
    


    for mol in suppl:

        res = []
        res = nom_id(fichier, numeroligne)
        idmolecule = res[0]
        nommolecule = res[1]
        numeroligne = int(res[2])

        S=num
        num = get_numline(lines,num)

        if mol is not None:
            j = 4 + mol.GetNumAtoms() + S
            L=get_matrix(lines,j,mol.GetNumBonds())

            lst = [(int(s[0]),int(s[1])) for s in L ]

            # Create a graph
            G = nx.Graph()
            G.add_edges_from(lst)

            repertoire = "MoleculesSparse6/" + idmolecule[6:] + ".txt"

            # Convert the graph to sparse6 format
            s6 = nx.write_sparse6(G, repertoire, header=False)


            i = i + 1 
            

    print("Il y a {} molécules dans le fichier".format(i-1))
    fichier.close()

parsing()

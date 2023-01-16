from ast import Raise
from lib2to3.pgen2.parse import ParseError
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import gzip
import sys
import os
import re
import numpy as np
from operator import attrgetter
import urllib.request
import gzip
import shutil
from Bib import *



#Fonction principale de parsing qui recueille les différentes informations importantes des molécules
#pour notre fichier personnalisé
def parsing():
    i = j = 1 #Compteur de molécules
    infoerror = "Molécules non lues: \n"
    cpterror = 0
    numeroligne = 0 #compteur de lignes pour retrouver les noms de molécules et id chebi
    
    creation_dossier_mol()
    creation_dossier_molSDF()
    
    #Parsing sur toutes les molécules 3 stars
    #telechargement()
    suppl = Chem.SDMolSupplier('ChEBI_complete_3star.sdf', sanitize = False) #Lecture fichier sdf et transformation en tableau de mol
    fichier = open('ChEBI_complete_3star.sdf', 'r') #Ouverture fichier sdf pour récupérer ids chebi et noms molécules
   
    for mol in suppl:

        #Lecture nom molecule et id chebi
        res = []
        res = nom_id(fichier, numeroligne)
        idmolecule = res[0]
        nommolecule = res[1]
        numeroligne = int(res[2])
        
        try:
            mol.UpdatePropertyCache(strict=False)
            #mol = Chem.RemoveAllHs(mol, sanitize=False)
        except:
            pass
        
        if mol is not None:
            #Passage en SMILES puis en mol
            #smiles = Chem.MolToSmiles(mol)
            #print(smiles)
            #m = Chem.MolFromSmiles(smiles)
        

            name = "Molecule_" + str(i) + ".txt"
            repertoire = "Molecules/" + idmolecule[6:] + ".txt"
            
            #Récupération nombre atomes et liaisons
            nbatom = mol.GetNumAtoms()
            nbbond = mol.GetNumBonds()
            infos = ""

            infosDebut = "1\n" + str(nbatom) + "\n" + str(nbbond) 

            #Récupération degrés atomes..
            infos += "\n" + degre_atomes(mol)

            #Calcul indice de début de chaque atome 
            infos += indice_e(mol)

            #Recherche des voisins de chaque atome 
            res = voisins_atomes(mol)
            infos += res[1] #e

            #Nombre de types d'atomes différents
            infos += types_atomes(mol)

            #Calcul formule
            formuledecomp = formule_molecule(mol)
            #Ajout de la formule de molécule
            infos += "\n" + formuledecomp + nommolecule 

            #Ce qu'on  ecrit dans le fichier
            #infosDebut contient un bit si molécule est lue ou non, nombre d'atomes de la molécule, de liaisons et taille de d, v et e
            #infos contient ce qui suit: d,v et e, le nombre de types d'atomes différents, formule chimique, nom molécule et coloration
            infosFinal = infosDebut + infos

            #Ecriture dans le fichier
            outf = open(repertoire, 'w+')
            outf.write(infosFinal)
            outf.close()
        else:
            #Molécule pas lue
            name = "Molecule_" + str(i) + ".txt"
            repertoire = "Molecules/" + idmolecule[6:] + ".txt"
            outf = open(repertoire, 'w+')
            st = "0 \nErreur de lecture molecule " + str(i) + "\n" + idmolecule + "\n" + nommolecule
            outf.write(st)
            outf.close()
            cpterror = cpterror + 1
            infoerror += "Molécule " + str(i) + " " + idmolecule + " ->" + nommolecule + "\n"
                
        i = i + 1 
    #Ecriture fichier molécules non lues
    outerror = open("Molecules/ErreurMolecule", 'w+')
    outerror.write(infoerror)
    outerror.close()
    print("Il y a {} molécules dans le fichier".format(i-1) + " dont " + str(cpterror) + " molécules non lues")
    fichier.close()


parsing()

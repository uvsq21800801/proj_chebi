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
from urllib.request import urlopen
import requests

#Téléchargement d'une molécule spécifique depuis chebi (format sdf)
def telechargement_mol(idmol):
    loc = "MoleculesSDF/"+idmol + ".sdf" 
    url = "https://www.ebi.ac.uk/chebi/saveStructure.do?sdf=true&chebiId=" + idmol + "&imageId=0" #le lien de téléchargement A COMPLETER
    req = urllib.request.urlretrieve(url, loc)

#Téléchargement, extraction du fichier des 50000 molécules 3 stars de Chebi (format sdf)
def telechargement(lib_path):

    # récupération du chemin de l'utilisateur
    current_path = os.path.abspath("parsing.py")
    path_len = len(current_path)
    len_to_delete = len("parsing.py")
    lib_path = current_path[:path_len-len_to_delete]
    
    url = 'https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz'

    # Le dataset ne sera téléchargé que si il n'a toujours pas
    # encore été téléchargé
    if not os.path.exists(os.path.join(lib_path, 'ChEBI_lite_3star.sdf.gz')):
        
        # récupération du .sdf.gz
        r = requests.get(url)
        path_file = os.path.join(lib_path, 'ChEBI_lite_3star.sdf.gz')  
        with open(path_file, 'wb') as f:
            f.write(r.content)

        # extraction du .gz
        with gzip.open(path_file,"rb") as f_in, open(os.path.join(lib_path,'ChEBI_lite_3star.sdf'),"wb") as f_out:
            shutil.copyfileobj(f_in, f_out)


'''
#Téléchargement, extraction du fichier des 50000 molécules 3 stars de Chebi (format sdf)
def telechargement():

    loc = "chebi.sdf.gz" #le chemin absolu vers ton fichier en local
    url = "ftp://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_complete_3star.sdf.gz" #le lien de téléchargement
    req = urlopen(url, loc)

    #on décompresse le fichier téléchargé avec ça
    new_file = "ChEBI_complete_3star.sdf" #le chemin absolu vers ton fichier décompressé en local
    with gzip.open(loc, 'rb') as file_in:
        with open(new_file, 'wb') as file_out:
            shutil.copyfileobj(file_in, file_out)
'''
#Créer un dossier pour contenir les molécules au format personnalisé s'il n'existe pas
def creation_dossier_mol():
    try:
       os.mkdir('Molecules')
    except OSError:
        if not os.path.isdir('Molecules'):
            Raise
#Créer un dossier pour contenir les molécules au format SDF s'il n'existe pas
def creation_dossier_molSDF():
    try:
        os.mkdir('MoleculesSDF')
    except OSError:
        if not os.path.isdir('MoleculesSDF'):
            Raise


def creation_dossier_molSparse6():
    try:
        os.mkdir('MoleculesSparse6')
    except OSError:
        if not os.path.isdir('MoleculesSparse6'):
            Raise


def get_numline(lines,num):
    mot=lines[num+1]
    while "$$$$" not in mot:
        num=num+1
        mot=lines[num]
    return num+1

#Lecture nom molecule et id chebi
def nom_id(fichier, numeroligne):
    ligne_prec = "> <ChEBI Name>" #la ligne qui précède le nom
    ligne_prec2 = "> <NAME>" #Peut etre ecrit de cette maniere
    ligne = fichier.readline(numeroligne)
    while ligne_prec not in ligne and ligne_prec2 not in ligne:
        if "> <ChEBI ID>" in ligne or "> <ID>" in ligne:
            idmolecule = fichier.readline(numeroligne + 1)
            idmolecule = idmolecule.strip('%s\n')
        ligne = fichier.readline(numeroligne)
        numeroligne = numeroligne + 1
    nommolecule = fichier.readline(numeroligne + 1) #On récupère le nom
    numeroligne += 1
    result = [idmolecule, nommolecule, str(numeroligne)]
    return result


def molecules(lines, j, nbatom):
    
    result=[]
    s=j
    while j<s+nbatom:
            mool=lines[j]
            molecules = mool.split(' ')
            molecules=[x for x in molecules if x]
            result.append(molecules[3])
            j = j + 1
    return result


def get_matrix(lines, j, nbatom):
    
    result=[]
    s=j
    while j<nbatom+s:
            mool=lines[j]
            molecules = mool.split(' ')
            molecules=[x for x in molecules if x]
            result.append([molecules[0],molecules[1],molecules[2]])
            j = j + 1
    return result



#Calcul formule de la molécule
def formule_molecule(molecule):
    formule = rdMolDescriptors.CalcMolFormula(molecule)
    formule2 = re.findall(r'([A-Z][a-z]?)(\d*)', formule)
            
    formuledecomp = ""
    for q in formule2:
        #if q[0] != "H": #suppression des hydrogènes
        if 1==1:
            formuledecomp += q[0] + "\n"
            if q[1] == "":
                formuledecomp += "1\n"
            else:
                formuledecomp += q[1] + "\n"
    return formuledecomp

#Calcul degré de chaque atome de la molécule (tableau d)
def degre_atomes(molecule):
    degres = ""
    atomes = molecule.GetAtoms()
    for a in atomes:
        #a.GetAtomWithIdx(0).GetSymbol()
        #print(a.getItemText())
        degres += str(a.GetDegree()) + " "
    return degres

#Calcul indice de début de chaque atome dans e 
def indice_e(molecule):
    atomes = molecule.GetAtoms()
    indices = "\n0 "
    cpt = 0
    ret = 0
    if molecule.GetNumAtoms() > 1: #on ne traite pas les voisins si l'atome est seul
        for a in atomes:
            if cpt == 0:
                indices += str(a.GetDegree()) + " "
                ret = a.GetDegree()
            elif cpt > 0 and cpt < molecule.GetNumAtoms()-1:
                indices += str(ret + a.GetDegree()) + " "
                ret += a.GetDegree()
            cpt += 1
                
    indices += "\n"
    return indices

#Recherche des voisins de chaque atome de la molécule 
def voisins_atomes(molecule):
    atomes = molecule.GetAtoms()
    cptE = 0 
    e = ""
    taille_e = ""
    
    for a in atomes:
        voisins = a.GetNeighbors()
        #print("atome : ",a.GetSymbol())
        #print("voisins :")

        for v in voisins:
            #print(v.GetSymbol())
            e += str(v.GetIdx()) + " "
            cptE += 1
    taille_e = str(cptE)
    result = [taille_e, e]
    return result
    
#Nombre de types d'atomes différents
def types_atomes(molecule):
    typesatomes = [] #Tableau des types d'atome deja trouvés
    typesatomesnonperiodique = ["R", "R1", "R2", "R3", "R4","R5","R6","R7","R8","R9","R10","R11","R12","R13","R14","R15","R16","R17","R18","R19","R20","R21","R22","R23","R24","R25","R26","R27","R28","R29","R30","R31","R32","*","R#","hv","X","A","D","ACP","Ps","Mu","Mu-","0","e","?"]
    atomes = molecule.GetAtoms()
    cpttype = 0 #Compteur de types d'atomes
    types = "" #Nombre de types differents
    for a in atomes:
        if a.GetSymbol() not in typesatomes and a.GetSymbol() not in typesatomesnonperiodique:
            typesatomes.append(a.GetSymbol())
            cpttype += 1
    types = "\n" + str(cpttype)
    return types

#Coloration des atomes (lab et ptn)
def coloration_atomes(molecule):            
    coloration = "" #lab
    colorationatome = "" #ptn      
    atomes = molecule.GetAtoms()
    listeatomes = []
    for g in atomes:
        listeatomes.append(g.GetSymbol())
    listecouleurs = np.unique(listeatomes)
            
    for h in listecouleurs:
        colorationliste = []
        for v in atomes:
            if h == v.GetSymbol():
                colorationatome += str(v.GetIdx()) + " "
                colorationliste.append("1")
        if len(atomes) > 1:
            del colorationliste[len(colorationliste)-1]
            colorationliste.append("0")
        for j in colorationliste:
            coloration += j + " "
    result = [colorationatome, coloration]
    return result

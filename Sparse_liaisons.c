/* This program demonstrates how an isomorphism is found between
   two graphs, using the Moebius graph as an example.
   This version uses sparse form with dynamic allocation.
*/


#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include "nausparse.h"    /* which includes nauty.h */
#include <ctype.h>


	
 void lire_sparse_graphe_fichier_molecule(int id_molecule, sparsegraph* sg, int** liste_atomes){
	
	printf("\nMolécule %d : \n", id_molecule);
	FILE * fp;
	//l'id de la molecule converti en string
	char* nom_fichier;
	nom_fichier = (char*) malloc(sizeof(char) * 100);
	strcpy(nom_fichier, "Parsing/Molecules/");
	sprintf(&nom_fichier[strlen("Parsing/Molecules/")], "%d", id_molecule);
    strcat(nom_fichier, ".txt");
    
    /*Ouvrir le fichier*/
   	fp = fopen (nom_fichier, "rb+");
   	
   	if (fp == NULL) {
        printf("Error opening file!\n");
        exit(1);
    }


	int nb_sommets;
	int nb_bonds;

	int degres[100];
	int V[100];
	int taille_V;
	int E[100];
	int taille_E;
    char buf[1000];
    char* token;
    int lineCount = 0;/* on sauvegarde le numero de la ligne */
    int i=0;
    int k;

    while (fgets(buf, 1000, fp) != NULL) {
        lineCount++;
        token = strtok(buf, " ");
		if(lineCount == 3){
			
			i = 0;
			//printf("Le vecteur d : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token est un nombre */
            		//sg->d[i] = atoi(token); // on remplit le vecteur d
            		degres[i] = atoi(token);
            		//printf("%d ", sg->d[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        	}
        	nb_sommets = i;// on sauvegarde le nombre de sommets
		}
		if(lineCount == 4){
			i = 0;
			//printf("\nLe vecteur v : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		//sg->v[i] = atoi(token); // on remplit le vecteur v
            		V[i] = atoi(token);
            		//printf("%d ", sg->v[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        		}
        	taille_V = i;	
		}
		if(lineCount == 5){
			i = 0;
			//printf("\nLe vecteur e : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		//sg->e[i] = atoi(token); // on remplit le vecteur v
            		E[i] = atoi(token);
            		//printf("%d ", sg->e[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        		}
        	taille_E = i;	
		}
		if(lineCount == 6){
			i = 0;
			int coded;
			while (token != NULL) {
				if(token[0] != " "){
						//printf("\nliste[%d] = %c",i,token[0]);
						coded = (int) token[0];
						liste_atomes[i] = coded;
						//printf("liste_atomes[%d] = %d\n", i, liste_atomes[i]);
						token = strtok(NULL, " ");	
						i++;	
				}
        	}
		}
		// la ligne qui contient le nouveau nombre d'aretes.
		if(lineCount == 8){
			while (token != NULL) {
		            nb_bonds = atoi(token)*2;
		            token = strtok(NULL, " ");
		            SG_ALLOC(*sg,nb_sommets,nb_bonds,"malloc");// on alloue la memoire dynamiquement au sparse graphe selon le nombre de sommets et d'aretes.
		            sg->nv = nb_sommets;
		            sg->nde = nb_bonds;
		            printf("\nNb sommets du graphe : %d\n", sg->nv);
		            printf("\nNb aretes du grphe : %d\n", sg->nde);
		            i = 0;
		            while(i<sg->nv){
		            	sg->d[i] = degres[i];
		            	//printf("d[%d] = %d |", i, sg->d[i]);
		            	i++;
					}
					i = 0;
					printf("\n\n");
		            while(i<taille_V){
		            	sg->v[i] = V[i];
		            	//printf("v[%d] = %d |", i, sg->v[i]);
		            	i++;
					}
					i=0;
					printf("\n\n");
					while(i<taille_E){
		            	sg->e[i] = E[i];
		            	//printf("e[%d] = %d |", i, sg->e[i]);
		            	i++;
					}
        	}
			
		}
    }
    
	fclose(fp);
	
}
int
main(int argc, char *argv[])
{

    DYNALLSTAT(int,lab1,lab1_sz);
    DYNALLSTAT(int,lab2,lab2_sz);
    DYNALLSTAT(int,ptn1,ptn1_sz);
    DYNALLSTAT(int,ptn2,ptn2_sz);
    DYNALLSTAT(int,orbits,orbits_sz);
    DYNALLSTAT(int,map,map_sz);
    static DEFAULTOPTIONS_SPARSEGRAPH(options);
    statsblk stats;
    
    int id_molecule1;
    int id_molecule2;
    
 /* Declare and initialize sparse graph structures */
    SG_DECL(cg1); SG_DECL(cg2);

    int n,m,i;

 /* Select option for canonical labelling */

    options.getcanon = TRUE;
    
    /* on specifie que les coloriages sont pris en charge */
    options.defaultptn = TRUE;

	n=100;
	m = SETWORDSNEEDED(n);
    nauty_check(WORDSIZE,m,n,NAUTYVERSIONID);

    DYNALLOC1(int,lab1,lab1_sz,n,"malloc");
    DYNALLOC1(int,lab2,lab2_sz,n,"malloc");
    DYNALLOC1(int,ptn1,ptn1_sz,n,"malloc");
    DYNALLOC1(int,ptn2,ptn2_sz,n,"malloc");
    DYNALLOC1(int,orbits,orbits_sz,n,"malloc");
    DYNALLOC1(int,map,map_sz,n,"malloc");

    id_molecule1 = atoi(argv[1]);
    id_molecule2 = atoi(argv[2]);
    
    sparsegraph sg1;
	SG_INIT(sg1);
	
	sparsegraph sg2;
	SG_INIT(sg2);

    
    lire_sparse_graphe_fichier_molecule(id_molecule1,&sg1,types_atomes_g1);
    lire_sparse_graphe_fichier_molecule(id_molecule2, &sg2,types_atomes_g2);
    
	
    /*on applique sparse nauty sur les deux graphes */
    sparsenauty(&sg1,lab1,ptn1,orbits,&options,&stats,&cg1);
    sparsenauty(&sg2,lab2,ptn2,orbits,&options,&stats,&cg2);
    
    if (aresame_sg(&cg1,&cg2))
        {
            printf("\nLes graphes sont isomoprhes ! \n");
            printf("Press ENTER key to Continue\n");  
			getchar();
            return 1;
    	}else{
            printf("\nLes graphes ne sont pas isomorphes.\n");
            printf("Press ENTER key to Continue\n");  
			getchar();
            return 0;
    	}
		
	    
    
}

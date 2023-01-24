/* This program demonstrates how an isomorphism is found between
   two graphs, using the Moebius graph as an example.
   This version uses sparse form with dynamic allocation.
*/

#include "nauty2_8_6/nausparse.h"    /* which includes nauty.h */
#include <ctype.h>


sparsegraph lire_sparse_graphe_fichier_molecule(int id_molecule){
	
	printf("\nMol�cule %d : \n", id_molecule);
	FILE * fp;
	//l'id de la molecule converti en string
	char* nom_fichier;
	nom_fichier = (char*) malloc(sizeof(char) * 100);
    sprintf(nom_fichier, "Molecules/%d", id_molecule);
	strcat(nom_fichier, ".txt");
    
    /*Ouvrir le fichier*/
   	fp = fopen (nom_fichier, "rb+");
   	
   	if (fp == NULL) {
        printf("Error opening file!\n");
        exit(1);
    }


	sparsegraph sg; /* La varibale sparse graphe que nous allons retourner */
	SG_INIT(sg);
	int nb_sommets;
	int nb_bonds;


    char buf[1000];
    char* token;
    int lineCount = 0;/* on sauvegarde le numero de la ligne */
    int i=0;
    int k;

    while (fgets(buf, 1000, fp) != NULL) {
        lineCount++;
        token = strtok(buf, " ");
        /*la ligne qui contient le nombre de sommets du graph */ 
        if(lineCount == 1){ 
             	while (token != NULL) {
		            nb_sommets = atoi(token);
		            token = strtok(NULL, " ");
        		}
		}
		if(lineCount == 2){
			
			while (token != NULL) {
		            nb_bonds = atoi(token)*2;
		            token = strtok(NULL, " ");
		            SG_ALLOC(sg,nb_sommets,nb_bonds,"malloc");// on alloue la memoire dynamiquement au sparse graphe selon le nombre de sommets.
		            sg.nv = nb_sommets;
		            sg.nde = nb_bonds;
		            printf("\nNbsommets = %d\n", sg.nv);
		            printf("\nNbaretes = %d\n", sg.nde);
        		}
		}
		if(lineCount == 3){
			i = 0;
			printf("Le vecteur d : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		sg.d[i] = atoi(token); // on remplit le vecteur d
            		printf("%d ", sg.d[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        	}
		}
		if(lineCount == 4){
			i = 0;
			printf("\nLe vecteur v : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		sg.v[i] = atoi(token); // on remplit le vecteur v
            		printf("%d ", sg.v[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        		}
		}
		if(lineCount == 5){
			i = 0;
			printf("\nLe vecteur e : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		sg.e[i] = atoi(token); // on remplit le vecteur v
            		printf("%d ", sg.e[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        		}
		}
    }
    
	
	fclose(fp);
       
	return sg; // On retourne le sparse graph
	
}


void out_sparseGraphe(char* nom_fichier, sparsegraph sg1){
	/* On affiche les graphes dans un format lisible par l'humain */
	
        FILE * fp;
   		fp = fopen (nom_fichier, "w+");
        put_sg(fp,&sg1,1,0);
        fclose(fp);
}

int
main(int argc, char *argv[])
{

    DYNALLSTAT(int,lab1,lab1_sz);
    DYNALLSTAT(int,lab2,lab2_sz);
    DYNALLSTAT(int,ptn,ptn_sz);
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
    
 
 /* Read the number of vertices and process it */

	n=100;
	m = SETWORDSNEEDED(n);
    nauty_check(WORDSIZE,m,n,NAUTYVERSIONID);

    DYNALLOC1(int,lab1,lab1_sz,n,"malloc");
    DYNALLOC1(int,lab2,lab2_sz,n,"malloc");
    DYNALLOC1(int,ptn,ptn_sz,n,"malloc");
    DYNALLOC1(int,orbits,orbits_sz,n,"malloc");
    DYNALLOC1(int,map,map_sz,n,"malloc");

    
    id_molecule1 = atoi(argv[1]);
    id_molecule2 = atoi(argv[2]);
    
    sparsegraph sg1 = lire_sparse_graphe_fichier_molecule(id_molecule1);
    sparsegraph sg2 = lire_sparse_graphe_fichier_molecule(id_molecule2);
    
    // afficher un sparse graphe avec une matrice d'adjacence
    /*out_sparseGraphe("adjacency_matrix1.txt", sg2);
    out_sparseGraphe("adjacency_matrix2.txt", sg1);*/
    
    /*on applique sparse nauty sur les deux graphes */
            
    sparsenauty(&sg1,lab1,ptn,orbits,&options,&stats,&cg1);
    sparsenauty(&sg2,lab2,ptn,orbits,&options,&stats,&cg2);
            
    
	
		
    if (aresame_sg(&cg1,&cg2))
        {
            printf("\nLes graphes sont isomoprhes ! \n");
            return 1;
    }else{
            printf("\nLes graphes ne sont pas isomorphes.\n");
            return 0;
    }
		
	    
    printf("Press ENTER key to Continue\n");  
	getchar();
}

/* This program demonstrates how an isomorphism is found between
   two graphs, using the Moebius graph as an example.
   This version uses sparse form with dynamic allocation.
*/

#include "nausparse.h"    /* which includes nauty.h */
#include <ctype.h>


// lis un fichier texte generér par gtools et le transforme en sparse graphe 
sparsegraph lire_sparse_graphe_fichier(char* nom_fichier) {
	FILE * fp;

   	fp = fopen (nom_fichier, "rb+");
    char buffer[1000];
    sparsegraph sg;
	while ( fscanf(fp, "%s", buffer) != EOF )
		{   
		   SG_INIT(sg);
		   int num_loops;
		   stringtosparsegraph(buffer, &sg, &num_loops);
		   //performCheck(&sg);
		   //SG_FREE(sg);
		}
	fclose(fp);
	return sg;
}


sparsegraph lire_sparse_graphe_fichier_molecule(int id_molecule){
	
	printf("\nMolécule %d : \n", id_molecule);
	FILE * fp;
	//l'id de la molecule converti en string
	char* nom_fichier;
	nom_fichier = (char*) malloc(sizeof(char) * 100);
    sprintf(nom_fichier, "%d", id_molecule);
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
    	
    
    printf("Veuillez introduire le Id de la premiere molécule : ");
    scanf("%d",&id_molecule1);
    printf("\nVeuillez maintenant introduire le Id de la deuxiéme molécule : ");
    scanf("%d",&id_molecule2);
    sparsegraph sg1 = lire_sparse_graphe_fichier("graphe1.txt");
    sparsegraph sg2 = lire_sparse_graphe_fichier_molecule(7);
    sparsegraph sg3 = lire_sparse_graphe_fichier_molecule(8);
    
	/*printf("\nSG2.dlen = %d", sg2.dlen);
    printf("\nSG2.vlen = %d", sg2.vlen);
    printf("\nSG2.elen = %d\n", sg2.elen);
    
    printf("\nNombres de sommets SG2 = %d", sg2.nv);
    printf("\nNombres de aretes SG2 = %d", sg2.nde);
    i = 0;
    printf("\nSG2.d : ");
    while(i< sg2.dlen){
    	printf("%d ",sg2.d[i]);
    	i++;
	}
    i = 0;
    printf("\nSG2.v : ");
    while(i< sg2.vlen){
    	printf("%d ",sg2.v[i]);
    	i++;
	}
	i = 0;
    printf("\nSG2.e : ");
    while(i< sg2.elen){
    	printf("%d ",sg2.e[i]);
    	i++;
	}*/
    
    	 
    /*on applique sparse nauty sur les deux graphes */
            
        sparsenauty(&sg2,lab1,ptn,orbits,&options,&stats,&cg1);
        sparsenauty(&sg3,lab2,ptn,orbits,&options,&stats,&cg2);
            
    // afficher un sparse graphe avec une matrice d'adjacence
    out_sparseGraphe("adjacency_matrix.txt", sg2);

    /* Compare canonically labelled graphs */

        if (aresame_sg(&cg1,&cg2))
        {
            printf("\nLes graphes sont isomoprhes ! \n");
        }
        else{
            printf("\nLes graphes ne sont pas isomorphes.\n");
        }
    printf("Press ENTER key to Continue\n");  
	getchar();
}

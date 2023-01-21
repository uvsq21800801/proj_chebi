/* This program demonstrates how an isomorphism is found between
   two graphs, using the Moebius graph as an example.
   This version uses sparse form with dynamic allocation.
*/

#include "nausparse.h"    /* which includes nauty.h */
#include <ctype.h>


// lis un fichier texte generér par gtools et le transforme en sparse graphe 
sparsegraph lire_sparse_graphe_fichier(int id_molecule) {
	
	char* nom_fichier;
	nom_fichier = (char*) malloc(sizeof(char) * 100);
	strcpy(nom_fichier, "sparse6mol/");
	sprintf(&nom_fichier[strlen("sparse6mol/")], "%d", id_molecule);
    strcat(nom_fichier, ".txt");
    
	FILE * fp;

   	fp = fopen (nom_fichier, "rb+");
    char buffer[1000];
    sparsegraph sg;
	while ( fscanf(fp, "%s", buffer) != EOF )
		{   
		   SG_INIT(sg);
		   int num_loops;
		   stringtosparsegraph(buffer, &sg, &num_loops);
		}
	fclose(fp);
	return sg;
}

void out_sparseGraphe(char* nom_fichier, sparsegraph sg1){
	/* On affiche les graphes dans un format lisible par l'humain */
	
        FILE * fp;
   		fp = fopen (nom_fichier, "w+");
        put_sg(fp,&sg1,1,0);
        fclose(fp);
}

int main(int argc, char *argv[])
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
    
    
    sparsegraph sg1 = lire_sparse_graphe_fichier(id_molecule1);
    sparsegraph sg2 = lire_sparse_graphe_fichier(id_molecule2);
    
    /*on applique sparse nauty sur les deux graphes */
            
    sparsenauty(&sg1,lab1,ptn,orbits,&options,&stats,&cg1);
    sparsenauty(&sg2,lab2,ptn,orbits,&options,&stats,&cg2);
            
    
    if (aresame_sg(&cg1,&cg2))
        {
            return 1;
        }
        else{
            return 0;
    }
	
	    
    printf("Press ENTER key to Continue\n");  
	getchar();
}

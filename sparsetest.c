/* This program demonstrates how an isomorphism is found between
   two graphs, using the Moebius graph as an example.
   This version uses sparse form with dynamic allocation.
*/

#include "nausparse.h"    /* which includes nauty.h */


// lis un fichier texte generér par gtools et le transforme en sparse graphe 
sparsegraph lire_sparse_graphe_fichier(char* nom_fichier){
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
    	
    sparsegraph sg1 = lire_sparse_graphe_fichier("graphe1.txt");
    sparsegraph sg2 = lire_sparse_graphe_fichier("graphe2.txt");
    	 
    /*on applique sparse nauty sur les deux graphes */
            
        sparsenauty(&sg1,lab1,ptn,orbits,&options,&stats,&cg1);
        sparsenauty(&sg2,lab2,ptn,orbits,&options,&stats,&cg2);
            
    /* On affiche les graphes dans un format readable par l'humain */
        FILE * fp;
   		fp = fopen ("test.txt", "w+");
        put_sg(fp,&sg1,0,10);
        fclose(fp);

    /* Compare canonically labelled graphs */

        if (aresame_sg(&cg1,&cg2))
        {
            printf("Isomorphic.\n");
        }
        else{
            printf("Not isomorphic.\n");
        }
    printf("Press ENTER key to Continue\n");  
	getchar(); 
}

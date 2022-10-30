/* This program prints generators for the automorphism group of an
   n-vertex polygon, where n is a number supplied by the user.

   This version uses a fixed limit for MAXN.
*/

#define MAXN 1000    /* Define this before including nauty.h */
#include "nauty.h"   /* which includes <stdio.h> and other system files */



int graphe_isomorphe(graph *g1,graph *g2 , int *lab1, int *lab2, int *ptn, int *orbits,optionblk *options, statsblk *stats,int m, int n){
	
		DYNALLSTAT(graph,cg1,cg1_sz); // le graphe canonique de g1 : " CG1 "
    	DYNALLSTAT(graph,cg2,cg2_sz); // Le graphe canonique de g2 : "CG2 "
		// on alloue les graphe canoniques cg1 et cg2
		DYNALLOC2(graph,cg1,cg1_sz,n,m,"malloc");
        DYNALLOC2(graph,cg2,cg2_sz,n,m,"malloc");

  		densenauty(g1,lab1,ptn,orbits,options,stats,m,n,cg1); // on applique dense nauty sur G1 et G2
        densenauty(g2,lab2,ptn,orbits,options,stats,m,n,cg2);
        
        int k;
        /* Compare les graphs canoniques */
            for (k = 0; k < m*(size_t)n; ++k)
                if (cg1[k] != cg2[k]) break;
            if(k==m*(size_t)n){
            	return 1;
			}
			else return 0;
	}


int
main(int argc, char *argv[])
{
	/*Declaration des variables alloué */
    DYNALLSTAT(int,lab1,lab1_sz); // lab1 et ptn pour le coloriage du graphe 1
    DYNALLSTAT(int,lab2,lab2_sz); // Lab2 et ptn pour le coloriage du graphe 1
    DYNALLSTAT(int,ptn,ptn_sz);
    DYNALLSTAT(int,orbits,orbits_sz); // un tableau d'orbits
    DYNALLSTAT(int,map,map_sz); // un array de map en cas d'ishomorphisme
    DYNALLSTAT(graph,g1,g1_sz); // un graphe g1 de taille g1_sz
    DYNALLSTAT(graph,g2,g2_sz); // un graphe g2 de taille g2_sz
    DYNALLSTAT(graph,cg1,cg1_sz); // le graphe canonique de g1 : " CG1 "
    DYNALLSTAT(graph,cg2,cg2_sz); // Le graphe canonique de g2 : "CG2 "
    static DEFAULTOPTIONS_GRAPH(options);
    statsblk stats;

    int n,m,i;
    size_t k;

 /* Select option for canonical labelling */

    options.getcanon = TRUE;

    while (1)
    {
        printf("\nenter n : ");
        if (scanf("%d",&n) != 1 || n <= 0)    /* On sort si le user n'injecte pas un entier*/
            break;

    	m = SETWORDSNEEDED(n); // declarer le nombre de setwords needed pour un graphe de taille n
        nauty_check(WORDSIZE,m,n,NAUTYVERSIONID); // optionnel

     	/* Allocation dynamique de la memoire pour stocker les graphes */
            DYNALLOC1(int,lab1,lab1_sz,n,"malloc");
            DYNALLOC1(int,lab2,lab2_sz,n,"malloc");
            DYNALLOC1(int,ptn,ptn_sz,n,"malloc");
            DYNALLOC1(int,orbits,orbits_sz,n,"malloc");
            DYNALLOC1(int,map,map_sz,n,"malloc");

        DYNALLOC2(graph,g1,g1_sz,n,m,"malloc");// on alloue le graphe g1 dynamiquement
        EMPTYGRAPH(g1,m,n); // on le vide
        
        /* on le remplis */
        for (i = 1; i < n; i++)   
            ADDONEEDGE(g1,i,0,m); // c un exemple ou tout les sommets sont lié au sommet 0
        
		DYNALLOC2(graph,g2,g2_sz,n,m,"malloc"); // on alloue le graphe g2
            EMPTYGRAPH(g2,m,n); // on le vide    
                
		 /* on le remplis */
        for (i = 0; i < n-1; i++)   
            ADDONEEDGE(g2,i,n-1,m); // c un exemple ou tout les sommets sont lié au sommet n-1
       
       
       
       
	    int k ;
	    // reetourn 1 si les graphes sont isomorphes, 0 cas contraire
        k = graphe_isomorphe(g1,g2 , lab1, lab2, ptn, orbits, &options, &stats,m,n);
        
        if(k == 1){
            printf("les graphes sont bien isomorphes !! :) ");
		}else{
				printf("les graphes ne sont pas isomorphes !!!");
			 }    
        printf("\n");
    }

    exit(0);
}

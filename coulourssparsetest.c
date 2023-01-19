/* This program demonstrates how an isomorphism is found between
   two graphs, using the Moebius graph as an example.
   This version uses sparse form with dynamic allocation.
*/


#include <stdio.h> 
#include <stdlib.h> 
#include <string.h> 
#include "nausparse.h"    /* which includes nauty.h */
#include <ctype.h>

unsigned int encode_string(char *string) {
    unsigned int encoded = 0;
    for (int i = 0; string[i] != '\0'; i++) {
        encoded += (unsigned int)string[i];
    }
    return encoded;
}


int compare(const void* a, const void* b) {
    int x = *(int*)a;
    int y = *(int*)b;
    return x - y;
}


 void lire_sparse_graphe_fichier_molecule(int id_molecule, sparsegraph* sg, int** liste_atomes){
	
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
		            SG_ALLOC(*sg,nb_sommets,nb_bonds,"malloc");// on alloue la memoire dynamiquement au sparse graphe selon le nombre de sommets.
		            sg->nv = nb_sommets;
		            sg->nde = nb_bonds;
		            printf("\nNbsommets = %d\n", sg->nv);
		            printf("\nNbaretes = %d\n", sg->nde);
        		}
		}
		if(lineCount == 3){
			i = 0;
			//printf("Le vecteur d : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		sg->d[i] = atoi(token); // on remplit le vecteur d
            		//printf("%d ", sg->d[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        	}
		}
		if(lineCount == 4){
			i = 0;
			//printf("\nLe vecteur v : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		sg->v[i] = atoi(token); // on remplit le vecteur v
            		//printf("%d ", sg->v[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        		}
		}
		if(lineCount == 5){
			i = 0;
			//printf("\nLe vecteur e : ");
			while (token != NULL) {
				if(isdigit(token[0])){ /*if token n'est pas un nombre */
            		sg->e[i] = atoi(token); // on remplit le vecteur v
            		//printf("%d ", sg->e[i]);
            		i++;
					}
				token = strtok(NULL, " ");	
        		}
		}
		if(lineCount == 6){
			i = 0;
			int coded;
			while (token != NULL) {
				if(token[0] != " "){
				coded =  encode_string(token); // coder l'atome vers un entier
				liste_atomes[i] = coded;
				token = strtok(NULL, " ");	
				i++;
				}
        	}
		}
    }
    
	fclose(fp);
	
}



// une methode qui va à partir de la liste d'atomes de ma molecule crée les tableaux ptn et lab pour le coloriage des graphs.
void colorer_graphe(int T[], int n, int lab[], int ptn[]) {
	int T2[n];
	int i;
    int z = 0;
    while(z < n){
    	T2[z] = T[z];
    	z++;
	}
	int stop = 0;
    int indice = 0;
    int current_value = T[0];
    lab[indice] = 0;
    indice++;
    int e =1;
    int checking = 1;
    while(stop == 0){
    	i = e;
    	while(i<n)
    	{
    		if(T[i] != -1 && checking == 1){
    			if(T[i] == current_value)
	        	{
	        		T[i] = -1;
	            	lab[indice] = i;
	            	indice++;
	        	}	
			}else{
				if(T[i] != -1 && checking == 0){
					current_value = T[i];
					lab[indice] = i;
					indice++;
					T[i] = -1;
				}
			}
		i++;
		if(i == n){
			checking = 0;
		}
    	}
    	e = e+1;
    	
    	if(e == n){
    		stop = 1;
		}
	}
   
   
    i = 0;
    for(i = 0; i < n-1; i++){
    	if(T2[lab[i]] == T2[lab[i+1]]){
    		ptn[i] = 1;
		}else{
			ptn[i] = 0;
		}
	}
    ptn[n-1] = 0;
    /*printf("\nafter coloring\n");
    z=0;
    while(z < n){
    	printf("\nLab [%d] = %d", z, lab[z]);
    	z++;
	}
	z=0;
    while(z < n){
    	printf("\nPtn [%d] = %d", z, ptn[z]);
    	z++;
	}*/
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
    options.defaultptn = FALSE;

	n=100;
	m = SETWORDSNEEDED(n);
    nauty_check(WORDSIZE,m,n,NAUTYVERSIONID);

    DYNALLOC1(int,lab1,lab1_sz,n,"malloc");
    DYNALLOC1(int,lab2,lab2_sz,n,"malloc");
    DYNALLOC1(int,ptn1,ptn1_sz,n,"malloc");
    DYNALLOC1(int,ptn2,ptn2_sz,n,"malloc");
    DYNALLOC1(int,orbits,orbits_sz,n,"malloc");
    DYNALLOC1(int,map,map_sz,n,"malloc");

    
    printf("Veuillez introduire le Id de la premiere molécule : ");
    scanf("%d",&id_molecule1);
    printf("\nVeuillez maintenant introduire le Id de la deuxiéme molécule : ");
    scanf("%d",&id_molecule2);
    
    sparsegraph sg1;
	SG_INIT(sg1);
	int* types_atomes_g1[100];
	
	sparsegraph sg2;
	SG_INIT(sg2);
	int* types_atomes_g2[100];
	
	int T[100] ;
    
    lire_sparse_graphe_fichier_molecule(id_molecule1,&sg1,types_atomes_g1);
    lire_sparse_graphe_fichier_molecule(id_molecule2, &sg2,types_atomes_g2);
    
    //printf("before coloration \n");
    int z = 0;
    while(z < sg1.nv){
    	T[z] = types_atomes_g1[z];
    	z++;
	}
	
	colorer_graphe(T, sg1.nv, lab1, ptn1); // Colorer le 1er graphe.
	
	z = 0;
    while(z < sg2.nv){
    	T[z] = types_atomes_g2[z];
    	z++;
	}
	
	colorer_graphe(T, sg2.nv, lab2, ptn2); // Colorer le 1er graphe.
	
    /*on applique sparse nauty sur les deux graphes */
    sparsenauty(&sg1,lab1,ptn1,orbits,&options,&stats,&cg1);
    sparsenauty(&sg2,lab2,ptn2,orbits,&options,&stats,&cg2);
    
    if (aresame_sg(&cg1,&cg2))
        {
            printf("\nLes graphes sont isomoprhes ! \n");
    	}else{
            printf("\nLes graphes ne sont pas isomorphes.\n");
    	}
		
	    
    printf("Press ENTER key to Continue\n");  
	getchar();
}


# Projet de fouille de données

## 	Contexte

Dans le cadre de l'eu de Fouille de données du Master de Bioinformatique de l'Université Paul-Sabatier, un projet visant à mettre au point et évaluer une méthode pour annoter les systèmes ABC dans les génomes d'eucaryote a été effectué. Ce rapport, résume le déroulement de ce projet, les méthodes utilisés ainsi que les résulstats obtenus.

### Les systèmes ABC

Les systèmes ABC forment une des plus grandes et des plus vieilles familles multi-géniques du monde du vivant. Présent dans les 3 grand règnes du vivant (Bactérie, archées et eucaryotes), leur l'architecture est très conservée.

Les transporteur ABC sont composés de 2 domaines pour les exporteurs et les 3 domaines pour les importeurs:
-   **MSD** : Membrane Spanning Domain. 2 domaines MSD (hétéro ou homo-dimère) forment le pore à travers la membrane.
-   **NBD** : Nucleotide Binding Domain. 2 domaines (hétéro ou homo-dimère) fournissent l’énergie pour le transport actif par hydrolyse de l’ATP.
-   **SBP** : Solute Binding Protein. 1 domaine capture le substrat et le mène à l’entrée du pore.

Les transporteurs sont composés de 1 à 5 protéines en fonction du nombre de domaines portés par le, ou les gène(s) condant pour les partenaires ABC.

Par exemple:
-   NBD -NBD : un gène port 2 domaines NBD 
-   MSD-NBD : un gène portant un domaine MSD suivi d’un domaine NBD
-   NBD-MSD-MSD

Les systèmes ABC sont très anciens. Ils ont donc subis un grand nombre de  dupliquations et parfois ont été perdu par certains ancêtres. Leur ancienneté amène aussi une grande diversité de ces systèmes, grâce à l'accumulation de mutations sur les séquences concernées.  Les systèmes ABC sont donc classées en sous-familles déterminées suite à une analyse de leur similarité de séquences qui indique indique si oui ou non les molécules transportées par les transporteurs sont similaires. Mais tout les individus dans la même famille multigénique ne partagent pas la même similarité de séquences Pour certain individus, une mutation peut changer complètement la fonction.

## Analyse

### Objectif du projet

Le but de ce projet est de:

- Prédire si des gènes code pour des partenaires ABC
- Pour les gènes identifiés comme étant ABC, prédiction de leur architecture en domaines fonctionnels.
- Évaluer la qualité des prédictions et comparer les performances des classificateur entre eux.


###  Analyse des données

Pours atteindre ces objectifs, les infomations contenues dans la base de données ABCdb ([https://www-abcdb.biotoul.fr/](https://www-abcdb.biotoul.fr/))  ont été utlisées. 

Cette dernière a été constituée à partir de l’expertise d’une centaine de génomes complets. Les génomes expertisés ont ensuite permis de faire une annotation automatique d’autres centaines de génomes complets.

La base de données contient les données suivantes :

-   des génomes complets et leur classification taxonomique 
-   les gènes de chaque génome 
-   les domaines identifiés sur les génes 
-   les relations d’orthologie 1:1 
-   les gènes identifiés comme ABC et les systèmes réassemblés

Repartis dans les tables suivantes:

**Taxonomy** renseigne sur la  taxonomy du NCBI. Il permet donc de reconstruire l'arbre phylogénétique d'un organisme. 
 
**Strain** contient des informations relatives aux organismes dont le génome a été séquencé (nom de la souche, espèce, taux de GC....)

**Chromosomes** contient des informations sur les chromosomes séquencés (numéros, taille, si circulaire ou linéaire....)

**Gene** contient l'ensemble des gènes prédits et annotés dans les génomes,  leurs position de début et de fin, le n° du gène, le score BLAST de l'alignement avec lui-même. 

**Functional_Domain** décrit les domaines présents dans les banques de données publiques de familles de protéines et de domaines.

**Conserved_Domain** contient les résultats des analyses avec *rpsblast* pour détecter la présence de domaines sur l’ensemble des protéomes considérés

**Orthology**  contient les résultats de l’identification d’orthologues 1:1 entre tous les gènes de tous les génomes considérés. Cette table compile les résultats d’analyses BLAST, c’est-à-dire les alignements entre paires d’orthologues 1:1 prédits.

**Protein** contiennent les informations sur les séquences potentiellement ABC

**Assembly** contient les informations sur les systèmes ABC reconstruits et expertisés

Pour pouvoir entrainer le classificateur, il faut donc traiter les données afin d'en extraire :

-	L'ensemble des gènes de la base de données, ainsi que leur caractéristique (longeur, position...etc).
-	S'ils codent, ou non, pour un partenaires ABC.
-	Les domaines fonctionnels présent sur le gène.

Ces information sont contenu sur les tables  *Functional_Domain*, *Conserved_Domain*, *Protein*, *Assembly* et *Gene*, Seulement ces tables seront conservées pour l'analyse


## Conception

Afin d'atteindre les objectifs fixés, il a été choisit de procéder en 2 étapes. Dans un premier temps, la prédiction de gène codant pour des partenaires ABC à partir de l'ensemble des gènes de la base de données. Puis, dans un second temps, la prédiction de l'architecture en domaines fonctionels à partir de partenaires ABC uniquement.
L'ensemble des scipts utilisés, ainsi que la documentation permettant leur utilisation sont disponible sur le [gitlab du projet.
](https://gitlab.com/LouDu/datamining.abc)

### Les matrices

Après avoir instancié la base de donnée en local, avec MySQL. L'utilisation de la librairie mysql.connector, sous Python 3, a permis la sélection:

- de l'ensemble des gènes de la base de données ainsi que, si oui on non, ils codent pour des partenaires ABC. Cette dernière information servira de classe pour la première matrice.	
- l'architecture en domaines fonctionels des partenaires ABC, qui servira de classe pour la deuxième matrice.
- les domaines conservés pour chaque gène.

Cela permet de créer 2 matrices: une pour l'identification des gènes abc et une pour l'identification l'architecture en domaines fonctionnels.

La structure des 2 matrices est la suivantes:

**Classe | Gene_ID | longueur du gène | nombre de domaine de type MSD | nombre de domaine de type NBD | nombre de domaine de type SBP**

Concerant la matrice permettant de prédire la structure en domaines fonctionnels, il a été choisit de créer 4 classes différentes :

 - MSD seul
 - NBD seul
 - SBP seul
 - Multiples

Ces deux matrices seront ensuite divisées en un set apprentissage et un set de test. Le set d'apprentissage sert pour l'entrainement du classificateur, tandis que le set de test sert à évaluer la performance du classificateur, et à estimer la précision et l'exactitude de la prédiction.

### Les  Classificateurs
Une fois les matrices réalisées, il a été choisit d'utiliser 3 classificateurs différents afin de comparer leur performances. 

#### L’arbre de décision

Un arbre de décision permet de répartir une population d'individus en groupe homogènes selon un ensemble de variables, appeler *variables prédictives*.

Dans un arbre de décision, chaque noeuds représente un test sur une des variables descriptive. Chaque branche représente le le résultat d'un test sur la valeur de l'attribut du noeuds  et chaque feuille représente un classe que l'on cherche à prédire
![plot iris dtc](https://scikit-learn.org/stable/_images/sphx_glr_plot_iris_dtc_002.png)
##### Avantage et inconvénient

Les arbres de décision sont relativement facile à programmer et simple a faire tourner

Ils sont en revanches très sensible aux données de départ, et sont sensible au sur-apprentissage (trop de branches, l'arbre est trop spécifique et ne généralise pas bien les données ) , et produisent des résultats à faible précision si on lui donne de nouvelles données

#### Classificateur bayésien naïf gaussien

Les classificateur bayésien naïf gaussien est un classificateur qui essaye de prédire a classe de la variable à prédire en supposant une total indépendance entre toute les variable explicative (Par exemple, pour prédire si un fruit est une pomme avec les variable "rond", "rouge" , le classificateur considérera les variables comme indépendantes les unes par rapport au autre pour sa prédiction). Le classificateur est gaussien suppose que la répartition des valeurs des différentes variables sont répartit de manières gaussienne

##### Avantage et inconvénient
Ces classificateur sont extrêmement rapide comparer à d'autre algorithme de classification et on besoin d'un moins grande quantité de données pour être entrainer.

Cependant, ils posent l'hypothèse de l'indépendance des arrtibuts, hypothèse rarement vérifié.


#### Classificateur bayésien naïf de Bernoulli

Ce classificateur fonctionne comme un classificateur Bayésien gaussien, à la différence que ce classificateur se base sur des booléens ( et donc la présence/absence d'éléments, à la place de leur fréquences) Par exemple, pour la classification de livre, cette algorithme peut choisir de place un livre dans la classe "chine", car le livre contenait le mot en question une fois.

##### Avantage et inconvénient

Ce classificateur possède les mêmes inconvénients et avantages que le classificateur bayésien.

##	Réalisation

### Les matrices

Les matrices sont générées par le script Data_preparation.py, les instructions d'utilisation ne seront pas décrites dans ce rapport car présentes dans la documentation du projet.
Le script utilise mysql.connector pour exécuter des requêtes SQL dans la base de données et récupère les informations souhaitées. 
Deux paramètres permettents de faire varier les informations comprises dans les matrices :
 - Le score minimal (S) nécessaire à la récupération des domaines conservés.
 - Le nombre minimum d'occurence du domaine (ND) dans la base de données pour être considéré comme étant spécifique à une catégorie de structure de domaine fonctionnel.

Le script crée ensuite deux fichier CSV :
- abc.csv, utilisé pour la prédiction de gènes codant pour des partenaires ABC
- subfamillies.CSV, utiliser pour la prédiction des structures en domaines fonctionnels.


### Les classificateurs

Les classificateurs sont executés dans le script Annotation.py. Ce dernier prend en paramètres une des matrices et fournit en sortie les résultats de la prédiction sur le jeu de test. Il est possible de préciser en paramètre la proportion du jeu de donnés à utiliser pour l'entrainement (par défault  80%).
Tout les algorithmes ont été réaliser avec la librairie sklearn de python. Les précision d'utilisation de ce script sont dans la documentation du projet.
 
### Résultats

Afin d'estimer l'impact des paramètres et de comparer les classificateurs entre eux, plusieurs prédiction ont étés effectuées. Il important de noter que pour chaque paramètres, le même jeu d'apprentissage est utilisé pour les 3 classificateurs afin de pouvoir comparer les résultats en eux. 

*Tableau des résultats pour la prédiction des gènes ABC en fonction de différents paramètres*

|Paramètres|Arbre de décision|Classificateur Bayésien naïf Gaussien |  Classificateur Bayésien naïf de Bernoulli |
|-----	| :-----| :----- | :--- |
|S=30,  ND=10 |Précision=91.5% Exactitude=98.5% |Précision=72.5% Exactitude=97.5% |Précision=41.0% Exactitude=95.3% |
|S=70, ND=50 | Précision=91.2% Exactitude=98.3%| Précision=91,0% Exactitude=97.5% |Précision=80% Exactitude=97.5% |
|S=100, ND=70 | Précision=90,9% Exactitude=98.1%| Précision=80,9% Exactitude=97.7% |Précision=83.9% Exactitude=97.5% |
|S=150, ND=100 | Précision=89.3% Exactitude=97.3%| Précision=73.6% Exactitude=96.8% |Précision=86.1% Exactitude=97.0% |
|S=200, ND=150| Précision=94.9% Exactitude=96.2%| Précision=9.66% Exactitude=71.17% |Précision=84.7% Exactitude=96.2% |
 
À noter que, pour chaque itération, l'exactitude des classificateurs peut varier de +/- *0,3%*, et la précision varie de +/- *1%*. 

*Tableau des résultats pour la prédiction des structures en domains fonctionels :*

|Paramètres|Arbre de décision|Classificateur Bayésien naïf Gaussien |  Classificateur Bayésien naïf de Bernoulli |
|-----	| :-----| :----- | :--- |
|S=30,  ND=10 |Exactitude : 98.6% |Exactitude: 95.0% |Exactitude : 88% |
|S=70, ND=50 |Exactitude : 97%| Exactitude : 95% | Exactitude : 88% |
|S=100, ND=70 |Exactitude : 96.6%| Exactitude : 94.5% | Exactitude : 87.7% |
|S=150, ND=100 |Exactitude : 89.5%|  Exactitude : 87.8% | Exactitude : 80.5% |
|S=200, ND=150 |Exactitude : 66.7%|  Exactitude : 59.7% | Exactitude : 54.8% |

A noter que, pour chaque itération, l'exactitude des classificateurs peut varier de +/- *0,5%*
##	Discussion

### Analyse des résultats

#### Prédiction des partenaires ABC
Pour la prédiction des gènes codant pour des partenaires ABC, il est important de s'intéresser à la précision plustôt qu'à l'exactitude. En effet, dans la base de données, sur l'ensemble des gènes à disposition, seul 5% d'entre eux codent pour des partenaires ABC. Un classificateur prédisant 100% du temps : NON-ABC, aura donc une exactitude de 95% mais une précision très faible.
##### Arbre de décision

L'arbre de décision semble être la meilleur méthode pour prédire si un gène code pour un partenaire ABC. Sa précision moyenne est de 90%.

Plus *nb_domain* et  de *score_min* sont élévés, plus l'exactitude et la précision diminuent. Néanmoins, les résultats de l'arbre de décision semble être le moins affecté par les variations de *nb_domain* et  de *score_min*
Il est intéresant de noter que pour *nb_domain* et  de *score_min* très élevé, respectivement 150 et 200, la précision est très bonne au détriment de l'exactitude. Cela peut être expliqué par un prédiction fréquente de partenaires ABC, permettant une sensibilité plus importante au détriment de la spécificité.

##### Classificateur bayésien naïf gaussien

Le classificateur bayésien naïf gaussien as une bonne exactitude (en moyenne égal à 97%) mais sa précision ne dépasse le seuil des 90% uniquement si *nb_domain = 70* et *score_min = 50*

Ce classificateur voit lui aussi son exactitude et précision diminuer si*nb_domain* et *score_min* sont trés éléver. De plus, une chute drastique de la précision est observé pour des valeurs très importantes des paramètres.

##### Classificateur bayésien naïf de Bernoulli

Le classificateur bayésien naïf de Bernoulli possède une précision très faible pour les paramètres par défault (40%). Une augmentation des paramètres améliore ces résultats, sans pour autant permettre une prédiction de meilleur qualité des autres classificateurs.


#### Prédiction des structures en domaines fonctionnels
La précision ne pouvant être calculée que pour les données ayant des classes binaires, l'évalutation des prédictions de structure en domaines fonctionnels se basera sur l'exactitude uniquement.
Pour l'ensemble des classificateurs, les paramètres par défaults donnent les meilleurs résultats en termes de prédiction de structure en domaines fonctionnels. L'augmentation des paramètres se fait au détriment de la l'exactitude pour les 3 mèthodes. Comme pour la prédiction de gènes codant pour des partenaires ABC, l'Arbre de décision donne les meilleurs résultats, jusqu'à une exactitude 98.6% avec les paramètres par défault.

### Conclusion sur la qualité des méthodes

L'arbre de décision semble être le meilleur classificateur pour le type de données présent dans les matrices construites. Il possède la meilleur capacité de prédiction pour prédire si un gène est un partenaire ABC et pour identifier sa structure en domaines fonctionnels. Le classificateur n'as aussi pas besoin que l'on filtre les données en faisant varier *nb_domain* et *score_min*. Cependant, cette méthode est connues pour être sensible au sur-apprentisage et n'est pas adaptée à l'ajout de nouvelle données.

Le classificateur bayésien naïf gaussien donne des résultat comparable a l'arbre de décision pour la prédiction des gène partenaire du système ABC et donne de bon résultat avec ces mêmes paramètres pour la prédiction des sous-familles. Les résultats sont aussi plus fiable que ceux de l'arbre de décision, car non affecter par le sur-apprentissage.

Le classificateur bayésien naïf de Bernoulli est le plus mauvais classificateur tester. Il ne donne pas de résultats significatif pour la prédiction des partenaires du système ABC et pour la prédiction des sous-famille. Ces faibles résultats peuvent s'expliquer par le fait que ce classificateur est adapté au traitement de données sous forme de booléen. Il n'est donc pas optimiser pour les données ici fournit.  Mais ce classificateur permet de confirmer que, pour les classificateur n'étant pas l'arbre de décision, les meilleurs paramètres pour réaliser la matrice sont *nb_domain = 50* et *score_min = 70*.

Le meilleur classificateur pour prédire si un gène est un partenaire du système ABC et pour déterminer la structure en domaine fonctionnels semble donc être le classificateur bayésien naïf gaussien combiner avec un pré-traitement des données.

##	Bilan et perspectives

Les résultats obtenus pour la prédiction de gène codant pour des partenaires ABC sont relativement satisfaisants. 90% des gènes codant pour des partenaires ABC ont été correctement prédits et une exactitude de avoisinant les 99% indique que quasiment aucun gène non-ABC a été faussement prédit comme étant ABC.

Cependant les résultats pour la prédiction de la structure en domaines fonctionnels sont plus nuancés. Bien que l’exactitude des classificateur est très satisfaisante (98.5% pour l’arbre de décision), la méthode utilisée ne permet d’identifier que les gènes comportants un seul des domaines caractéristiques des partenaires ABC. Les gènes comportant plusieurs domaines sont alors classés comme étant “multiples” sans pour autant donner la composition en domaines fonctionnels. Une approche utilisant autant de classes que de combinaisons de domaines fonctionnels possible a été tenté, sans succès. En effet, le trop grand nombre de classes à eu pour conséquences de ne pas être en mesure d’avoir un classificateur pouvant prédire correctement ces dernières. Une matrice différente pourrait éventuellement pallier à ce problème.

De plus, afin de correctement évaluer les classificateur, il aurait fallu utiliser un nouveau jeu de données pour vérifier que l’arbre de décision n'est pas été victime de sur-apprentissage.

Pour conclure, si ce projet était à refaire, une approche différente pourrait être tentée. Dans un premier temps, la création d’un matrice comportant plus d’informations susceptible d’améliorer l’apprentissage du classificateur, comme par exemple l’utilisation des données concernant l’Orthologie pour identifier les gènes orthologues 1:1 susceptible de coder pour un partenaire ABC. Dans un second temps, l’utilisation d’une autre méthode de classification plus adaptée aux données. Le très grand nombre d’individus et de variables dans la base de données pousse à utiliser des méthodes plus souple telle que les réseaux de neurones.

##	Gestion du projet

### Organisation

Le groupe s’est réuni toutes les semaines pour discuter de l’avancement du projet, le plus souvent en présentiel, mais aussi sur discord. Suite aux réunions, un objectif pour la prochaine réunion était fixé et un agenda des tâches était ensuite établi sur Trello. La majeure partie du travail s’est effectuée en local, suite au réunion, sur l'ordinateur instanciant la base de données. Un Gitlab du projet a été crée pour herberger les scripts. Le rapport a été rédigé sur StackEdit.

 Différentes tâches ont été établies et réparties suivant le calendrier suivant :

-   De début à mi-Avril : Appréhension de la base de données et implémentation en local sur mySQL. Débat sur les données qui seront utilisés dans la matrice et les classificateur utilisés
    

-   Mi-avril : Création de la première matrice et rédaction des scripts de tests
    
-   Fin avril : Evaluation des méthodes de classification choisi
    
-   Mai : Rédaction du rapport
    
Chaque tâche s’est vu répartit de la façon suivante:
-   Implémentation de la base de données : Etienne
-   Script de la première matrice : Etienne   
-   Script Data_preparation : Lou
-   Script Annotation : Lou
-   Evaluation des classificateur : Etienne et Lou
-   Gitlab : Lou
-   Rédaction du rapport : Etienne et Lou

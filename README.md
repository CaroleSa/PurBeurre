OC Projet 5 


Auteur : 
Carole Sartori


Le programme Pur Beurre a été créé dans le but de proposer une alternative aux aliments caloriques du quotidien.
Il utilise les données de l'A.P.I. d'Open Food Facts et donne accès, suite au choix d'un aliment,
à un substitut au nutriscore plus intéressant.
Il est également possible d'enregistrer ses recherches.


Requirements :
mysql-connector==2.2.9
mysql-connector-python==8.0.16
requests==2.22.0  


Données configurables :

Le programme fonctionne à partir d'une base MySql :
Éléments de connexion à MySql (fichier connection.yml)


Fonctionnement du programme :
Sur le terminal, lors du lancement du programme, 
l'utilisateur se voit proposer 3 choix : 
- choix 1 > quels aliments souhaitez-vous remplacer ?
- choix 2 > retrouver mes aliments substitués
- choix 3 > quitter. 

Si l'utilisateur tape "1", une liste de catégories lui est proposée.
Suite au choix d'une catégorie, s'affiche la liste des aliments.
En choisissant un aliment, l'utilisateur se voit proposer un substitut,
ses informations détaillées ainsi que 3 choix possibles :
- enregistrer sa recherche 
- ne pas enregistrer la recherche
- avoir un autre substitut possible.

Si l'utilisateur tape "2", la liste des aliments enregistrés s'affiche. 
Suite au choix d'un aliment, le programme affiche les informations détaillées
de son substitut ainsi que 3 choix possibles :
- supprimer cet aliment
- chercher un autre aliment substitué enregistré
- retourner au menu.

Si l'utilisateur tape "3", il met fin au programme.

À tout moment, l'utilisateur à la possibilité de retourner aux étapes précédentes.

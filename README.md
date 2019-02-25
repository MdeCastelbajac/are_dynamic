# ARE DYNAMIC

## RESTAURATION : Optimisation et coordination des tâches

Mardi 19 février

### Présentation du projet

Nous avons décidé de modéliser et simuler, dans le cadre de l'Atelier de Recherche Encadrée, l'activité d'un restaurant, en étudiant l'organisation et la coordination des tâches en nous concentrant sur l'optimisation du temps d'attente.

Nous rappellerons qu'un système complexe est "un ensemble constitué de nombreuses entités dont les interactions produisent un comportement global difficilement prévisible" (définition du CNRS). Nous détaillerons ci-après les entités, intéractions et comportements de notre modèle.


### Description du modèle

Le modèle est bâti autours de cinq points clés : 
- Les clients qui arrivent aléatoirement.
- Les tables que ces derniers remplissent pour passer commande aléatoirement.
- Les serveurs, chargés entre autre de récupérer ces commandes et de les envoyer en cuisine. Ils effectuent également tout un tas d'autre tâches plus ou moins intermédiaires : apporter les plats, débarasser, accueillir les clients, etc.
- Une cuisine, pivot du modèle, chargée de trier, en fonction de divers paramètres, les plats à cuisiner / préparer en respectant une contrainte fondamentale : les plats commandés à une même tables doivent être servis dans un intervalle de temps restreint, les clients d'une même tables s'attendent à manger ensemble.
- Un Temps d'Attente Moyen ou TAM, qui est la valeur à surveiller. Elle se construit en calculant le temps d'attente, pour un client, entre deux étapes (ie arrivée -> commande, commande -> dégustation, etc.).
<p align="center">
   <img src="https://github.com/TortueDivine/are_dynamic/blob/master/Pr%C3%A9sentation/Restaurant_test_1.jpg?raw=true" alt="Illustration de l'environnement de simulation"/>

</p>

### Objectifs

On s'aperçoit immédiatement que les comportements respectifs des serveurs et de la cuisine auront une grande influence sur le TAM.

Nous nous demanderons donc s'il existe des comportements plus efficaces (compte tenu de la place de l'aléatoire) qui permettent d'obtenir un TAM minimal.

On pourra songer aussi à modifier d'autres paramètres plus spécifiques du modèle pour en tirer d'autres observations comme la rapidité d'exécution des différentes entités, ou encore la variété (et donc la variabilité) des temps de cuisson / préparation des plats.


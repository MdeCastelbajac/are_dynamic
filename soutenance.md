
## Introduction

Dans le cadre de L’ARE nous devions modéliser un système complexe. Qui selon le CNRS est :
> un ensemble constitué de nombreuses entités dont les interactions produisent un comportement global difficilement prévisible

La simulation choisie du restaurant est de type ABM ([voir ici](ExemplesDocu.md)): 
> An agent-based model (ABM) is a class of computational models for simulating the actions and interactions of autonomous agents with a view to assessing their effects on the system as a whole
 
L’ABM connaît actuellement beaucoup de succès du fait de ses applications multiples notamment commerciales et scientifiques.


L’idée fondamentale, est l’application de règles à l’**état microscopique** à ce que l’on appelle des **agents autonomes**, qui interagiront entre eux, engendrant ainsi une effet de système à **l'échelle macroscopique**.


Le but de ce projet est de modéliser et de simuler l'activité d'un (petit) restaurant avec Python. Si notre travail peut être relié à des ABM préexistants, nous avons souhaité rester le plus autonome possible en construisant de A à Z le modèle, la simulation (oui, même les dessins) et le présent site. Le choix de la **programmation orientée objet** s'est rapidement imposé.

Le restaurant nous a semblé être le choix le plus original, et la difficulté progressive et modulable. Il présente également l'intérêt notable d'être concret! En effet la simulation et l'optimisation est un sujet aux résultats palpables.

Enfin il présente l'intérêt et la difficulté d’avoir des paramètres multiples, ainsi que de présenter une notion d’aléatoire. En effet les choix des plats initié par les tables sont purement aléatoires.

Depuis la première présentation, il y a eu quelques changements, des déconvenues aussi - mais nous y reviendrons - et, bien sûr, les forums de programmation comme StackOverflow ont été nos meilleurs amis. Nous vous présentons donc aujourd'hui le projet dans sa version finale, les expériences que nous avons pu mener ainsi que les résultats que nous avons pu exploiter. Enfin, nous reviendrons sur les améliorations qu'il reste à apporter au projet.

**Voici les problématiques que nous nous sommes posées :**

- **Quel est l’impact du nombre de serveurs sur le TAM?**
  - **Est il proportionnel, ou autre?**
  - **Existe t il un nombre de serveurs optimal, ou à partir duquel celui-ci n’a plus d’effet significatif sur le TAM?**

- **Quel est l’impact de la carte sur le TAM? :**
  - **Selon la variance des temps de cuisson.**
  - **Selon le nombre de choix.**
 
## Retour sur une description générale du modèle.
 Nous décomposerons le modèle que nous avons construit selon trois aspects distincts : 
 
- D'une part, les **paramètres** :
  
  - <strong>L'affluence des clients</strong> : fixe et maximale. 
   
  - <strong>La carte des plats</strong> qui à chaque plat associe un temps de cuisson ou de préparation unique.
    
       
        # MENU OF DISHES
        MENU = {"Boeuf Bourguignon" : 35.30,
        "Spicy Burger" : 15.30,
        "Tartar" : 13.0,
        "Veggie Salad" : 10.30,
        "Veggie Burger": 14.30,
        "Ceasar Salad" : 12.30,
        "Bruceta" : 26.30,
        "Daily Pasta" : 13.30,
        "Carbonara" : 14.0,
        "Homard" : 18.00,
        "Filet de Saint-Pierre" : 20.00,
        "Filet de Merlu a la Plancha" : 16.00,
        "Noix de Saint-Jacques au beurre salé" : 21.00
        }
        
- D'autre part, les **agents**: 
 
  - les <strong>tables</strong> de quatre qui une fois remplies, commandent aléatoirement des plats parmi ceux proposés dans la  carte.
    
<p align="center">
   <img src="https://github.com/MdeCastelbajac/are_dynamic/blob/test/table_served.gif?raw=true"/>  
</p>

  - les <strong>serveurs</strong> qui peuvent, dans cet ordre de priorité : accueillir de nouveaux cients, servir les plats,    prendre les commandes, les transmettre à la cuisine ou être inactif.

<p align="center">
   <img src="https://github.com/MdeCastelbajac/are_dynamic/blob/test/waiter_down.gif?raw=true"/> 
</p>
    
- Enfin, la **variable calculée** :   
  - Le <strong>temps d'attente moyen</strong>, noté <strong>TAM</strong> qui représente le temps moyen qu'attendent les clients entre leur arrivée et leur départ du restaurant. 
  
## Echelle micro : quelques spécificités 

#### Exemple d'OOP
    
    class Waiter:

         #Initialization
         def __init__(self, num, room, coords):
             self.num = num # Numéro du serveur
             self.room = room # Placement dans la salle
             self.img = self.room.create_image(coords[0], coords[1], image = waiter_down) # Création de l'image
             self.coords = coords # Waiter's real-time coords
             self.orders = {} # Waiter's list of orders
             self.delivery = 0 # waiter's list of delivery
             self.waiting = False # the waiter's waiting
             self.number = 0 # Target table's number
             param.waiters[self.num] = 0 #Waiter's state

 Pourquoi c'est utile : 
 - Chaque serveur est une **instance** de la classe. Les fonctions associée s'appliquent donc automatiquement à tous les serveurs (sous certaines conditions)
 - On a donc pas besoin de tous les "surveiller". 
 
 
#### Le déplacement
 
       def movement_x(self, x_dir): # Those parameters are conditional, they indicate which direction
       # the waiter takes
           if x_dir > 0 and x_dir != 0:
               room.delete(self.img)
               self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_left)
               self.room.move(self.img, -5, 0)
           elif x_dir !=0:
              room.delete(self.img)
              self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_right)
              self.room.move(self.img, 5, 0)
           self.coords = self.room.coords(self.img)
         
 - La fonction prend une direction ( + ou - ) en paramètre.
 - On change de sprite a chaque changement de direction.
 
       def go_to_kitchen(self):
        
           if self.coords[1] != koords[1]:
               y_dir = self.coords[1] - koords[1]
               root.after(10, self.movement_y(y_dir))
           elif self.coords[0] != koords[0]: 
               x_dir = self.coords[0] - koords[0]
               root.after(10, self.movement_x(x_dir))
 
 
 
#### Calcul du TAM
 
 Dans la classe Table :
 
      self.timer = 0.0
      self.timer_debut_action = 0.0
      self.timer_fin_action = 0.0

- On récupère le temps écoulé par la différence des deux derniers timers - lancés resp. en début et en fin d'action -.
- On calcule simplement la moyenne des temps écoulés pour toutes les tables


#### La cuisson

- Les plats d'une même commande doivent tous être prêt en même temps.
- Si tous les plats d'une même commande sont presque prêt, la cuisine finit leur cuisson en priorité.
- Sinon, elle prend les plats les plus longs à cuire. Elle retire a chaque tour 1.0 seconde.
- Ces "choix" ont une influence sur le TAM. A chaque tour de fonction, toutes les tables qui attendent voient leur temps d'attente augmentés d'1.0 seconde.

#### Comment ça marche ?

 - Le programme fait tourner en boucle des fonctions **main** pour chaque classe.
 - Les serveurs effectuent les actions les plus importantes en priorité.
 - Les tables effectuent leurs actions toujours dans le même ordre.

## Expériences et Exploitation des résultats

#### Protocole 1
Nous commencerons par observer **l'influence du nombre de serveur**.



Rappelons ici les questions que nous nous posions au début du projet : 
- Existe-t-il, d'une part, un nombre de serveur qui permet d'obtenir un **TAM optimal**? et, par suite, un nombre de serveur au-delà duquel le TAM ne diminue plus?


- On isole le paramètre **nombre de serveurs**. On fixe alors tous les autres paramètres. Pour toutes nos expériences on fixe le nombre de table à **8**, et la carte au modèle présenté ci-dessus.

Ensuite, pour un nombre de serveur **variant de 1 à 8**, on récupère les **50 premières valeurs de Temps d'attente**, un nombre qui paraît suffisament grand compte tenu de l'influence qu'auront les choix aléatoires de plats sur celles-ci. L'intervalle du nombre de serveur s'explique facilement par le fait qu'au-delà de huit, il y a toujours un ou plusieurs serveurs qui sont inactifs, du fait du nombre de table préalablement fixé.

Enfin, on construit un **histogramme des TAM en fonction du nombre de serveurs**.


#### Résultats
On construit par la suite le graphe suivant duquel on peut déduire plusieurs affirmations intéressantes :







#### Protocole 2 
Nous observerons ici l'influence de la carte, de part sa **taille**, et de part **la variance des temps de cuisson**.
Reprenons donc la carte utilisée jusqu'ici
    
       
       # MENU OF DISHES
        MENU = {"Boeuf Bourguignon" : 35.30,
        "Spicy Burger" : 15.30,
        "Tartar" : 13.0,
        "Veggie Salad" : 10.30,
        "Veggie Burger": 14.30,
        "Ceasar Salad" : 12.30,
        "Bruceta" : 26.30,
        "Daily Pasta" : 13.30,
        "Carbonara" : 14.0,
        "Homard" : 18.00,
        "Filet de Saint-Pierre" : 20.00,
        "Filet de Merlu a la Plancha" : 16.00,
        "Noix de Saint-Jacques au beurre salé" : 21.00
        }
    
    
  Si l'on veut obtenir des résultats exploitables, il nous faut utiliser seulement des cartes ayant une **même moyenne de temps de cuisson.**
  
  On commence donc par calculer simplement la moyenne et la variance des temps de cuisson de cette carte, qui servira de référence pour la suite de l'expérience.
  
  
    Moyenne = 17.44
  
    Variance = 46.44
  
  
 On gardera le même nombre de tables, et on fixera le nombre de serveurs à .
 
 Dans un premier temps, on réduit puis augmente la taille de la carte, de telle façon à ce qu'elle conserve sa moyenne, et on récupère les valeurs du TAM selon la même procédure que précédemment.

Voici les deux cartes obtenues après modifications : 

**Taille + :** 

      
      # MENU OF DISHES
        MENU = {"Boeuf Bourguignon" : 35.30,
        "Spicy Burger" : 15.30,
        "Tartar" : 13.0,
        "Veggie Salad" : 10.30,
        "Veggie Burger": 14.30,
        "Ceasar Salad" : 12.30,
        "Bruceta" : 26.30,
        "Daily Pasta" : 13.30,
        "Carbonara" : 14.0,
        "Homard" : 18.00,
        "Filet de Saint-Pierre" : 20.00,
        "Filet de Merlu a la Plancha" : 16.00,
        "Noix de Saint-Jacques au beurre salé" : 21.00,
        "Kouign Amann" : 17.0,
        "Poêlée de Champignons et légumes du jardin" : 18.30,
        "Salade de Tofu" : 15.0,
        "Ratatouille" : 20.30
        }
        
        Moyenne = 17.48

**Taille - :**


       # MENU OF DISHES
        MENU = {"Boeuf Bourguignon" : 35.30,
        "Spicy Burger" : 15.30,
        "Tartar" : 13.0,
        "Veggie Salad" : 10.30,
        "Veggie Burger": 14.30,
        "Ceasar Salad" : 12.30,
        "Bruceta" : 26.30,
        "Daily Pasta" : 13.30,
        "Carbonara" : 16.0
        }

        Moyenne = 17.44
 
 On construit avec ces données le graphe suivant : 
 
       
 
 



Dans un second temps, on s'occupe de la variance, qu'on s'emploie à augmenter, puis à diminuer.
On procèdera encore une fois de la même façon.
  
**Variance + :**
        
        # MENU OF DISHES
        MENU = {"Boeuf Bourguignon" : 42.30,
        "Spicy Burger" : 25.30,
        "Tartar" : 8.0,
        "Veggie Salad" : 3.30,
        "Veggie Burger": 6.30,
        "Ceasar Salad" : 7.30,
        "Bruceta" : 31.30,
        "Daily Pasta" : 17.30,
        "Carbonara" : 10.0,
        "Homard" : 21.00,
        "Filet de Saint-Pierre" : 20.00,
        "Filet de Merlu a la Plancha" : 11.00,
        "Noix de Saint-Jacques au beurre salé" : 26.00
        }

        Moyenne = 17.44 (=)
  
        Variance = 131.44


**Variance - :**
       
       MENU = {"Boeuf Bourguignon" : 20.30,
        "Spicy Burger" : 17.30,
        "Tartar" : 20.0,
        "Veggie Salad" : 15.30,
        "Veggie Burger": 16.30,
        "Ceasar Salad" : 14.30,
        "Bruceta" : 19.30,
        "Daily Pasta" : 18.30,
        "Carbonara" : 15.0,
        "Homard" : 21.00,
        "Filet de Saint-Pierre" : 17.00,
        "Filet de Merlu a la Plancha" : 16.00,
        "Noix de Saint-Jacques au beurre salé" : 19.00
        }
        
        
        Moyenne = 17.44 (=)
  
        Variance = 4.44


On construit avec ces données le graphe suivant : 
 




## Conclusion et dernières réflexions 

Ce projet fut certes l'occasion de simuler un système dynamique, mais également l'opportunité de mettre en pratique des connaissances et d'en acquérir de nouvelles. Ainsi dans cette simulation il a été question d'utiliser Python en POO et de se familiariser avec la bibliothèque graphique Tkinter. Il a également été question de se familiariser avec Github pages. Certains talents personnels ont même été mis au service du projet. Les dessins ont par exemple été fait entièrement from scratch.

Ce fut également l'occasion de faire connaissance avec tout un domaine et une forme de simulation qui est de type ABM. Il existe même des solutions visant à faciliter des simulations de ce type, tels qu’**Anylogic**, permettant de faire divers types de simulation sans réinventer la roue à chaque fois! 

Grâce à cette simulation nous avons pu établir certaines conclusions et répondre à certaines de nos problématiques.
**Bien que répondant déjà à certaines questions critiques, le modèle pourrait être étendu notamment en ajoutant des commandes de tables non remplies, ou en accentuant l'aléatoire via une affluence variable.**


Ensuite actuellement la valeur des temps d'attente est parfois tributaire de la puissance de calcul de la machine sur laquelle se déroule la simulation. En effet, à saturation, l'estimation peut être faussée.

**Bien que le prétexte initial de ce projet ait été évidemment de travailler sur une simulation de système dynamique et l’utilisation de nouvelles connaissances, l’idée en tant que telle d'optimiser un restaurant en fonction de certains critères donnés et de variables pourrait présenter une finalité intéressante comme l’optimisation d’un restaurant ou l'estimation des besoins en terme de personnel lors d’une création d’enseigne.**

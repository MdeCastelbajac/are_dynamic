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

**Voici les problématiques que nous nous sommes posées:**

**- Quel est l’impact du nombre de serveurs sur le TAM?
  - Est il proportionnel, ou autre?**
**- Existe t il un nombre de serveurs optimal, ou à partir duquel celui-ci n’a plus d’effet significatif sur le TAM?**

**- Quel est l’impact de la carte sur le TAM?:
  - Selon la variance des temps de cuisson.**
**- Selon le nombre de choix.**
 
## Retour sur une description générale du modèle.
 Nous décomposerons le modèle que nous avons construit selon trois aspects distincts : 
 
 - D'une part, les **paramètres** :
  
   <strong>L'affluence des clients</strong> qui est fixe et maximale. Dès que les conditions sont réunies - une table est     libre et un serveur est prêt à les accueillir - les clients arrivent.
  
   <strong>La carte des plats</strong> qui à chaque plat associe un temps de cuisson ou de préparation unique.
    
       
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
    
  
   <strong>La cuisine</strong> qui prépare les plats commandés de telle façon à ce que les plats commandés à une même table  soient prêts en même temps.
  
- D'autre part, les **agents **: 
 
  les <strong>tables</strong> de quatre qui une fois remplies, commandent aléatoirement des plats parmi ceux proposés dans la  carte. Elles peuvent alors appeler un serveur qui vient prendre la comande. Une fois celle-ci reçu, elles se vident après une durée fixe.
  
  les <strong>serveurs</strong> qui peuvent, dans cet ordre de priorité : accueillir de nouveaux cients, servir les plats, prendre les commandes, les transmettre à la cuisine ou être inactif.
 
- Enfin, la **variable calculée** : 
  
  Le <strong>temps d'attente moyen</strong>, noté <strong>TAM</strong> qui représente le temps moyen qu'attendent les clients entre leur arrivée et leur départ du restaurant. Plus exactement, le temps attendu entre l'arrivée et le passage de la commande, et le temps attendu entre le passage de la commande et l'arrivée des plats.
  
## Description du modèle à l'échelle micro.
Rappelons que nous utilisons la bibliothèque TKinter pour la gestion graphique de la simulation.
Revenons ici sur les actions et intéractions des agents à une plus grande échelle. 

#### La classe Table : 


    class Table:

    #initialization
    def __init__(self, room, image, coords, number, fullcapacity, degust, timer, timer_debut_action, timer_fin_action):
        self.room = room
        self.img = self.room.create_image(coords[0], coords[1], image = table_vide)
        self.image = image
        self.number = number # The table's number is necessary to register orders and deliver dishes at the right place
        self.coords = coords # The table's coords : same necessity
        self.fullcapacity = fullcapacity # How many clients are needed to fill the table
        self.capacity = 0 # How many clients are currently sitting there
        self.order = [] # The clients randomly chose dishes in the MENU
        param.tables[self.number] = 0 # Table's state for other agents
        self.degust = False #clients are eating
 
 
Il faut bien comprendre que chaque table suit une liste d'actions prédéfinie et toujours dans le même ordre, via une fonction main. 
Quel intérêt alors ? Il est double. D'une part, le programme ne comprend pas, autrement que par l'illustration, la notion de client. Toutes les actions qu'on imputerait à ces derniers sont en fait effectuées par les tables - *comme le choix des plats* -. Cela nous permet de réunir plus d'information autour d'une même instance d'objet. D'autre part, elles seules sont à même de mesurer le temps d'attente comme nous le vérifierons plus tard.


#### La classe serveur

La classe Serveur est un peu plus compliquée à mettre en place. Pour cause, chaque instance doit être gérée sur deux plans différents de façon plus poussée. Jusqu'ici, nous n'avons pas beaucoup parlé de simulation. On présentera donc leur fonctionnement à la fois dans le modèle et dans la simulation.

Le code relatif se révélant un peu touffu, on se bornera à prendre quelques exemples.

Au coeur de la simulation, on retrouve les fonctions de déplacement que l'on explicitera :   
    
   
    def movement_x(self, x_dir): # Those parameters are conditional, they indicate which direction
    # the waiter takes
        if x_dir > 0 and x_dir != 0:
            room.delete(self.img)
            self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_left)
            root.update_idletasks()
            root.update()
            self.room.move(self.img, -5, 0)
        elif x_dir !=0:
            room.delete(self.img)
            self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_right)
            root.update_idletasks()
            root.update()
            self.room.move(self.img, 5, 0)
        self.coords = self.room.coords(self.img)
   
   
   
 En effet, plusieurs fonctions font appel aux déplacements : 
 
    
     
    def go_to_kitchen(self):
        if self.coords[1] != koords[1]:
            y_dir = self.coords[1] - koords[1]
            root.after(10, self.movement_y(y_dir))
        elif self.coords[0] != koords[0]: # The waiter goes back to the kitchens to give the order he collected
            x_dir = self.coords[0] - koords[0]
            root.after(10, self.movement_x(x_dir))
        else:
            self.waiting = True
        


Tout comme pour les tables, on a aussi une fonction main, qui, en fonction des conditions propres aux serveurs, et des appels respectifs de la cuisine et des tables, ordonne au serveur d'effectuer une certaine tâche.



#### Calcul du TAM

De nouveau dans la classe Table : 



        # TAM calculation
        self.timer = 0.0 
        self.timer_debut_action = 0.0
        self.timer_fin_action = 0.0



A chaque début d'attente, on lance un timer. A chaque fin d'attente on lance un nouveau timer. Il ne reste plus qu'à prendre la différence des deux et on obtient un temps d'attente pour une table. De plus, a chaque "tour" de cuisson, on incrémente cette valeur à hauteur du temps de cuisson écoulé *des plats de cette table*. Le résultat qui nous intéresse est simplement la moyenne de toutes ces valeurs récupérées, le TAM.

#### Fonctionnement du programme 

L'exécution du programme passe par plusieurs étapes.

Tout d'abord, on doit initialiser graphiquement la fenêtre en fonction des paramètres choisis : 
    
     
    for i in range(1, nb_serv+1):
    exec("%s = %s" % ('waiter'+str(i),'Waiter(i, room, [300,300+100*i])'))
    

Ensuite, on rentre dans une boucle, qui exécute successivement les fonctions main des classes Tables et Serveurs.


## Expériences et Exploitation des résultats

#### Protocole 1
Nous commencerons par observer **l'influence du nombre de serveur**.



Rappelons ici les questions que nous nous posions au début du projet : 
   - Existe-t-il, d'une part, un nombre de serveur qui permet d'obtenir un **TAM optimal**? et, par suite, un nombre de serveur au-delà duquel le TAM ne diminue plus?


Il convient tout d'abord d'isoler le paramètre **nombre de serveurs**. On fixe alors tous les autres paramètres. Pour toutes nos expériences on fixe le nombre de table à **8**, et la carte au modèle présenté ci-dessus.

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

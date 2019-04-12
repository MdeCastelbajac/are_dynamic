## Introduction
 Le but de ce projet est de modéliser et de simuler l'activité d'un (petit) restaurant avec Python. Si notre travail peut être relié à des ABM préexistants, ([]()) nous avons souhaité rester le plus autonome possible en construisant de A à Z le modèle, la simulation (oui, même les dessins) et le présent site. Le choix de la programmation orientée objet s'est rapidement imposé. 
 
 
 Depuis la première présentation, il y a eu quelques changements, des déconvenues aussi - mais nous y reviendrons - et, bien sûr, les forums de programmation comme StackOverflow ont été nos meilleurs amis. Nous vous présentons donc aujourd'hui le projet dans sa version finale, les expériences que nous avons pu mener ainsi que les résultats que nous avons pu exploiter.
Enfin, nous reviendrons sur les améliorations qu'il reste à apporter au projet.
 
## Retour sur une description générale du modèle.
 Nous décomposerons le modèle que nous avons construit selon trois aspects distincts : 
 
 - D'une part, les paramètres :
  
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
  
- D'autre part, les agents : 
 
  les <strong>tables</strong> de quatre qui une fois remplie, commande aléatoirement des plats parmi ceux proposés dans la  carte. Elles peuvent alors appeler un serveur qui vient prendre la comande. Une fois celle-ci reçu, elle se vident après une durée fixe.
  
  les <strong>serveurs</strong> qui peuvent, dans cet ordre de priorités : accueillir de nouveau cients, servir les plats, prendre les commandes, les transmettre à la cuisine ou être inactif.
 
- Enfin, la variable calculée : 
  
  Le <strong>temps d'attente moyen</strong>, noté <strong>TAM</strong> qui représente le temps qu'attendent les clients entre leur arrivée et leur départ du restaurant. Plus exactement, le temps attendu entre l'arrivée et le passage de la commande, et le temps attendu entre le passage de la commande et l'arrivée des plats.
  
## Description du modèle à l'échelle micro.
Revenons ici sur les actions et intéractions des agents à une plus grande échelle. 

#### La classe Table : (on commentera directement le code)


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
Quel intérêt alors ? Il est double. D'une part, le programme ne comprend pas, autrement que par l'illustration, la notion de client. Toutes les actions qu'on imputerait à ces derniers sont en fait effectuées par les tables - *comme le choix des plats* -. Cela nous permet de réunir plus d'information autour d'une même instance d'objet. D'autre part, elles seules sont à même de mesurer le temps d'attente comme nous allons justement le vérifier.


#### Calcul du TAM

Toujours dans la classe Table : 



        # TAM calculation
        self.timer = 0.0 
        self.timer_debut_action = 0.0
        self.timer_fin_action = 0.0



A chaque début d'attente, on lance un timer. A chaque fin d'attente on lance un nouveau timer. Il ne reste plus qu'à prendre la différence des deux et on obtient un temps d'attente pour une table. Le résultat qui nous intéresse est simplement la moyenne de toutes ces valeurs récupérées, le TAM.


#### La classe serveur

La classe Serveur est un peu plus compliquée à mettre en place. Pour cause, chaque instance doit être gérée sur deux plans différents de façon plus poussée. Jusqu'ici, nous n'avons pas beaucoup parlé simulation. On présentera donc leur fonctionnement à la fois dans le modèle et dans la simulation.

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


#### Fonctionnement du programme 

L'exécution du programme passe par plusieurs étapes.

Tout d'abord, on doit initialiser graphiquement la fenêtre en fonction des paramètres choisis. On utilise donc la bibliothèque TKinter : 
    
     
    for i in range(1, nb_serv+1):
    exec("%s = %s" % ('waiter'+str(i),'Waiter(i, room, [300,300+100*i])'))
    

Ensuite, on rentre dans une boucle, qui exécute successivement les fonctions main des classes Tables et Serveurs.


## Expériences et Exploitation des résultats

#### Protocole 1
Nous commencerons par observer l'influence du nombre de serveur.

A titre indicatif : (insérere le premier graphe).


Il convient tout d'abord d'isoler le nombre de serveurs. On fixe alors tous les autres. Pour toutes nos expériences on fixe le nombre de table à 8, et la carte au modèle présenté ci-dessus.
Ensuite, pour un nombre de serveur variant de 1 à 8, on récupère les 50 premières valeurs du TAM, un nombre qui paraît suffisament grand compte tenu de l'influence qu'auront les choix de plats aléatoires sur celles-ci. L'intervalle du nombre de serveur s'explique facilement par le fait qu'au-delà de huit, il y a toujours un ou plusieurs serveurs qui sont inactifs, du fait du nombre de table préalablement fixé.


Rappelons ici les questions que nous nous posions au début du projet : 
   - Existe-t-il, d'une part, un nombre de serveur qui permet d'obtenir un TAM optimal ? et, par suite, un nombre de serveur au-delà duquel le TAM ne diminue plus?

#### Résultats
On construit par la suite le graphe suivant duquel on peut déduire plusieurs affirmations intéressantes :


#### Protocole 2 
Nous observerons ici l'influence de la carte, de part sa taille, et de part la variance des temps de cuisson.
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
    
    
  S'il on veut obtenir des résultats exploitables, il nous faut utiliser seulement des cartes ayant une même moyenne de temps de cuisson.
  
  On commence donc par calculer simplement la moyenne et la variance des temps de cuisson de cette carte, qui servira de référence pour la suite de l'expérience.
  
  
    Moyenne = 17.44
  
    Variance = 46.44
  
  
 On gardera le même nombre de table, et on fixera le nombre de serveurs à (nb_TAM_optimal).
 
 Dans un premier temps, on réduit puis augmente la taille de la carte, de telle façon à ce qu'elle conserve sa moyenne, et on récupère les valeurs du TAM selon la même procédure que précédemment.

Voici les deux cartes obtenues après modifications : 

taille+ : 




taille- :
 
 On construit avec ces données le graphe suivant : 
 
 
 
 



Dans un second temps, on s'occupe de la variance, qu'on s'emploie à augmenter, puis à diminuer.
On procèdera encore une fois de la même façon.
  
variance + : 



variance - :



On construit avec ces données le graphe suivant : 
 




## Conclusion et dernières réflexions 











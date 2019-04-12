
## Retour sur une description générale du modèle.
 Nous décomposerons le modèle que nous avons construit selon trois aspects distincts : 
 
 - D'une part, les paramètres :
  
   <strong>L'affluence des clients</strong> qui est fixe et maximale. Dès que les conditions sont réunies - une table est     libre et un serveur est prêt à les accueillir - les clients arrivent.
  
   <strong>La carte des plats</strong> qui à chaque plat associe un temps de cuisson ou de préparation unique.
  
   <strong>La cuisine</strong> qui prépare les plats commandés de telle façon à ce que les plats commandés à une même table  soient prêts en même temps.
  
- D'autre part, les agents : 
 
  les <strong>tables</strong> de quatre qui une fois remplie, commande aléatoirement des plats parmi ceux proposés dans la  carte. Elles peuvent alors appeler un serveur qui vient prendre la comande. Une fois celle-ci reçu, elle se vident après une durée fixe.
  
  les <strong>serveurs</strong> qui peuvent, dans cet ordre de priorités : accueillir de nouveau cients, servir les plats, prendre les commandes, les transmettre à la cuisine ou être inactif.
 
- Enfin, la variable calculée : 
  
  Le <strong>temps d'attente moyen</strong>, noté <strong>TAM</strong> qui représente le temps qu'attendent les clients entre leur arrivée et leur départ du restaurant. Plus exactement, le temps attendu entre l'arrivée et le passage de la commande, et le temps attendu entre le passage de la commande et l'arrivée des plats.
  
## Description du modèle à l'échelle micro.
Revenons ici sur les actions et intéractions des agents à une plus grande échelle. 

#### La classe Table : (on commentera directement le code)

"""
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
 """
 
Il faut bien comprendre que chaque table suit une liste d'actions prédéfinie et toujours dans le même ordre. 
Quel intérêt alors ? Il est double. D'une part, le programme ne comprend pas, autrement que par l'illustration, la notion de client. Toutes les actions qu'on imputerait à ces derniers sont en fait effectuées par les tables - *comme le choix des plats* -. Cela nous permet de réunir plus d'information autour d'une même instance d'objet. D'autre part, elles seules sont à même de mesurer le temps d'attente comme nous allons justement le vérifier.


#### Calcul du TAM

Toujours dans la classe Table : 

"""
# TAM calculation
 self.timer = 0.0 
 self.timer_debut_action = 0.0
 self.timer_fin_action = 0.0
"""




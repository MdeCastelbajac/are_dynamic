
# Retour sur une description générale du modèle.
 Nous décomposerons le modèle que nous avons construit selon trois aspects distincts : 
 -D'une part, les paramètres :
  -- <strong>L'affluence des clients</strong> qui est fixe et maximale. Dès que les conditions sont réunies - une table est libre et un serveur est prêt à les accueillir - les clients arrivent.
  -- <strong>La carte des plats</strong> qui à chaque plat associe un temps de cuisson ou de préparation unique.
  -- <strong>La cuisine</strong> qui prépare les plats commandés de telle façon à ce que les plats commandés à une même table soient prêts en même temps.
 -D'autre part, les agents : 
  -- les <strong>tables</strong> de quatre qui une fois remplie, commande aléatoirement des plats parmi ceux proposés dans la carte. Elles peuvent alors appeler un serveur qui vient prendre la comande. Une fois celle-ci reçu, elle se vident après une durée fixe.
  -- les <strong>serveurs</strong> qui peuvent, dans cet ordre de priorités : accueillir de nouveau cients, servir les plats, prendre les commandes, les transmettre à la cuisine ou être inactif.
  Enfin, la variable calculée : 
  -- Le <strong>temps d'attente moyen</strong>, noté <strong>TAM</strong> qui représente le temps qu'attendent les clients entre leur arrivée et leur départ du restaurant. Plus exactement, le temps attendu entre l'arrivée et le passage de la commande, et le temps attendu entre le passage de la commande et l'arrivée des plats.
  
# Description du modèle à l'échelle micro.

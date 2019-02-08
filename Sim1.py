

     #####   #####   ######   #######   #####    #   #    ######
     #   #   #       #           #      #   #    #   #    #    #
     #####   ####    ######      #      #####    #   #    ######
     # #     #            #      #      #   #    #   #    # #
     #  #    #####   ######      #      #   #    #####    #  #

# Nous tenterons ici de modéliser un restaurant en action comprenant :
# des serveurs, des tables, des clients.
# Une fois les tables remplies (2 ou 4 personnes pour faire simple),
# les clients peuvent commander parmi une sélection de plats et d'entrées et/ou de menus
# (nous écarterons les desserts pour le moment). Chaque plat / entrée possède un temps de
# préparation propre (ou de cuisson).
#
# Nous nous demanderons dans le cadre de cette simulation, étant donné une certaine taille
# de restaurant (nombre de tables), quel nombre de serveur serait minimal pour assurer un
# service de qualité.

Carte = dict[str : float]
#Plats : Carte
Plats = { "Assiette végétarienne" : 10.30,
          "Poulet fermier et pommes grenades" : 25.00,
          "N'importe quoi" : 18.30}
#Entrees : Carte
Entrees = { "Salade fermière" : 10.00,
            "Assiette de fromage" : 5.20,
            "Thonmate -Spécialité du chef-"" : 12.00}

def Clients():
    "génère un nombre aléatoire de clients entre 1 et 4"
    #nb_clients : int
    nb_clients = randint(1,4)
    return nb_clients

def Table_2(n):
    """
    int-> dict[int : tuple[int, bool]]
    Tables pour 2 clients."""
    table_2 = {i : (0, False) for i in range(1, n+1)}
    return table_2

def Table_4(n):
    """
    int-> dict[int : tuple[int, bool]]
    Tables pour 4 clients."""
    table_4 = {i : (0, False) for i in range(1, n+1)}
    return table_4

def Remplissage():
    """Rempli les 2n tables avec les clients arrivés."""
    clients = Clients()

    if clients > 2:       # Ils cherchent une table de 4.
        for (j, (nb, full)) in Table_4.items():
            if (not(full)) and (nb + clients <= 4):
                nb += clients
                if nb == 4:
                    full = True
                return Table_4 # Ils ont trouvé une table

    # Créer une file d'attente

    else : #Ils cherchent en priorité une table de 2, mais peuvent remplir une table de 4 s'il n'y a plus de place.
        for (j, (nb,full)) in Table_2.items():
            if (not(full)) and (nb + clients <= 2):
                nb += clients
                if nb == 2:
                    full = True
                return Table_2    # S'ils ne trouvent pas de place à la fin de la boucle, ils regardent pour les tables de 4.
        for i in range(1, len(Table_4)+1):
            for (i, (nb, full)) in Table_4.items():
                if (not(full)) and (nb + clients <= 4):
                    nb += clients
                    if nb == 4:
                        full = True
                return Table_4

def mise_a_jour():
    """ Mets à jour la liste des tables pleines."""

    for (i,(nb, full)) in Table_4.items():
        if full and T4full[i]!="en attente" #Si la table n'a pas encore commandé
            T4full[i] = "prêt à commander"
    for (i,(nb, full)) in Table_2.items():
        if full and T2full[i] != "en attente":
            T2full[i] = "prêt à commander"

def Commande(menu):
    """ Une table remplie peut passer commande"""

    #Les deux dictionnaires Commande2 et Commande4 répertorient une liste de commandes par numéro de table, respectivement
    #pour 2 et 4 personnes.

    for i in T4full:
        if T4full[i] == "prêt à commander":
            for j in range(4):
                Commande4[i].append(choice(Entree))
                Commande4[i].append(choice(Plats))
            T4full[i] == "en attente"
    for i in T2full:
        if T2full[i] == "prêt à commander":
            for j in range(2):
                Commande2[i].append(choice(Entree))
                Commande2[i].append(choice(Plats))
            T2full[i] == "en attente"
    return (Commande4, Commande2)

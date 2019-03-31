

# On peut pas itérer sur un dict et modifier sa taille en même temps, donc je fais une copie supprime
# laquelle j'itère, puis je modifie to_be_cooked, tu as besoin d'import copy par contre.
import copy


def check_ready():
    """ vérifie si la commande d'une table est prête. Si oui, alors elle donne elle appelle le serveur et supprime les timers
    et les plats de ses listes to_be_cooked et cooking"""

    Dtemp = copy.deepcopy(to_be_cooked)
    for i in Dtemp:
        for tupl in cooking:
            if tupl[0] == i:
                if not(tupl[1] <= 0.0):
                    return None # Si non
        indice = i
        # Si oui
        cooked.append(i)
        for indice in to_be_cooked:
            for tupl in cooking:
                if tupl[0] == indice :
                    cooking.remove(tupl)
        del to_be_cooked[indice]
        # On clear toute la commande des deux listes et dictionnaires

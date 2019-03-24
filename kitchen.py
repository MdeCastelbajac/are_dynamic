
import random
import time
from tkinter import *

class Furnace: # On créé x (fixe) instances de 'fours' qui ne peuvent cuir qu'un seul plat simultanément

     to_be_cooked = {} #Dictionnaire rempli par les serveur
     cooking = []

     def __init__(self, num, case, filled, aside):

         self.num = num # Pour repérer les fours
         self.case = (0,0.0)  # Plat dans le four (+ numéro de table)
         self.filled = False
         self.aside = [] # Liste de tuple de réserve
         #Param ...

    #def global_timer_per_table(self

     """ La difficulté est ici de gérer et d'entretenir la répartition des plats (sous forme de timers) appartenant
     différentes tables.
     L idée est donc ici de transformer le dictionnaire de départ to_be_cooked qui tri ces plats par numéro de table,
     en une liste de tuple (num_table, timer, pioché(ou pas)) dans laquelle les fours pourront piocher des plats selon qu'ils aient besoin
     d'un plat d'une table en particulier, ou au contraire, d'un timer court ou élevé peu importe la table. """

     def constr_list():

         k = 0 # indice de la nouvelle liste
         for i in to_be_cooked:
             for j in to_be_cooked[i]:
                 cooking[k] = (i, to_be_cooked[i][j]) # On forme des tuples num_table / timer
                 k += 1

     """ Une fois cette liste disponible, chaque four va pouvoir piocher un timer (et se remplir) et le diminuer seconde
     après seconde dans la liste avec une update.

     Exemple : On prend toujours le un four prend toujours le timer disponible le plus haut (dans sa réserve ou dans la liste)"""

     def cook(self):
         # On détermine le timer disponible le plus haut
         time_max = 0.0
         indice = 0
         for i in cooking:
             if cookind[i][1] > time_max and not(cooking[i][2]):
                 time_max = cooking[i][1]
                 indice = i

         if self.filled: # Le four est déjà plein
             if time_max > case[1]:
                 if self.aside == []: # La réserve est vide
                     self.aside = self.case
                     self.case = cooking[i]
                     cooking[i][2] = True # Le timer est pioché
             # Sinon on ne fait rien et on attend que les timers décroissent
         else: # Le four est vide
             self.case = cooking[i]
             cooking[i][2] = True # Le timer est pioché

         cooking[i][1] -= 1.0
         root.after(1000, tictoc()) # Après 1 seconde, on décrémente le timer d'une seconde

     def tictoc(self, i):
         """ fait baisser le timer présent dans un four"""
         self.case[1] -= 1.0

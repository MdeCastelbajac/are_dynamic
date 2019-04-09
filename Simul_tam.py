sudo pip install nose nosegae

import random
import time
from tkinter import *
import copy

#Room
root = Tk()
img_bg = PhotoImage(file = "C:\\Users\\Florian\\Pictures\\ARE_images\\rest_room_bg.gif")
room = Canvas(width = 600, height = 800)
instance_bg = room.create_image(300, 400, image = img_bg)
room.pack()

#Paramétrage
class Param: # Un ensemble de dictionnaires contenant l'état des objets
    def __init__(self):
        self.kitchen = {} #Etat des cuisines
        self.tables = {} #Etat des tables
        self.waiters = {} #Etat des serveurs


param = Param()
tstart = {} # Un dictionnaire contenant des temps de départ
time_now = time.time() # Le temps présent renouvelé à chaque étape
filled = [] # La liste des tables remplies
empty = [] # La liste des tables vides
command = [] # La liste des tables ayant passé commande
fill = 0 # Numéro de la table se remplissant (0 par défaut)
accueil = 0 # Etat de l'accueil des clients
pris = []

# MENU OF DISHES
MENU = {"Boeuf Bourguignon" : 35.30,
        "Spicy Burger" : 15.30,
        "Tartar" : 13.0,
        "Veggie Salad" : 10.30,
        "Veggie Burger": 14.30,
        "Ceasar Salad" : 12.30,
        "Bruceta" : 26.30,
        "Daily Pasta" : 13.30 }


total_time_per_table = 0.0
number_of_tables = 0
total_t_per_table = 0.0
n_of_tables = 0


def TAM(time):
    global total_time_per_table, number_of_tables
    total_time_per_table += time
    number_of_tables += 1
    print("TAM : ", total_time_per_table/number_of_tables)


def tam(time):
    global total_t_per_table, n_of_tables
    total_t_per_table += time
    n_of_tables += 1
    print("tam : ", total_t_per_table/n_of_tables)


#########################################################################################
#                                     K I T C H E N                                     #
#########################################################################################


#Kitchen entrance coordinates
koords = [300.0, 240.0]
entrance = [300.0, 720.0]

# Functions relative to kitchen's behavior

## We'll set three dictionnary to-be-cooked , cooking and cooked that will contain
## dishes and orders at these 3 stages. Waiter will bring order in the first one and take
## dishes in the last one, while in the cooking one, we'll set a timer which will take into
## account the cooking time of every dishes.

to_be_cooked ={} # Ce qui est à cuisiner
cooking = []
inside = []
cooked = [] # Ce qui est cuisiné


def constr_list():
    if to_be_cooked != {} or cooking == []:
        for i in to_be_cooked:
            if not i in inside:
                for j in to_be_cooked[i]:
                    cooking.append((i, j, False)) # On forme des tuples num_table / timer
                inside.append(i)


class Furnace: # On créé x (fixe) instances de 'fours' qui ne peuvent cuir qu'un seul plat simultanément

    def __init__(self, num):
        self.num = num # Pour repérer les fours
        self.case = (0,0.0)  # Plat dans le four (+ numéro de table)
        self.filled = False
        self.aside = () # Liste de tuple de réserve
        self.indice_case = 0 # Permet de garder en memoire l'emplacement du plat pioché dans cooking
        self.indice_aside = 0 # Permet de garder en memoire l'emplacement du plat en reserve dans cooking

    """ La difficulté est ici de gérer et d'entretenir la répartition des plats (sous forme de timers) appartenant
    différentes tables.
    L idée est donc ici de transformer le dictionnaire de départ to_be_cooked qui tri ces plats par numéro de table,
    en une liste de tuple (num_table, timer, pioché(ou pas)) dans laquelle les fours pourront piocher des plats selon qu'ils aient besoin
    d'un plat d'une table en particulier, ou au contraire, d'un timer court ou élevé peu importe la table. """

    """ Une fois cette liste disponible, chaque four va pouvoir piocher un timer (et se remplir) et le diminuer seconde
    après seconde dans la liste avec une update.
    Exemple : On prend toujours le un four prend toujours le timer disponible le plus haut (dans sa réserve ou dans la liste)"""


    def tictoc(self):
        """ fait baisser le timer présent dans un four"""
        if self.case != ():
            a,b,c = self.case
            self.case = (a,b-1.0,c)


    def cook(self):
        # On détermine le timer disponible le plus haut
        if cooking != []:
            time_max = 0.0
            indice = 0
            for i in range(len(cooking)):
                if cooking[i][1] > time_max and not(cooking[i][2]):
                    time_max = cooking[i][1]
                    indice = i
            if time_max > 0.0 :
                if self.filled: # Le four est déjà plein
                    if time_max > case[1]:
                        if self.aside == (): # La réserve est vide
                            self.aside = self.case
                            self.case = cooking[i]
                            self.indice_case = indice
                        # Sinon on ne fait rien et on attend que les timers décroissent
                else: # Le four est vide
                    if self.aside != ():
                        self.indice_case = self.indice_aside
                        self.case = self.aside
                        self.aside = ()
                    else:
                        self.case = cooking[indice]
                        self.indice_case = indice
                if self.case[1] <= 1.0:
                    if self.case[1] <= 0.0 : # La cuisson du plat correspondant est terminée
                        self.case = ()
                        (a,b,c) = cooking[indice]
                        cooking[indice] = (a,0.0,c)
                        # On vide le four mais on ne change pas la valeur de pioché, le plat est en quelque sorte mis de côté
                    else:
                        (a,b,c) = cooking[indice]
                        cooking[indice] = (a,0.0,c)
                        Furnace.tictoc(self)
                (a,b,c) = cooking[indice]
                cooking[indice] = (a,b-1,c)
            Furnace.check_ready()
            root.after(int(5/nb_cuis), Furnace.tictoc(self)) # Après 1 seconde, on décrémente le timer d'une seconde

        """ Je n'ai pas trouvé le moyen de limiter la durée de la réserve pour l'instant : à voir """


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


#########################################################################################
#                                     W A I T E R S                                     #
#########################################################################################


class Waiter:

    #Initialization
    def __init__(self, num, room, coords):
        self.num = num # Numéro du serveur
        self.room = room # Placement dans la salle
        self.img = self.room.create_image(coords[0], coords[1], image = waiter_down) # Création de l'image
        self.coords = coords # Waiter's real-time coords
        self.orders = {} # Waiter's list of orders
        self.delivery = 0 # waiter's list of delivery
        self.waiting = False # Si le serveur attend (indicateur)
        self.number = 0 # Numéro de la table cible
        param.waiters[self.num] = 0 # Etat du serveur


    def movement_x(self, x_dir): # Those parameters are conditional, they indicate which direction
    # the waiter takes
        if x_dir > 0 and x_dir != 0:
            self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_left)
            root.update_idletasks()
            root.update()
            self.room.move(self.img, -5, 0)
        elif x_dir !=0:
            self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_right)
            root.update_idletasks()
            root.update()
            self.room.move(self.img, 5, 0)
        self.coords = self.room.coords(self.img)
        root.update_idletasks()
        root.update()


    def movement_y(self, y_dir): # we update the waiter's image when the function starts
        if y_dir > 0:
            if self.coords[0] > 330 and self.coords[0] < 390:
                self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_up)
                self.room.move(self.img, 0, -5)
                root.update_idletasks()
                root.update()
                self.coords = self.room.coords(self.img)
            elif self.coords[0] <= 330:
                Waiter.movement_x(self, -1)
                root.update_idletasks()
                root.update()
            elif self.coords[0] >= 390:
                Waiter.movement_x(self, 1)
                root.update_idletasks()
                root.update()
        elif y_dir !=0 and self.coords[0] < 260 and self.coords[0] > 240:
                self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_down)
                self.room.move(self.img, 0, 5)
                root.update_idletasks()
                root.update()
                self.coords = self.room.coords(self.img)
        elif self.coords[0] >= 260 :
            Waiter.movement_x(self, 1)
            root.update_idletasks()
            root.update()
        elif self.coords[0] <= 240:
            Waiter.movement_x(self, -1)
            root.update_idletasks()
            root.update()


    def collect_order(self): # Waiter collects a filled table's order
        if not self.number in filled and not self.number in pris: # Si aucune table cible
            self.number = filled[0] # Prise pour cible de la table pleine depuis le plus de temps
            filled.remove(self.number)
            pris.append(self.number)
        if param.tables[self.number] == 2: # Si la table a commandé
            if (self.coords[1] != eval("%s" % "table"+str(self.number)).coords[1]):
                y_dir = self.coords[1] - eval("%s" % "table"+str(self.number)).coords[1]
                root.after(5, self.movement_y(y_dir))
            elif (self.coords[0] != eval("%s" % "table"+str(self.number)).coords[0]+((-1)**(self.number+1))*100):
                # The waiter must close out the distance before collecting the order
                x_dir = self.coords[0] - eval("%s" % "table"+str(self.number)).coords[0]+((-1)**(self.number))*100
                root.after(5, self.movement_x(x_dir))
                self.waiting = False # Confirmation de non-attente
            elif not self.waiting:
                self.waiting = True # Passage à l'attente
                tstart['w'+str(self.num)] = time.time() # Départ de la prise de commande
            else:
                if time_now - tstart['w'+str(self.num)] > 2.0000: # Prise de commande terminée
                    #Le serveur est arrivé, la table arrête d'attendre
                    exec("%s" % ("Table.update_timers(table"+str(self.number)+")"))
                    exec("%s" % ("Table.update_t(table"+str(self.number)+")"))
                    #La table commence a attendre :
                    exec("%s" % ("Table.update_timers(table"+str(self.number)+")"))
                    exec("%s" % ("Table.update_t(table"+str(self.number)+")"))
                    self.orders[self.number] = eval("%s" % "table"+str(self.number)).order # Waiter just takes the orders coming from the table that called him
                    self.waiting = False # Passage à la non-attente
                    pris.remove(self.number) # La table est transférée de la liste des remplies...
                    command.append(self.number) #... à  celles ayant passé commande
                    eval("%s" % "table"+str(self.number)).order = []
                    self.number = 0 # Annulation du ciblage de la table


    def go_to_entrance(self):
        if(self.coords[1] != entrance[1]):
            y_dir = self.coords[1] - entrance[1]
            root.after(5, self.movement_y(y_dir))
        elif(self.coords[0] != entrance[0]):
            x_dir = self.coords[0] - entrance[0]
            root.after(5, self.movement_x(x_dir))
        else:
            self.waiting = True


    def go_to_kitchen(self):
        if self.coords[1] != koords[1]:
            y_dir = self.coords[1] - koords[1]
            root.after(5, self.movement_y(y_dir))
        elif self.coords[0] != koords[0]: # The waiter goes back to the kitchens to give the order he collected
            x_dir = self.coords[0] - koords[0]
            root.after(5, self.movement_x(x_dir))
        else:
            self.waiting = True


    def transmit(self):
        if(self.coords == koords)and(self.orders!=[]): # Waiter's in the kitchen and has orders to transmit
            for i in self.orders: # Transmission des commandes
                k = [MENU[l] for l in self.orders[i]]
                to_be_cooked[i] = k
            self.orders = {} # Stockage des commandes vide
            self.waiting = False


    def pick_up(self):
        if not self.waiting:
            Waiter.go_to_kitchen(self)
        else:
            self.delivery = cooked[0] # Prise des plats
            cooked.remove(cooked[0])
            self.waiting = False


    def deliver(self):
        if self.delivery != 0: # Si le serveur transporte des plats
            self.number = self.delivery
        if (self.coords[1] != eval("%s" % "table"+str(self.number)).coords[1]):
            y_dir = self.coords[1] - eval("%s" % "table"+str(self.number)).coords[1]
            root.after(5, self.movement_y(y_dir))
        elif (self.coords[0] != eval("%s" % "table"+str(self.number)).coords[0]+((-1)**(self.number+1))*100): # The waiter must close out the distance before collecting the order
            x_dir = self.coords[0] - eval("%s" % "table"+str(self.number)).coords[0]+((-1)**(self.number))*100
            root.after(5, self.movement_x(x_dir))
        else:
            eval("%s" % "table"+str(self.number)).img = eval("%s" % "table"+str(self.number)).room.create_image(eval("%s" % "table"+str(self.number)).coords[0], eval("%s" % "table"+str(self.number)).coords[1], image = table_served)
            root.update_idletasks()
            root.update()
            # Les plats sont arrivés, la table arrête d'attendre
            exec("%s" % ("Table.update_timers(table"+str(self.number)+")"))
            exec("%s" % ("Table.update_t(table"+str(self.number)+")"))
            param.tables[self.number] = 3 # La table est servie
            self.delivery = 0 # Le serveur ne transporte rien
            self.number = 0


    def activity(self):
        global accueil
        if param.waiters[self.num] == 0 and empty != [] and accueil == 0:
            # Si le serveur est libre, que des tables sont libres et que personne ne s'occupe de l'entrée
            param.waiters[self.num] = 1
            accueil = 1 # Quelqu'un se dirige vers l'entrée
            Waiter.go_to_entrance(self)
        elif param.waiters[self.num] == 1 and empty != []: # Si le serveur se dirige vers l'entrée
            Waiter.go_to_entrance(self)
            if self.coords == entrance: # Le serveur est arrivé à l'entrée
                accueil = 2 # Quelqu'un accueille les clients
        elif param.waiters[self.num] == 1 and empty == []: # Si toutes les tables sont pleines
            param.waiters[self.num] = 0 # Le serveur devient inactif
            accueil = 0 # Personne ne s'occupe de l'entrée
        elif (param.waiters[self.num] == 3 and self.delivery == 0) or (param.waiters[self.num] == 5 and self.orders == {}):
            param.waiters[self.num] = 0
        elif (param.waiters[self.num] == 0 or param.waiters[self.num] == 2) and self.delivery == 0 and cooked != []:
            # Le serveur est disponible et des commandes sont prètes à être servies
            param.waiters[self.num] = 2 # Le serveur va chercher les plats
            Waiter.pick_up(self)
        elif param.waiters[self.num] == 2 and self.delivery != 0:
            param.waiters[self.num] = 3
            Waiter.deliver(self)
        elif param.waiters[self.num] == 3 and self.delivery != 0:
            # Le serveur a des plats en main
            Waiter.deliver(self)
        elif (param.waiters[self.num] == 0 or param.waiters[self.num] == 4) and (filled != [] or self.number in pris):
            # Le serveur est disponible et des tables peuvent commander
            param.waiters[self.num] = 4 # Le serveur va noter les commandes
            Waiter.collect_order(self)
        elif (param.waiters[self.num] == 5 and self.orders != {}) or (param.waiters[self.num] == 4 and filled == []):
            # Le serveur a pris des commandes
            param.waiters[self.num] = 5 # Le serveur les transmet aux cuisines
            Waiter.go_to_kitchen(self)
            Waiter.transmit(self)
        else:
            Waiter.go_to_center(self)


    def go_to_center(self):
        if(self.coords[1] != entrance[1] - 50*self.num):
            y_dir = self.coords[1] - entrance[1] + 50*self.num
            root.after(5, self.movement_y(y_dir))
        elif(self.coords[0] != entrance[0] - 10):
            x_dir = self.coords[0] - entrance[0] + 10
            root.after(5, self.movement_x(x_dir))
        else:
            self.waiting = True


#########################################################################################
#                                      T A B L E S                                      #
#########################################################################################


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
        param.tables[self.number] = 0 # Etat de la table
        self.degust = False # Si les clients mangent
        self.timer = 0.0
        self.timer_debut_action = 0.0
        self.timer_fin_action = 0.0
        self.t = 0
        self.t_debut_action = 0
        self.t_fin_action = 0


    def update_timers(self):
        # En fin d'action
        if self.timer_debut_action != 0.0:
            self.timer_fin_action = time.time()
            self.timer += self.timer_fin_action - self.timer_debut_action
            self.timer_debut_action = 0.0
        # En début d'action
        elif self.timer_debut_action == 0.0:
            self.timer_debut_action = time.time()


    def update_t(self):
        # En fin d'action
        if self.t_debut_action != 0:
            self.t_fin_action = t
            self.t += self.t_fin_action - self.t_debut_action
            self.t_debut_action = 0
        # En début d'action
        elif self.t_debut_action == 0:
            self.t_debut_action = t


    def filling(self):
        global time_now, fill
        # This way it works with both 4 and 2 chairs tables
        if fill == 0: # Si aucune table ne se remplit
            fill = self.number # La table se remplit
            tstart['t'+str(self.number)] = time.time() # Début du remplissage
        if fill == self.number:
            if self.capacity != self.fullcapacity : # Si la table n'est pas remplie
                if time_now - tstart['t'+str(self.number)] >= 1.000:
                    self.capacity += 1
                if self.capacity == 1:
                    self.img = self.room.create_image(self.coords[0], self.coords[1], image = table_1_client)
                    root.update_idletasks()
                    root.update()
                elif self.capacity == 2:
                    self.img = self.room.create_image(self.coords[0], self.coords[1], image = table_2_client)
                    root.update_idletasks()
                    root.update()
                elif self.capacity == 3:
                    self.img = self.room.create_image(self.coords[0], self.coords[1], image = table_3_client)
                    root.update_idletasks()
                    root.update()
                elif self.capacity == 4 :
                    self.img = self.room.create_image(self.coords[0], self.coords[1], image = table_4_client)
                    root.update_idletasks()
                    root.update()
                    filled.append(self.number) # La table est remplie
                    empty.remove(self.number) # La table n'est plus vide
                    param.tables[self.number] = 1
                    fill = 0


    def ordering(self): # Randomly choice a dishes within the MENU times clients
        if self.order == []:
            for i in range(self.fullcapacity):
                self.order.append(random.choice(list((MENU.keys()))))
        self.timer_debut_action = time.time()
        self.t_debut_action = t
        # En attente du serveur

    def main(self):
        global time_now
        if param.tables[self.number] == 0 and accueil == 2 and fill == 0:
            # Si la table est vide et qu'un serveur est à l'accueil
            Table.filling(self)
            param.tables[self.number] = 1
        elif param.tables[self.number] == 1 and self.number in empty: # La table se remplit
            Table.filling(self)
        elif param.tables[self.number] == 1 and (self.number in filled or self.number in pris): # La table est pleine
            Table.ordering(self)
            param.tables[self.number] = 2 # La table est prète à commander
        elif param.tables[self.number] == 3: # La table a été servie
            if not self.degust:
                tstart['d'+str(self.number)] = time.time()
                self.degust = True
            if time_now - tstart['d'+str(self.number)] > 15.000:
                param.tables[self.number] = 4 # Les clients ont fini de manger
                self.degust = False
                TAM(self.timer)
                self.timer = 0.0
                tam(self.t)
                self.t = 0
        elif param.tables[self.number] == 4:
            param.tables[self.number] = 0 # La table est vide
            self.capacity = 0
            empty.append(self.number)
            #command.remove(self.number) # La table n'a plus de commande
            self.img = self.room.create_image(self.coords[0], self.coords[1], image = table_vide)
            root.update_idletasks()
            root.update()


#########################################################################################
#                                     I M A G E S                                       #
#########################################################################################


table_vide = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\table_4.gif")
table_1_client = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\table_1_client.gif")
table_2_client = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\table_2_client.gif")
table_3_client = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\table_3_client.gif")
table_4_client = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\table_4_client.gif")
table_served = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\table_served.gif")

waiter_down = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\waiter_down.gif")
waiter_up = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\waiter_up.gif")
waiter_right = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\waiter_right.gif")
waiter_left = PhotoImage(file="C:\\Users\\Florian\\Pictures\\ARE_images\\waiter_left.gif")


#########################################################################################
#                                      R U N N I N G                                    #
#########################################################################################


# OUR AGENTS
# Our table
# Nombres de tables, serveurs et plans de cuisine
nb_tabl= 8
nb_serv= 2
nb_cuis= 8

# Gestion du temps
interval = 0.01 # Intervalle minimum de temps

for i in range(1, nb_tabl+1):
    if i%2 == 1:
        exec("%s = %s" % ('table'+str(i),'Table(room, table_vide, [100, 300+110*(i//2)], i, 4, False, 0.0,0.0,0.0)'))
    else:
        exec("%s = %s" % ('table'+str(i),'Table(room, table_vide, [490, 300+110*(i//2-1)], i, 4, False, 0.0, 0.0, 0.0)'))
    exec("empty.append(table"+str(i)+".number)")

for i in range(1, nb_serv+1):
    exec("%s = %s" % ('waiter'+str(i),'Waiter(i, room, [300,300+100*i])'))

for i in range(1, nb_cuis+1):
    exec("%s = %s" % ('furnace'+str(i),'Furnace(i)'))

root.update_idletasks()
root.update()


def fonc():
    global time_now, t
    tstart['sys'] = time.time() # Début de l'étape
    constr_list()
    for i in range(1, nb_tabl+1):
        exec("%s" % ("Table.main(table"+str(i)+")"))
    for i in range(1, nb_serv+1):
        exec("%s" % ("Waiter.activity(waiter"+str(i)+")"))
    for i in range(1, nb_cuis+1):
        exec("%s" % ("Furnace.cook(furnace"+str(i)+")"))
    t += 1
    while tstart['sys']+interval > time_now:
        time_now = time.time() # Temps actuel

t = 0
m = 0
while m < 1:
    fonc()


root.mainloop()

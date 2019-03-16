import random
import time
from tkinter import *


#Room


root = Tk()
img_bg = PhotoImage(file = "~/Downloads/rest_room_bg.gif")
room = Canvas(width = 600, height = 800)
instance_bg = room.create_image(300, 400, image = img_bg)
room.pack()


#Paramétrage


class Param: # Un ensemble de dictionnaires contenant l'état des objets

    def __init__(self):
        self.kitchen = {}
        self.tables = {}
        self.waiters = {}
        self.popup = {}

param = Param()

tstart = {} # Un dictionnaire contenant des temps de départ

time_now = time.time() # Le temps présent renouvelé à chaque étape

nb_pop = 0

interval = 0.1


# MENU OF DISHES

MENU = {"Boeuf Bourguignon" : 20.30,
        "Spicy Burger" : 15.30,
        "Tartar" : 13.0,
        "Veggie Salad" : 10.30,
        "Veggie Burger": 14.30,
        "Ceasar Salad" : 12.30,
        "Bruceta" : 16.30,
        "Daily Pasta" : 13.30 }


def popup_text(num, str, x, y):
    global nb_pop
    if not num in param.popup:
        param.popup[num] = (str, x, y)
        popup = room.create_text(x, y,font=('bold', '16'), text = str)
        root.update_idletasks()
        root.update()
        tstart['p'+str(num)] = time.time()
        nb_pop += 1
        if nb_pop > 1000:
            nb_pop = 1
    elif time_now - tstart['p'+str(num)] > 1.0:
        room.delete(popup)
        root.update_idletasks()
        root.update()
        del param.popup[num]


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


to_be_cooked ={} #comment
cooking = {}
cooked = {}


class worktop:

    def __init__(self, num):
        self.num = num
        self.to_be_cooked = {}
        self.cooking = {}
        self.cooked = {}
        self.time_max = 0.0
        param.kitchen[self.num] = 0


    def cook(self, waiter):
        if param.kitchen[self.num] == 0 and self.to_be_cooked != {}:# if there's something to be cooked and if the kitchen is able to cook it :
            for number in self.to_be_cooked: # for each table
                for order in self.to_be_cooked[number]:# for each ordered dishes
                    if order in MENU: # if it matches a dishes in the MENU
                        if number in self.cooking:
                            self.cooking[number].append(MENU[order]) # We keep track of the table's number and we had the info on the cooking time
                        else :
                            self.cooking[number] = [MENU[order]]
            param.kitchen[self.num] = 1

        # We just set a maximal cooking time wich will define the minimal latency for the clients on a specific table to enjoy their meal

        elif param.kitchen[self.num] == 1: # if cooking isn't empty
            for number in self.cooking:
                for cooking_time in self.cooking[number]: # for each cooking time per order
                    if cooking_time > self.time_max:
                        self.time_max = cooking_time
            tstart['c'+str(self.num)] = time.time()
            param.kitchen[num] = 2

            # Now cooking

        elif param.kitchen[self.num] == 2:
            if time_now - tstart['c'+str(self.num)] >= time_max:# Transforms minutes into seconds to go faster
                popup_text(nb_pop, "Done !", 300, 100)
                self.cooked = self.cooking
                self.cooking = {}
                Waiter.pick_up(waiter, self.cooked)
                Waiter.deliver(waiter)
                param.kitchen[self.num] = 0


#########################################################################################
#                                     W A I T E R S                                     #
#########################################################################################


class Waiter:

    #Initialization

    def __init__(self, room, orders, delivery, call):
        self.room = room
        self.image = PhotoImage(file = "~/Downloads/waiter_down.gif")
        self.img = self.room.create_image(300, 300, image = self.image)
        self.coords = self.room.coords(self.img) # Waiter's real-time coords
        self.orders = orders # Waiter's list of orders
        self.delivery = delivery # waiter's list of delivery
        self.call = call # Waiter is called wether by the kitchen or the tables


    def movement(self, x_dir, y_dir): # Those parameters are conditional, they indicate which direction

    # the waiter takes

        if x_dir > 0 and x_dir != 0:
            self.room.move(self.img, -5, 0)
        elif x_dir !=0:
            self.room.move(self.img, 5, 0)
        if y_dir > 0 and y_dir != 0:
            self.room.move(self.img, 0, -5)
        elif y_dir !=0 :
            self.room.move(self.img, 0, 5)
        self.coords = self.room.coords(self.img)
        root.update_idletasks()
        root.update()


    def collect_order(self, table): # Waiter collects a filled table's order

        while (self.coords[0] != self.call[1][0]+100 or self.coords[1] != self.call[1][1]+100): # The waiter must close out the distance before collecting the order
            x_dir = self.coords[0] - self.call[1][0]-100
            y_dir = self.coords[1] - self.call[1][1]-100
            root.after(20, self.movement(x_dir, y_dir))
        start_time = time.time()
        time_now = time.time()
        while time_now - start_time < 2.0000:
            time_now = time.time()
        self.orders = table.order # Waiter just takes the orders coming from the table that called him
        popup_text(nb_pop, "Order registered", self.coords[0], self.coords[1])


    def go_to_entrance(self):

        while(self.coords != entrance):
            x_dir = self.coords[0] - entrance[0]
            y_dir = self.coords[1] - entrance[1]
            root.after(20, self.movement(x_dir, y_dir))
        start_time = time.time()
        time_now = time.time()
        while time_now - start_time < 2.0:
            time_now = time.time()


    def go_to_kitchen(self):

        while self.coords != koords: # The waiter goes back to the kitchens to give the order he collected
            x_dir = self.coords[0] - koords[0]
            y_dir = self.coords[1] - koords[1]
            root.after(20, self.movement(x_dir, y_dir))


    def transmit(self):

        if(self.coords == koords)and(self.orders!=[]): # Waiter's in the kitchen and has orders to transmit
            table_number = [i for i in self.call]
            to_be_cooked[table_number[0]] = self.orders
            popup_text(nb_pop, (" To be cooked : ",to_be_cooked), 300, 100)


    def pick_up(self, cooked):

        Waiter.go_to_kitchen(self)
        self.delivery = cooked
        cooked = {}


    def deliver(self):

        if self.delivery != {}:
            while (self.coords[0] != self.call[1][0]+100 and self.coords[1] != self.call[1][1]+100): # The waiter must close out the distance before collecting the order
                x_dir = self.coords[0] - self.call[1][0]
                y_dir = self.coords[1] - self.call[1][1]
                root.after(20, self.movement(x_dir, y_dir))
            popup_text(nb_pop, "Enjoy your meal !", self.coords[0], self.coords[1])
            self.delivery = {}
            self.call = {}


#########################################################################################
#                                      T A B L E S                                      #
#########################################################################################


class Table:

    #initialization

    def __init__(self, room, number, fullcapacity, capacity, filled, order):

        self.room = room
        self.image = PhotoImage(file = "~/Downloads/table_4.gif")
        self.img = self.room.create_image(100, 270, image = self.image)
        self.number = number # The table's number is necessary to register orders and deliver dishes at the right place
        self.coords = self.room.coords(self.img) # The table's coords : same necessity
        self.fullcapacity = fullcapacity # How many clients are needed to fill the table
        self.capacity = capacity # How many clients are currently sitting there
        self.filled = filled # The table's filled with clients
        self.order = order # The clients randomly chose dishes in the MENU


    def filling(self,clients):

        # This way it works with both 4 and 2 chairs tables

        if self.capacity < self.fullcapacity:
            self.capacity += clients
        else:
            self.capacity = self.fullcapacity
            self.filled = True
            popup_text(nb_pop, "Ready to order !", self.coords[0], self.coords[1])


    def ordering(self): # Randomly choice a dishes within the MENU times clients

        if self.filled:
            for i in range(self.fullcapacity):
                self.order.append(random.choice(list((MENU.keys()))))
                print("New order : ", self.order[i])


    def calling(self, waiter):

        if (self.order != []) and (waiter.call == {}): # If the waiter can take the order...
            waiter.call[self.number] = self.coords # He'll registered the table's number and coords

            # Then , he'll have to move towards the table that called him

            Waiter.collect_order(waiter, self)


#########################################################################################
#                                      R U N N I N G                                    #
#########################################################################################


# OUR AGENTS

# Our table

nb_tabl=1
nb_serv=1

for i in range(1,nb_tabl+1):
    exec("%s = %d" % ('table'+str(i),Table(room, i, 4, 0, False, [])))

for i in range(1,nb_serv+1):
    exec("%s = %d" % ('serveur'+str(i),Waiter(room, [], [], dict(), dict())))

nb_clients = random.randint(1, 4)
root.update_idletasks()
root.update()

waiter1.go_to_entrance()
Table.filling(table1, nb_clients)
Table.ordering(table1)
print("waiter is coming...\n")
Table.calling(table1, waiter1)
Waiter.go_to_kitchen(waiter1)
waiter1.transmit()
cook(cooking, cooked, to_be_cooked, waiter1)


def fonc():
    global time_now
    tstart['sys'] = time.time()
    for i in param.popup:
        a, b, c = param.popup[i]
        popup_text(i, a, b, c)
    while tstart['sys']+interval > time_now:
        time_now = time.time()


root.mainloop()

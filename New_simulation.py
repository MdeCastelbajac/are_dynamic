import random
import time
from tkinter import *


#Room

root = Tk()
img_bg = PhotoImage(file = "C:\\Users\\Florian\\Pictures\\ARE_images\\rest_room_bg.gif")
room = Canvas(width = 600, height = 800)
instance_bg = room.create_image(300, 400, image = img_bg)
room.pack()


#Paramétrage

class Param: # Un ensemble de dictionnaires contenant l'état des objets
    def __init__(self):
        self.kitchen = {}
        self.tables = {}
        self.waiters = {}
        self.pop = {}

param = Param()
tstart = {} # Un dictionnaire contenant des temps de départ
time_now = time.time() # Le temps présent renouvelé à chaque étape
order_tab = {}
nb_pop = 1
filled = []
empty = []
command = []
fill = 0
accueil = 0


# MENU OF DISHES

MENU = {"Boeuf Bourguignon" : 20.30,
        "Spicy Burger" : 15.30,
        "Tartar" : 13.0,
        "Veggie Salad" : 10.30,
        "Veggie Burger": 14.30,
        "Ceasar Salad" : 12.30,
        "Bruceta" : 16.30,
        "Daily Pasta" : 13.30 }

def popup_text(num, st, x, y):
    global nb_pop
    if not num in param.pop:
        param.pop[num] = room.create_text(x, y,font=('bold', '16'), text = st)
        root.update_idletasks()
        root.update()
        tstart['p'+str(num)] = time.time()
        nb_pop += 1
        if nb_pop > 1000:
            nb_pop = 1


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


to_be_cooked ={}
cooked = {}


class Worktop:

    def __init__(self, num):
        self.num = num
        self.cooking = {}
        self.time_max = 0.0
        param.kitchen[self.num] = 0


    def cook(self):
        if param.kitchen[self.num] == 0 and to_be_cooked != {}:
            L = []
            for n in to_be_cooked:
                L.append(n)
                number = L[0]
            for order in to_be_cooked[number]:
                if order in MENU:
                    if number in self.cooking:
                        self.cooking[number].append(MENU[order])
                    else:
                        self.cooking[number] = [MENU[order]]
            param.kitchen[self.num] = 1
            del to_be_cooked[number]
        elif param.kitchen[self.num] == 1:
            for number in self.cooking:
                for cooking_time in self.cooking[number]:
                    if cooking_time > self.time_max:
                        self.time_max = cooking_time
            tstart['c'+str(self.num)] = time.time()
            popup_text(nb_pop, "Cooking started...", 300, 100)
            param.kitchen[num] = 2
        elif param.kitchen[self.num] == 2:
            if time_now - tstart['c'+str(self.num)] >= self.time_max:
                popup_text(nb_pop, "Done !", 300, 100)
                for number in self.cooking:
                    cooked[number] = self.cooking
                self.cooking = {}
                param.kitchen[self.num] = 0
                self.time_max = 0.0


#########################################################################################
#                                     W A I T E R S                                     #
#########################################################################################


class Waiter:

    #Initialization
    def __init__(self, num, room):
        self.num = num
        self.room = room
        self.img = self.room.create_image(300, 300, image = waiter_down)
        self.coords = self.room.coords(self.img) # Waiter's real-time coords
        self.orders = {} # Waiter's list of orders
        self.delivery = {} # waiter's list of delivery
        self.waiting = False
        self.number = 0
        param.waiters[self.num] = 0


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
            self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_up)
            self.room.move(self.img, 0, -5)
            root.update_idletasks()
            root.update()
            self.coords = self.room.coords(self.img)
        elif y_dir !=0:
            self.img = self.room.create_image(self.coords[0], self.coords[1], image = waiter_down)
            self.room.move(self.img, 0, 5)
            root.update_idletasks()
            root.update()
            self.coords = self.room.coords(self.img)


    def collect_order(self): # Waiter collects a filled table's order
        if self.number == 0:
            self.number = filled[0]
        exec("%s = %s" % ('table','table'+str(self.number)))
        if param.tables[self.number] == 2:
            if (self.coords[0] != table.coords[0]+100): # The waiter must close out the distance before collecting the order
                x_dir = self.coords[0] - table.coords[0]-100
                root.after(20, self.movement_x(x_dir))
            elif (self.coords[1] != table.coords[1]):
                y_dir = self.coords[1] - table.coords[1]
                root.after(20, self.movement_y(y_dir))
                self.waiting = False
            elif not self.waiting:
                self.waiting = True
                tstart['w'+str(self.num)] = time.time()
            else:
                if time_now - tstart['w'+str(self.num)] > 2.0000:
                    self.orders[self.number] = table.order # Waiter just takes the orders coming from the table that called him
                    popup_text(nb_pop, "Order registered", self.coords[0], self.coords[1])
                    self.waiting = False
                    filled.remove(self.number)
                    command.append(self.number)
                    self.number = 0
                    


    def go_to_entrance(self):
        if(self.coords[0] != entrance[0]):
            x_dir = self.coords[0] - entrance[0]
            root.after(20, self.movement_x(x_dir))
        elif(self.coords[1] != entrance[1]):
            y_dir = self.coords[1] - entrance[1]
            root.after(20, self.movement_y(y_dir))
        else:
            self.waiting = True


    def go_to_kitchen(self):
        if self.coords[0] != koords[0]: # The waiter goes back to the kitchens to give the order he collected
            x_dir = self.coords[0] - koords[0]
            root.after(20, self.movement_x(x_dir))
        elif self.coords[1] != koords[1]:
            y_dir = self.coords[1] - koords[1]
            root.after(20, self.movement_y(y_dir))
        else:
            self.waiting = True


    def transmit(self):
        if(self.coords == koords)and(self.orders!=[]): # Waiter's in the kitchen and has orders to transmit
            for i in self.orders:
                to_be_cooked[i] = self.orders[i]
            self.orders = {}
            self.waiting = False
            popup_text(nb_pop, (" To be cooked : ",to_be_cooked), 300, 100)


    def pick_up(self):
        if not self.waiting:
            Waiter.go_to_kitchen(self)
        else:
            number = cooked.keys()[0]
            self.delivery = cooked[number]
            del cooked[number]
            self.waiting = False


    def deliver(self):
        if self.delivery != {}:
            for number in self.delivery:
                exec("%s = %s" % ('table', 'table'+str(number)))
            if (self.coords[0] != table.coords[0]+100): # The waiter must close out the distance before collecting the order
                x_dir = self.coords[0] - table.coords[0]
                root.after(20, self.movement_x(x_dir))
            elif (self.coords[1] != table.coords[1]):
                y_dir = self.coords[1] - self.table.coords[1]
                root.after(20, self.movement_y(y_dir))
            else:
                popup_text(nb_pop, "Enjoy your meal !", self.coords[0], self.coords[1])
                table.img = table.room.create_image(table.coords[0], table.coords[1], image = table_served)
                param.tables[number] = 3
                self.delivery = {}


    def activity(self):
        global accueil
        if param.waiters[self.num] == 0 and empty != [] and accueil == 0:
            param.waiters[self.num] = 1
            accueil = 1
            Waiter.go_to_entrance(self)
        elif param.waiters[self.num] == 1 and empty != []:
            Waiter.go_to_entrance(self)
            if self.coords == entrance:
                accueil = 2
        elif param.waiters[self.num] == 1 and empty == []:
            param.waiters[self.num] = 0
            accueil = 0
        elif (param.waiters[self.num] == 3 and self.delivery == {}) or (param.waiters[self.num] == 5 and self.orders == {}):
            param.waiters[self.num] = 0
        elif (param.waiters[self.num] == 0 or param.waiters[self.num] == 2) and self.delivery == {} and cooked != {}:
            param.waiters[self.num] = 2
            Waiter.pick_up(self)
        elif (param.waiters[self.num] == 2 or param.waiters[self.num] == 3) and self.delivery != {}:
            param.waiters[self.num] = 3
            Waiter.deliver(self)
        elif (param.waiters[self.num] == 0 or param.waiters[self.num] == 4) and filled != []:
            param.waiters[self.num] = 4
            Waiter.collect_order(self)
        elif (param.waiters[self.num] == 5 and self.orders != {}) or (param.waiters[self.num] == 4 and filled == []):
            param.waiters[self.num] = 5
            Waiter.transmit(self)


#########################################################################################
#                                      T A B L E S                                      #
#########################################################################################


class Table:

    #initialization
    def __init__(self, room, image, number, fullcapacity):
        self.room = room
        self.img = self.room.create_image(100, 270, image = table_vide)
        self.image = image
        self.number = number # The table's number is necessary to register orders and deliver dishes at the right place
        self.coords = self.room.coords(self.img) # The table's coords : same necessity
        self.fullcapacity = fullcapacity # How many clients are needed to fill the table
        self.capacity = 0 # How many clients are currently sitting there
        self.order = [] # The clients randomly chose dishes in the MENU
        param.tables[self.number] = 0
        tstart['d'+str(self.number)] = 0


    def filling(self):
        global time_now, fill
        # This way it works with both 4 and 2 chairs tables
        if fill == 0:
            fill = self.number
            tstart['t'+str(self.number)] = time.time()
        if fill == self.number:
            if self.capacity != self.fullcapacity :
                if time_now - tstart['t'+str(self.number)] >= 0.500:
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
                    filled.append(self.number)
                    empty.remove(self.number)
                    popup_text(nb_pop, "Ready to order !", self.coords[0], self.coords[1])
                    param.tables[self.number] = 1
                    fill = 0


    def ordering(self): # Randomly choice a dishes within the MENU times clients
        if self.number in filled:
            for i in range(self.fullcapacity):
                self.order.append(random.choice(list((MENU.keys()))))
                print("New order : ", self.order[i])


    def main(self):
        global time_now
        if param.tables[self.number] == 0 and accueil == 2 and fill == 0:
            Table.filling(self)
            param.tables[self.number] = 1
        elif param.tables[self.number] == 1 and self.number in empty:
            Table.filling(self)
        elif param.tables[self.number] == 1 and self.number in filled:
            Table.ordering(self)
            param.tables[self.number] = 2
        elif param.tables[self.number] == 3:
            if tstart['d'+str(self.number)] == 0:
                tstart['d'+str(self.number)] = time.time
            if time_now - tstart['d'+str(self.number)] > 5.000:
                param.tables[self.number] = 4
                tstart['d'+str(self.number)] = 0
        elif param.tables[self.number] == 4:
            param.tables[self.number] = 0
            empty.append(self.number)
            command.remove(self.number)
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
nb_tabl= 1
nb_serv= 1
nb_cuis= 1
interval = 0.01
temps = 3000

for i in range(1, nb_tabl+1):
    exec("%s = %s = %s" % ('table','table'+str(i),'Table(room, table_vide, i, 4)'))
    empty.append(table.number)

for i in range(1, nb_serv+1):
    exec("%s = %s = %s" % ('waiter','waiter'+str(i),'Waiter(i, room)'))

for i in range(1, nb_cuis+1):
    exec("%s = %s = %s" % ('worktop','worktop'+str(i),'Worktop(i)'))

root.update_idletasks()
root.update()

def fonc():
    global time_now, param
    tstart['sys'] = time.time()
    if param.pop != []:
        for i in param.pop:
            if time_now - tstart['p'+str(i)] > 1.0:
                room.delete(param.pop[i])
                root.update_idletasks()
                root.update()
    for i in range(1, nb_tabl+1):
        exec("%s = %s" % ('table','table'+str(i)))
        Table.main(table)
    for i in range(1, nb_serv+1):
        exec("%s = %s" % ('waiter','waiter'+str(i)))
        Waiter.activity(waiter)
    for i in range(1, nb_cuis+1):
        exec("%s = %s" % ('worktop','worktop'+str(i)))
        Worktop.cook(worktop)
    while tstart['sys']+interval > time_now:
        time_now = time.time()

t=0
while t < temps:
    fonc()
    t+1


root.mainloop()

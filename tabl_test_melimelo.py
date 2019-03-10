import random

import time

from tkinter import *


#Fenetre = Tk()


# MENU OF DISHES

MENU = {"Boeuf Bourguignon" : 20.30,

        "Spicy Burger" : 15.30,

        "Tartar" : 13.0,

        "Veggie Salad" : 10.30,

        "Veggie Burger": 14.30,

        "Ceasar Salad" : 12.30,

        "Bruceta" : 16.30,

        "Daily Pasta" : 13.30 }



#########################################################################################

#                                     K I T C H E N                                     #

#########################################################################################



#Kitchen entrance coordinates

koords = [0,0]


# Functions relative to kitchen's behavior


## We'll set three dictionnary to-be-cooked , cooking and cooked that will contain

## dishes and orders at these 3 stages. Waiter will bring order in the first one and take

## dishes in the last one, while in the cooking one, we'll set a timer which will take into

## account the cooking time of every dishes.


to_be_cooked ={}

cooking = {}

cooked = {}

target = {} # Association between a waiter and a table


def cook(cooking, cooked, to_be_cooked, waiter):

    time_max = 0.0

    if cooking == {} and to_be_cooked != {}:# if there's something to be cooked and if the kitchen is able to cook it :

        for number in to_be_cooked: # for each table

            for order in to_be_cooked[number]:# for each ordered dishes

                if order in MENU:

                    if number in cooking:

                        cooking[number].append(MENU[order]) # We keep track of the table's number and we had the info on the cooking time

                    else :

                        cooking[number] = [MENU[order]]


    # We just set a maximal cooking time wich will define the minimal latency for the clients on a specific table to enjoy their meal

    if(cooking != {}): # if cooking isn't empty

        for number in cooking:

            for cooking_time in cooking[number]: # for each cooking time per order

                if cooking_time > time_max:

                    time_max = cooking_time

        # Now cooking


        print("Cooking started")

        print('Estimated remaining time : ', time_max,' minutes')

        start_time = time.time()

        time_now = time.time()

        i = 0

        while(time_now - start_time < time_max/10):# Transforms minutes into seconds to go faster

            time_now = time.time()

            i += 1

            if i%1000000 ==0:

                print("Près dans : ",time_max/10  - (time_now - start_time))

        print("\n C'est prêt !\n")

        cooked = cooking

        cooking = {}

        Waiter.pick_up(waiter, cooked)

        print("Waiter moves towards the table 1\n")

        Waiter.deliver(waiter)



#########################################################################################

#                                     W A I T E R S                                     #

#########################################################################################



class Waiter:


    #Initialization

    def __init__(self, coords, orders, delivery, call):

        self.coords = coords # Waiter's real-time coords

        self.orders = orders # Waiter's list of orders

        self.delivery = delivery # waiter's list of delivery

        self.call = call # Waiter is called wether by the kitchen or the tables


    def movement(self, x_dir, y_dir): # Those parameters are conditional, they indicate which direction

    # the waiter takes

        if x_dir > 0:

            self.coords[0] -= 1


        else :

            self.coords[0] += 1


        if y_dir > 0:

            self.coords[1] -= 1


        else :

            self.coords[1] += 1


    def collect_order(self, table): # Waiter collects a filled table's order


        while not(self.coords == self.call[1]): # The waiter must close out the distance before collecting the order

            x_dir = self.coords[0] - self.call[1][0]

            y_dir = self.coords[1] - self.call[1][1]

            Waiter.movement(self, x_dir, y_dir)


        self.orders = table.order # Waiter just takes the orders coming from the table that called him

        print("Your order is registered\n")


    def go_to_kitchen(self):

        print("waiter is moving towards the kitchen...\n")

        while not(self.coords == koords): # The waiter goes back to the kitchens to give the order he collected

            x_dir = self.coords[0] - koords[0]

            y_dir = self.coords[1] - koords[1]

            Waiter.movement(self, x_dir, y_dir)

        print("waiter is in the kitchen\n")


    def transmit(self):


        if(self.coords == koords)and(self.orders!=[]): # Waiter's in the kitchen and has orders to transmit

            table_number = [i for i in self.call]

            to_be_cooked[table_number[0]] = self.orders

        print(" To be cooked : ",to_be_cooked)


    def pick_up(self, cooked):

        Waiter.go_to_kitchen(self)

        self.delivery = cooked

        cooked = {}


    def deliver(self):

        if self.delivery != {}:

            while not(self.coords == self.call[1]): # The waiter must close out the distance before collecting the order

                x_dir = self.coords[0] - self.call[1][0]

                y_dir = self.coords[1] - self.call[1][1]

                Waiter.movement(self, x_dir, y_dir)

            print("Enjoy your meals \n")

            self.delivery = {}

            target[self].state = 2

            Waiter.go_to_kitchen(self)


    def clean(self, table, tip): # The waiter cleans the table

        if table.state == 3:

            while not(self.coords == self.call[1]): # The waiter must close out the distance before collecting the order

                x_dir = self.coords[0] - self.call[1][0]

                y_dir = self.coords[1] - self.call[1][1]

                Waiter.movement(self, x_dir, y_dir)

            print("Maybe a tip ?\n")

            table.state = 0

            if tip == 0:

                print("That's great !\n")

            else:

                print("Nothing... \n")

            self.call = {}

            Waiter.go_to_kitchen(self)



#########################################################################################

#                                      T A B L E S                                      #

#########################################################################################



class Table:

    #initialization

    def __init__(self, number, coords, fullcapacity, capacity, state, order):


        self.number = number # The table's number is necessary to register orders and deliver dishes at the right place

        self.coords = coords # The table's coords : same necessity

        self.fullcapacity = fullcapacity # How many clients are needed to fill the table

        self.capacity = capacity # How many clients are currently sitting there

        self.state = state # The table's filled with clients, empty or dirty

        self.order = order # The clients randomly chose dishes in the MENU


    def filling(self, clients):

        # This way it works with both 4 and 2 chairs tables

        while self.capacity < self.fullcapacity:

            self.capacity += clients

        if self.capacity >= self.fullcapacity:
            
            self.capacity = self.fullcapacity

            self.state = 1

            print("Table 1 is ready to order \n")


    def ordering(self): # Randomly choice a dishes within the MENU times clients


        if self.state == 1:

            for i in range(self.fullcapacity):

                self.order.append(random.choice(list((MENU.keys()))))

                print("New order : ", self.order[i])


    def calling(self, waiter):


        if (self.order != []) and (waiter.call == {}): # If the waiter can take the order...

            waiter.call[self.number] = self.coords # He'll registered the table's number and coords

            # Then, he'll have to move towards the table that called him

            Waiter.collect_order(waiter, self)

            target[waiter] = self


    def tasting(self, waiter): # Now, the clients can eat


        if self.state == 2:

            time_requisite = 1.0

            start_time = time.time()

            time_now = time.time()

            i = 0

            while(time_now - start_time < time_requisite):# No originality, just the time the client take to eat

                time_now = time.time()

                i += 1

                if i%1000000 ==0:

                    print("Fini dans : ",time_requisite  - (time_now - start_time))

            print("\n Les clients se sont régalés !\n")

            self.state = 3

            self.capacity = 0

            Tip = random.randint(0, 5) # Just a little more

            Waiter.clean(waiter, self, Tip)



#########################################################################################

#                                      R U N N I N G                                    #

#########################################################################################



# OUR AGENTS

# Our table


table_1 = Table(1, [100,100], 4, 0, 0, [])


waiter_1 = Waiter([0,0], [],dict(), dict())


Table.filling(table_1, random.randint(1,4))

Table.ordering(table_1)

print("waiter is coming...\n")

Table.calling(table_1, waiter_1)

Waiter.go_to_kitchen(waiter_1)

waiter_1.transmit()

cook(cooking, cooked, to_be_cooked, waiter_1)

Table.tasting(table_1, waiter_1)

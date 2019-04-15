# Optimisation of the waiting time in a restaurant

## Introduction

As part of the ARE Dynamic course at Sorbonne University we had to choose a Dynamic system to model in the semester’s time frame. It is a mean to use Mathematical and Computer programming notions on a specific subject.

After a few weeks of an introduction course on Python we had to choose a specific dynamic system to work on.

We had several ideas of simulations, like predator/prey systems, or road simulations, ...
As a group of four students, we finally chose the simulation of a restaurant which is a type of model called Agent Based Model, or ABM.
ABM is a pretty new concept initiated in 1971, made possible by new mathematical theories and new computer capabilities.
The idea behind an ABM, is to set rules at an individual level on each entity called autonomous agents, and then to analyze how their interactions result in system wide changes.

An ABM is defined on wikipedia as 

> a class of computational models for simulating the actions and interactions of autonomous agents with a view to assessing their effects on the system as a whole

This technique enables the possibility to analyze complex systems which we could not analyze before.
There are a lot of relatively significant work that have been done thanks to this technique! 
It has been used in biology with the analysis of the evolution of epidemics, or in business with the modelisation of logistics, in economics and social sciences, …

Specifically our ABM is about analyzing how the waiting time of the clients evolves in a restaurant according to different parameters. 

## Our Model and the parameters

The configuration of the restaurant:

- The number of tables of four people (which is a limitation of our model). Each table is filled by the clients affluence and then each tables books a dish randomly.
- The Menu with several choices and a variable cooking time for each dish
- The waiters who are among other tasks taking the orders, bringing them to the kitchen, and so on.
- The kitchen is dealing with the orders, and respecting some specific rules, like cooking each tables orders so that each table’s clients can begin to eat simultaneously. 

The result we are analyzing:

- The average client's waiting time which is the sum of the time spend for each action from the order of the dishes to the moment the clients begin to eat.

## The main goal

Our plan according to this model, is to determine and compare the average client waiting time, from the moment they are reaching their table to the moment they can begin to eat their meal.

The goal is to analyze how some parameters impact the average waiting time.

We are for example simulating how the number of choices in the menu impacts the waiting time, or how the variability of the dishes cooking times has an impact on the average waiting time.
We are also trying to grasp the way the number of waiters impact this waiting time. Is it proportional? Is there a critical number where adding even more waiters doesn’t impact the waiting time anymore? And so on!

## How it could be useful

In fact if we could determine the optimal workforce (Waiters/Cooks) needed for a specific restaurant configuration (Number of tables, and estimated client affluence), then this system could be used to streamline and optimize the workforce needed. This could save money, improve the client satisfaction, and facilitate the restaurants management.

## If you want to dive deeper in our project, please visit our Github site:
https://mdecastelbajac.github.io/are_dynamic

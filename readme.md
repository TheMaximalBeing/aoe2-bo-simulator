# **Age of Empires II - Build Order Simulator**

---

***Note: this tool is still very unfinished and lacks most civ bonuses and anything beyond castle age***

### *a tool for testing your custom build order*

With this tool you can answer the following:

- If I make XYZ adjustments to my favourite build order, will it be better?
- Is my completely new build order viable?
- Which civ bonuses are objectively the best (given a particular benchmark)?
- Which is the best time to get a certain tech?
- How many units can I expect at a given time, assuming flawless execution?

## *Goals*

- ability to set the civ and game start info (such as natural resources)
- ability to set techs, units and buildings for your BO
- ability to set villager numbers for you BO
- simulate villagers; including gathering, drop-offs, reassignment, etc
- simulate buildings and farm reseeds
- simulate correct gather rates, carry capacity and walking speed
  (including adjustments for techs and civ bonuses)
- simulate different food sources (boar, sheep, etc)
- properly account for all the civ bonuses
- detect when there is not enough stockpiled resources at any point in time for your BO
- detect when there is not enough natural resources for your BO
- detect when you will be housed
- detect when buildings are idle
- detect when the economy is imbalanced due to poor villager assignments
- detect when BO is viable

## *Limitations*

- no geometry / map locations; we use fixed walking distances to simulate reassignment
- no enemy attacks; no idle time; no garrisoned villagers
- no control of military units / attacking enemies
- villagers don't know what specific object they are targetting (but do know its type)
- assume all resources have a dropsite with a fixed distance 
  (you must manually add enough dropsites to ensure realism)
- assume there is no reassignment between the same resource (assume its all in 1 place)
- farm info is carried by the farmer
- all-farms are force reseeded (need to unassign farmer to prevent it)
- no cramming of villagers (assume that you distribute them properly)

## *Instructions*

*No knowledge of Python is required to get started*

1. Install Python (e.g. from python.org) and a suitable text editor such as VS code
2. open *gameStart.py* and select your civ. Adjust any other info there to your liking
3. Open *villNumbers.py* and see example 'villNumbers["FF-FLUSH"]'. Copy this
   and rename it. Change the vill numbers as desired and change 'activeVillNumbers'
  at the bottom of the file.
4. Open *buildOrder.py* and see example 'buildOrders["FF-FLUSH"]'. Copy this
   and rename it. Change the build order numbers as desired and change 'activeBuildOrder'
  at the bottom of the file.
5. Open *simulation.py* and find the 'simulation info' section. You can change simulation
   'endTime' here. The drop-off/and reassignment distances are also here, in case you 
   would like to change them.
6. Run the *simulation.py* file (if using VS code you can just press F5).

## *What do the results mean?*

- The results display the game state every 25 seconds. This includes:
  - game time MM:SS; civilian population; military population; population headroom; stockpiles
  - techs researches
  - units trained
  - buildings built
  - idle buildings - this displays idle time in seconds and as a percentage of total time
  - villager distribution (i.e. what villagers are gathering)
  - villager activities (percent time per task per villager type)
- The activities are as follows
  - build: building something (including walking to building)
  - gather: gathering resources
  - drop: dropping off resources or returning to camp
  - reassign: walking to resource for first time
  - reseed: reseeding farm
  - lure: luring boar

## *What do I look for?*

- Ensure that buildings, such as the town center, are not going idle. If they are, then
  adjust your build order before this happens so that you have enough resources. If 
  military buildings are going idle then consider delaying feudal age.
- Remaining res represents natural food resources on the map. If these go negative then 
  you have run out and haven't built enough farms for your villagers to transition to.
  You should reassign them elsewhere or build more farms.
- If stockpiles go too negative then you cannot afford something and should either delay
  it or adjust you villager numbers. A slightly negative stockpile might be ok if you
  manually drop off resources.
- If your economy is not balanced then change your villager numbers.
- If stockpiles are floating then consider going feudal faster or add more farms.
- Build enough houses so that the population headroom doesn't go negative

## *How do I adjust the build order?*

- Use the overwatch (on) request to keep training villagers/military continuously. Each
  request allows 1 more to be trained simultaneously. Use off to cancel 1 overwatch.
- You can use the place request to place a building. It is not recommended to use 
  overwatch for buildings as they may be blocked by units and built much later
  than ideal. If you cannot afford them then the problem is with your villager numbers
  or buying too much stuff.
- You can use the pending request to start researching techs. If the building that the 
  tech comes from is also training units then you should use overwatch instead (otherwise 
  the building will do multiple things at once). Overwatch will wait until the 
  building is free. For techs, overwatch will only get the item once.
  

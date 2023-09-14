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

1. Install Python (e.g. form python.org) and a suitable text editor such as VS code
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

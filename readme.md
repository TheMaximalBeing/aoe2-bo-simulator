# **Age of Empires II - Build Order Simulator**

---

## *Goals*

- ability to predict accurate expected float
- simulate correct gather rates
- simulate different resource types
- simulate reassigning between different resources/town-center
- simulate drop offs
- simulate carry res properly
- simulate limited resources
- simulate 1 vill per farm
- ability to see stockpiles over whole game
- ability to detect if BO is viable
- ability to add whatever we want at a particular time and see the resoures
- ability to enforce limited resources and tech-tree prerequisites when desired (or ignore them)


## *Limitations*

- no geometry / map locations; we use fixed walking times to simulate reassignment
- no town under attack
- no control of military units
- no villager idle time in general
- villagers don't know what specific object they are targetting (but do know its type)
- assume all resources have a dropsie with a fixed distance (you must manually add enough dropsites to ensure realism)
- assume there is no reassignment between the same resource (assume its all in 1 place)
- farm info is carried by the farmer
- all-farms are force reseeded (need to unassign farmer to prevent it)
- food vills follow a fixed priority order: farms->boar->deer->sheep->fish->forage
- no cramming of villagers (Assume that you distribute them properly)
- 1 builder per building


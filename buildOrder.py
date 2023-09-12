from utils import *

buildOrders = { }

# format: [ [MM.SS, name, request] ]

# these check (see below):
# (a) if train site is avaliable
# (b) if enough resources
# (c) if pre-requisites are met

# request types:
# done    -> add to done list (none)
# place   -> add to placement list (a,c); buildings only; a is irrelevant here
# pending -> add to pending list (a,c)
# on      -> add to overwatch list (a,b,c)
# off     -> remove from overwatch list (a,b,c)

# all will consume resources (no free stuff)

buildOrders["FF-FLUSH"] =  [

  # houses (16 = 85 pop)
  [0.00, "house", "place"],
  [0.00, "house", "place"],
  [3.00, "house", "place"],
  [5.00, "house", "place"],
  [7.00, "house", "place"],
  [11.25, "house", "place"],
  [11.40, "house", "place"],
  [12.10, "house", "place"],
  [13.05, "house", "place"],
  [13.30, "house", "place"],
  [14.00, "house", "place"],
  [15.00, "house", "place"],
  [15.20, "house", "place"],
  [17.40, "house", "place"],
  [18.40, "house", "place"],
  [19.40, "house", "place"],

  # farms (20), should be 2 reseeds
  # [5.25, "farm", "place"],
  # [7.00, "farm", "place"],

  [11.15, "farm", "place"],
  # [11.30, "farm", "place"],
  # [11.55, "farm", "place"],
  [11.20, "farm", "place"],

  [11.40, "farm", "place"],
  [12.00, "farm", "place"],
  
  [12.40, "farm", "place"],
  [13.40, "farm", "place"],
  [14.50, "farm", "place"],
  [15.20, "farm", "place"],
  [16.05, "farm", "place"],
  [16.30, "farm", "place"],
  [16.45, "farm", "place"],


  [17.00, "farm", "place"],

  [18.00, "farm", "place"],
  [18.10, "farm", "place"],
  [18.30, "farm", "place"],
  [18.40, "farm", "place"],
  [18.45, "farm", "place"],
  [19.05, "farm", "place"],
  # [19.15, "farm", "place"],
  # [19.45, "farm", "place"],
  # [20.00, "farm", "place"],

  # buildings
  [3.00, "lumber-camp",    "place"],
  [4.20, "mill",           "place"],
  [6.30, "lumber-camp",    "place"],
  [8.40, "mining-camp",    "place"],
  # [8.50, "mining-camp",    "place"],


  [9.10, "barracks",       "place"],
  [10.30, "archery-range", "place"],
  [10.30, "archery-range", "place"],
  [13.50, "blacksmith",    "place"],

  # units
  [0.00, "villager",   "on"],
  [0.00, "archer",     "on"],
  [0.00, "archer",     "on"],
  [0.00, "skirmisher", "on"],
  [0.00, "skirmisher", "on"],

  # techs
  # [7.04, "loom",           "on"],
  # [7.54, "feudal-age",      "on"],

  [7.29, "loom",           "on"],
  [8.19, "feudal-age",      "on"],


  [0.00, "fletching",       "on"],
  [16.20, "wheelbarrow",    "on"],
  [18.00, "castle-age",     "on"],
  [10.30, "double-bit-axe", "pending"],
  # [10.30, "horse-collar",   "pending"],

]

activeBuildOrder = buildOrders["FF-FLUSH"]

# convert to seconds

for x in activeBuildOrder:
  x[0] = convertToSecs(x[0])

# sort by time
activeBuildOrder.sort(key=lambda x : x[0])

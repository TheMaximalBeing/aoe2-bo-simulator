from utils import *

# -- objects

buildings = [

	"barracks",
	"dock",
	"siege-workshop",
	"farm",
  "gate",
	"mill",
	"house",
	"palisade-wall",
	"palisade-gate",
	"watch-tower",
	"castle",
	"market",
	"archery-range",
	"stable",
	"blacksmith",
	"monastery",
	"town-center",
	"stone-wall",
	"fish-trap",
	"university",
	"bombard-tower",
	"wonder",
	"lumber-camp",
	"mining-camp",
	"outpost",
	"feitoria",
	"krepost",
	"donjon",
	"folwark",
	"caravanserai", ]

units = [

  "villager",
  "millitia",
  "spearman",
  "eagle-scout",
  "archer",
  "skirmisher",
  "scout-cavalry",
  "camel-scout",
  "fishing-ship",
  "transport-ship",
  "fire-galley",
  "trade-cog",
  "demolition-raft",
  "galley",
  "serjeant",
  "trade-cart", ]

techs = [

  "feudal-age",
  "castle-age",
  "imperial-age",
  "loom",
  "man-at-arms",
  "supplies",
  "bloodlines",
  "wheelbarrow",
  "town-watch",
  "gold-mining",
  "stone-mining",
  "double-bit-axe",
  "horse-collar",
  "padded-archer-armor",
  "fletching",
  "foraging",
  "scale-barding-armor",
  "scale-mail-armor", ]

# -- costs

buildingCost = {

	"barracks":[0,175,0,0],
	"dock":[0,150,0,0],
	"siege-workshop":[0,200,0,0],
	"farm":[0,60,0,0],
  "gate":[0,0,30,0],
	"mill":[0,100,0,0],
	"house":[0,25,0,0],
	"palisade-wall":[0,2,0,0],
	"palisade-gate":[0,20,0,0],
	"watch-tower":[0,50,125,0],
	"castle":[0,0,650,0],
	"market":[0,175,0,0],
	"archery-range":[0,175,0,0],
	"stable":[0,175,0,0],
	"blacksmith":[0,150,0,0],
	"monastery":[0,175,0,0],
	"town-center":[0,275,100,0],
	"stone-wall":[0,0,5,0],
	"fish-trap":[0,100,0,0],
	"university":[0,200,0,0],
	"bombard-tower":[0,0,125,100],
	"wonder":[0,1000,1000,1000],
	"lumber-camp":[0,100,0,0],
	"mining-camp":[0,100,0,0],
	"outpost":[0,25,5,0],
	"feitoria":[0,0,300,350],
	"krepost":[0,0,350,0],
	"donjon":[0,75,175,0],
	"folwark":[0,125,0,0],
	"caravanserai":[0,175,0,50], }

unitCost = {

  "villager":[50,0,0,0],
  "millitia":[60,0,0,20],
  "spearman":[25,35,0,0],
  "eagle-scout":[25,0,0,50],
  "archer":[0,25,0,45],
  "skirmisher":[25,35,0,0],
  "scout-cavalry":[80,0,0,0],
  "camel-scout":[55,0,0,60],
  "fishing-ship":[0,75,0,0],
  "transport-ship":[0,125,0,0],
  "fire-galley":[0,75,0,45],
  "trade-cog":[0,100,0,50],
  "demolition-raft":[0,70,0,50],
  "galley":[0,90,0,30],
  "serjeant":[50,0,0,35],
  "trade-cart":[0,100,0,50], }

techCost = {

  "feudal-age":[500,0,0,0],
  "castle-age":[800,0,0,200],
  "imperial-age":[1000,0,0,800],
  "loom":[0,0,0,50],
  "man-at-arms":[60,0,0,20],
  "supplies":[75,0,0,75],
  "bloodlines":[150,0,0,100],
  "wheelbarrow":[175,50,0,0],
  "town-watch":[75,0,0,0],
  "gold-mining":[100,75,0,0],
  "stone-mining":[100,75,0,0],
  "double-bit-axe":[100,50,0,0],
  "horse-collar":[75,75,0,0],
  "padded-archer-armor":[100,0,0,0],
  "fletching":[100,0,0,50],
  "foraging":[150,0,0,0],
  "scale-barding-armor":[150,0,0,0],
  "scale-mail-armor":[100,0,0,0], }

# -- trainsite (i.e. the building dependency)

buildingSite = {

	"barracks":"",
	"dock":"",
	"siege-workshop":"blacksmith",
	"farm":"mill",
  "gate":"",
	"mill":"",
	"house":"",
	"palisade-wall":"",
	"palisade-gate":"",
	"watch-tower":"",
	"castle":"",
	"market":"mill",
	"archery-range":"barracks",
	"stable":"barracks",
	"blacksmith":"",
	"monastery":"",
	"town-center":"",
	"stone-wall":"",
	"fish-trap":"dock",
	"university":"",
	"bombard-tower":"",
	"wonder":"",
	"lumber-camp":"",
	"mining-camp":"",
	"outpost":"",
	"feitoria":"",
	"krepost":"",
	"donjon":"",
	"folwark":"",
	"caravanserai":"", }

unitSite = {

  "villager":"town-center",
  "millitia":"barracks",
  "spearman":"barracks",
  "eagle-scout":"barracks",
  "archer":"archery-range",
  "skirmisher":"archery-range",
  "scout-cavalry":"stable",
  "camel-scout":"stable",
  "fishing-ship":"dock",
  "transport-ship":"dock",
  "fire-galley":"dock",
  "trade-cog":"dock",
  "demolition-raft":"dock",
  "galley":"dock",
  "serjeant":"donjon",
  "trade-cart":"market", }

techSite = {

  "feudal-age":"town-center",
  "castle-age":"town-center",
  "imperial-age":"town-center",
  "loom":"town-center",
  "man-at-arms":"barracks",
  "supplies":"barracks",
  "bloodlines":"stable",
  "wheelbarrow":"town-center",
  "town-watch":"town-center",
  "gold-mining":"mining-camp",
  "stone-mining":"mining-camp",
  "double-bit-axe":"lumber-camp",
  "horse-collar":"mill",
  "padded-archer-armor":"blacksmith",
  "fletching":"blacksmith",
  "foraging":"blacksmith",
  "scale-barding-armor":"blacksmith",
  "scale-mail-armor":"blacksmith", }

# -- dependency (i.e. the tech dependency)

buildingDep = {

	"barracks":"",
	"dock":"",
	"siege-workshop":"castle-age",
	"farm":"",
  "gate":"feudal-age",
	"mill":"",
	"house":"",
	"palisade-wall":"",
	"palisade-gate":"",
	"watch-tower":"feudal-age",
	"castle":"castle-age",
	"market":"feudal-age",
	"archery-range":"feudal-age",
	"stable":"feudal-age",
	"blacksmith":"feudal-age",
	"monastery":"castle-age",
	"town-center":"castle-age",
	"stone-wall":"feudal-age",
	"fish-trap":"feudal-age",
	"university":"castle-age",
	"bombard-tower":"bombard-tower",
	"wonder":"imperial-age",
	"lumber-camp":"",
	"mining-camp":"",
	"outpost":"",
	"feitoria":"imperial-age",
	"krepost":"castle-age",
	"donjon":"feudal-age",
	"folwark":"",
	"caravanserai":"imperial-age", }

unitDep = {

  "villager":"",
  "millitia":"",
  "spearman":"feudal-age",
  "eagle-scout":"feudal-age",
  "archer":"feudal-age",
  "skirmisher":"feudal-age",
  "scout-cavalry":"feudal-age",
  "camel-scout":"feudal-age",
  "fishing-ship":"",
  "transport-ship":"",
  "fire-galley":"feudal-age",
  "trade-cog":"feudal-age",
  "demolition-raft":"feudal-age",
  "galley":"feudal-age",
  "serjeant":"feudal-age",
  "trade-cart":"feudal-age", }

techDep = {

  "feudal-age":"",
  "castle-age":"feudal-age",
  "imperial-age":"castle-age",
  "loom":"",
  "man-at-arms":"feudal-age",
  "supplies":"feudal-age",
  "bloodlines":"feudal-age",
  "wheelbarrow":"feudal-age",
  "town-watch":"feudal-age",
  "gold-mining":"feudal-age",
  "stone-mining":"feudal-age",
  "double-bit-axe":"feudal-age",
  "horse-collar":"feudal-age",
  "padded-archer-armor":"feudal-age",
  "fletching":"feudal-age",
  "foraging":"feudal-age",
  "scale-barding-armor":"feudal-age",
  "scale-mail-armor":"feudal-age", }

# -- create time

buildingTime = {

	"barracks":50,
	"dock":35,
	"siege-workshop":40,
	"farm":15,
  "gate":70,
	"mill":35,
	"house":25,
	"palisade-wall":6,
	"palisade-gate":30,
	"watch-tower":80,
	"castle":200,
	"market":60,
	"archery-range":50,
	"stable":50,
	"blacksmith":40,
	"monastery":40,
	"town-center":150,
	"stone-wall":10,
	"fish-trap":40,
	"university":60,
	"bombard-tower":80,
	"wonder":3500,
	"lumber-camp":35,
	"mining-camp":35,
	"outpost":15,
	"feitoria":120,
	"krepost":150,
	"donjon":90,
	"folwark":40,
	"caravanserai":60, }

unitTime = {

  "villager":25,
  "millitia":21,
  "spearman":22,
  "eagle-scout":60,
  "archer":35,
  "skirmisher":22,
  "scout-cavalry":30,
  "camel-scout":48,
  "fishing-ship":40,
  "transport-ship":46,
  "fire-galley":65,
  "trade-cog":36,
  "demolition-raft":45,
  "galley":60,
  "serjeant":16,
  "trade-cart":51, }

techTime = {

  "feudal-age":130,
  "castle-age":160,
  "imperial-age":190,
  "loom":25,
  "man-at-arms":40,
  "supplies":20,
  "bloodlines":50,
  "wheelbarrow":75,
  "town-watch":25,
  "gold-mining":30,
  "stone-mining":30,
  "double-bit-axe":25,
  "horse-collar":20,
  "padded-archer-armor":40,
  "fletching":30,
  "foraging":50,
  "scale-barding-armor":45,
  "scale-mail-armor":40, }

# -- other

resources = [ "food", "wood", "stone", "gold"]
fullResources = [ "sheep", "boar", "deer", "berries", "fish", "farms", "wood", "stone", "gold" ]

# -- getters for above (includes adjustments)

# adjustment types
# (*) baseline
# (*) civ-bonuses
# (*) team-bonuses
# (*) tech-bonuses (standerd, unique)
# (*) unique-buildings (folwark, caravanserai)

def getBuildingCost(obj, gameState):
  
  # baseline
  tmp = buildingCost[obj]
  return { "food":tmp[0], "wood":tmp[1], "stone":tmp[2], "gold":tmp[3] }

def getUnitCost(obj, gameState):
  
  # baseline
  tmp = unitCost[obj]
  return { "food":tmp[0], "wood":tmp[1], "stone":tmp[2], "gold":tmp[3] }

def getTechCost(obj, gameState):
  
  # baseline
  tmp = techCost[obj]
  return { "food":tmp[0], "wood":tmp[1], "stone":tmp[2], "gold":tmp[3] }

def getBuildingTime(obj, gameState):
  
  # baseline
  return buildingTime[obj]

def getUnitTime(obj, gameState):
  
  # baseline
  return unitTime[obj]

def getTechTime(obj, gameState):
  
  # baseline
  return techTime[obj]

def checkBuildingAvaliable(obj, ready_buildings, gameState):

  bSite = buildingSite[obj]
  if bSite != "" and ready_buildings[bSite] <= 0:
    return False

  bDep = buildingDep[obj]
  if bDep != "" and gameState.done_techs[bDep] <= 0:
    return False

  return True

def checkUnitAvaliable(obj, ready_buildings, gameState):
  
  bSite = unitSite[obj]
  if bSite != "" and ready_buildings[bSite] <= 0:
    return False

  bDep = unitDep[obj]
  if bDep != "" and gameState.done_techs[bDep] <= 0:
    return False

  return True

def checkTechAvaliable(obj, ready_buildings, gameState):
  
  bSite = techSite[obj]
  if bSite != "" and ready_buildings[bSite] <= 0:
    return False

  bDep = techDep[obj]
  if bDep != "" and gameState.done_techs[bDep] <= 0:
    return False

  return True

def canAffordBuilding(obj, gameState):

  cost = getBuildingCost(obj, gameState)
  if cost["food"] > max(0,gameState.stockpiles["food"]): return False
  if cost["wood"] > max(0,gameState.stockpiles["wood"]): return False
  if cost["stone"] > max(0,gameState.stockpiles["stone"]): return False
  if cost["gold"] > max(0,gameState.stockpiles["gold"]): return False
  return True

def canAffordUnit(obj, gameState):

  cost = getUnitCost(obj, gameState)
  if cost["food"] > max(0,gameState.stockpiles["food"]): return False
  if cost["wood"] > max(0,gameState.stockpiles["wood"]): return False
  if cost["stone"] > max(0,gameState.stockpiles["stone"]): return False
  if cost["gold"] > max(0,gameState.stockpiles["gold"]): return False
  return True

def canAffordTech(obj, gameState):

  dropF = 0.
  dropG = 0.
  if obj == "feudal-age": dropF = 65
  if obj == "castle-age": dropF = 95
  if obj == "castle-age": dropG = 35

  cost = getTechCost(obj, gameState)
  if cost["food"]-dropF > max(0,gameState.stockpiles["food"]): return False
  if cost["wood"] > max(0,gameState.stockpiles["wood"]): return False
  if cost["stone"] > max(0,gameState.stockpiles["stone"]): return False
  if cost["gold"]-dropG > max(0,gameState.stockpiles["gold"]): return False
  return True

# -- other getters

def getFarmFood(gameState):

  # - baseline
  F = 175

  # - adjust techs
  if gameState.done_techs["horse-collar"] > 0: F += 75
  # if gameState.done_techs["heavy-plow"] > 0: F += 125
  # if gameState.done_techs["crop-rotation"] > 0: F += 175

  # - adjust unique techs
  # (none)

  # - adjust civ bonuses
  if gameState.civ == "sicilians":
    if gameState.done_techs["horse-collar"] > 0: F += 75*0.25
    # if gameState.done_techs["heavy-plow"] > 0: F += 125*0.25
    # if gameState.done_techs["crop-rotation"] > 0: F += 175*0.25
  if gameState.civ == "mayans": F *= 1.15

  # - adjust team bonuses
  if gameState.civ == "chinese": F *= 1.10

  return F

def getFishTrapFood(gameState):

  # baseline
  return 715

def getVillagerSpeed(gameState):

  # (*) baseline
  result = 0.8

  # (*) civ-bonuses
  
  # (*) team-bonuses
  
  # (*) tech-bonuses (standerd, unique)

  if gameState.done_techs["wheelbarrow"] > 0: result *= 1.1
  # if gameState.done_techs["hand-cart"] > 0: result *= 1.1
  # if gameState.civ == "bohemians" and gameState.done_techs["fervor"] > 0: result *= 1.15
  
  # (*) unique-buildings (folwark, caravanserai)

  return result

def getGatherRates(gameState):

  # (*) baseline
  result = initDict(fullResources, 0.33)
  result["fish"] = 0.426
  result["boar"] = 0.408
  result["deer"] = 0.408
  result["wood"] = 0.388
  result["gold"] = 0.379
  result["stone"] = 0.359
  result["sheep"] = 0.330
  # result["farms"] = 0.33 # max 0.40 due to farm res rate
  result["farms"] = 0.335
  result["berries"] = 0.310

  # (*) civ-bonuses

  if gameState.civ == "celts": result["wood"] *= 1.2
  
  # (*) team-bonuses
  
  # (*) tech-bonuses (standerd, unique)

  if gameState.done_techs["double-bit-axe"] > 0: 
    result["wood"] *= 1.2
  # if gameState.done_techs["bow-saw"] > 0: result["wood"] *= 1.2
  # if gameState.done_techs["two-man-saw"] > 0: result["wood"] *= 1.1
  if gameState.done_techs["stone-mining"] > 0: result["stone"] *= 1.15
  # if gameState.done_techs["stone-shaft-mining"] > 0: result["stone"] *= 1.15
  if gameState.done_techs["gold-mining"] > 0: result["gold"] *= 1.15
  # if gameState.done_techs["gold-shaft-mining"] > 0: result["gold"] *= 1.15
  # if gameState.done_techs["grand-trunk-road"] > 0: result["gold"] *= 1.10
  if gameState.done_techs["wheelbarrow"] > 0: result["farms"] = 0.37 # need to do proper testing for these
  # if gameState.done_techs["hand-cart"] > 0: result["farms"] = 0.40
  
  # (*) unique-buildings (folwark, caravanserai)



  return result

def getHousingCap(gameState):

  # baseline
  housing_cap = gameState.done_buildings["house"]*5 + gameState.done_buildings["town-center"]*5 + gameState.done_buildings["castle"]*20
  
  # civ-bonuses
  if gameState.civ == "huns": housing_cap = gameState.pop_cap
  if gameState.civ == "incas": housing_cap += gameState.done_buildings["house"]*5
  if gameState.civ == "chinese": housing_cap += gameState.done_buildings["town-center"]*5
  housing_cap = min(housing_cap, gameState.pop_cap)

  return housing_cap

def getMaxCarry(gatherType, gameState):

  result = 10

  # (*) baseline

  if gatherType == "sheep":
    pass
  elif gatherType == "boar":
    result = 10 # allow drops
  elif gatherType == "deer":
    result = 35
  elif gatherType == "berries":
    pass
  elif gatherType == "fish":
    pass
  elif gatherType == "farms":
    pass
  elif gatherType == "wood":
    pass
  elif gatherType == "stone":
    pass
  elif gatherType == "gold":
    pass

  # (*) civ-bonuses

  # (*) team-bonuses
  
  # (*) tech-bonuses (standerd, unique)

  if gameState.done_techs["wheelbarrow"] > 0: result *= 1.25
  # if gameState.done_techs["hand-cart"] > 0: result *= 1.50
  # if gatherType == "farms" and gameState.done_techs["heavy-plow"] > 0: result += 1

  # (*) unique-buildings (folwark, caravanserai)

  return result

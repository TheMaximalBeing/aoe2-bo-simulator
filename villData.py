from gameData import *
from utils import *
from villNumbers import *
import math
import copy

class VillData:

  def __init__(self):

    # avaliable states:
    # (*) idle - not doing anything
    # (*) build - building something
    # (*) gather - gathering resources
    # (*) drop - drop off resources
    # (*) return - return to res after a drop off
    # (*) reassign - reassign to a new resource
    # (*) lure - walking to and luring boar
    # (*) toBuilding - walk to building (to build it)
    # (*) fromBuilding - walk back from building after building it
    # (*) reseed - reseed our associated farm
    self.state = "idle"
    # the type or resource being gathered
    self.gatherType = "none"
    # the number of resources being gethered
    self.carry = 0
    # the amount of time working on current task
    self.time = 0
    # the carry limit before current task completed
    self.maxCarry = 10
    # the time limit before current task completed
    self.maxTime = -1
    # the amount of food left on our farm
    self.farmFood = 0
    # the villager type: "villager" or "fishing-ship"
    self.type = "villager"
    # what we are building
    self.building = "none"

  def gatherTypeSimple(self):

    if self.gatherType in ["sheep", "boar", "deer", "berries", "farms"]:
      return "food"
    else:
      return self.gatherType


# ===== helper functions =====

def getVillIndex(res,vills):

  minValue = 1e50
  minKey = -1

  for i,v in enumerate(vills):

    val = v.carry
    if v.state != "gather": val += 100000
    if v.gatherTypeSimple() != res: val += 10000
    if v.gatherType == "farms": val += 50
    if val < minValue:
      minValue = val
      minKey = i
  return minKey

wastedTime = initDict(resources,0)

def builderSelection(obj, gameState):

  global wastedTime

  # get gatherer counts

  counts = initDict(resources, 0)
  for v in gameState.villager_states:
    if v.state == "gather":
      counts[v.gatherTypeSimple()] += 1

  wastedTime2 = copy.deepcopy(wastedTime)
  wastedTime2 = {k:v/max(1,gameState.villager_distribution[k]) for k,v in wastedTime2.items() }
  if counts["food"] == 0: wastedTime2["food"] += 100000
  if counts["wood"] == 0: wastedTime2["wood"] += 100000
  if counts["stone"] == 0: wastedTime2["stone"] += 100000
  if counts["gold"] == 0: wastedTime2["gold"] += 100000

  # decide on F,W,S,G

  # !!!!
  # if gameState.done_units["villager"] >= 21:
    # res = "food"

  res = argMinValue(wastedTime2, lambda x: x)
  if obj == "farm": res = "food"
  if obj == "lumber-camp": res = "wood"
  if obj == "mining-camp": res = "gold"

  if wastedTime2[res] < 1000:
    print(res, obj, wastedTime[res], int(wastedTime["food"]), int(wastedTime["wood"]), gameState.villager_distribution["food"], gameState.villager_distribution["wood"])


  # get villager of appropriate res
  vill = getVillIndex(res,gameState.villager_states)

  if gameState.villager_states[vill].state != "gather": return -1
  
  if vill == -1 and obj == "mining-camp":
    vill = getVillIndex(res,gameState.villager_states)

  if vill != -1:
    # TODO: also add walking time..
    wastedTime[res] += getBuildingTime(obj, gameState)
  
  return vill

def getCarryStockpiles(gameState):

  carry = initDict(fullResources, 0)

  for v in gameState.villager_states:

    # food types
    if v.gatherType == "boar": carry["boar"] += v.carry
    if v.gatherType == "deer": carry["deer"] += v.carry
    if v.gatherType == "sheep": carry["sheep"] += v.carry
    if v.gatherType == "berries": carry["berries"] += v.carry
    if v.gatherType == "fish": carry["fish"] += v.carry
    if v.gatherType == "farms": carry["farms"] += v.carry

    # others
    if v.gatherType == "wood": carry["wood"] += v.carry
    if v.gatherType == "stone": carry["stone"] += v.carry
    if v.gatherType == "gold": carry["gold"] += v.carry

  # full food carry
  carrySimple = { k:carry[k] for k in ["wood","gold","stone"] }
  carrySimple["food"] = carry["boar"] + carry["deer"] + carry["sheep"] + carry["berries"] + carry["fish"] + carry["farms"]

  return (carry, carrySimple)

def getActVillNumbers(gameState):

  act = initDict(fullResources, 0)

  for v in gameState.villager_states:

    # food types
    if v.gatherType == "boar": act["boar"] += 1
    if v.gatherType == "deer": act["deer"] += 1
    if v.gatherType == "sheep": act["sheep"] += 1
    if v.gatherType == "berries": act["berries"] += 1
    if v.gatherType == "fish": act["fish"] += 1
    if v.gatherType == "farms": act["farms"] += 1

    # others
    if v.gatherType == "wood": act["wood"] += 1
    if v.gatherType == "stone": act["stone"] += 1
    if v.gatherType == "gold": act["gold"] += 1

  # full food carry
  act["food"] = act["boar"] + act["deer"] + act["sheep"] + act["berries"] + act["fish"] + act["farms"]

  # another version without extra food stuff
  actSimple = { k:v for k,v in act.items() if k not in ["boar", "deer", "sheep", "berries", "fish", "farms"]}

  return (act,actSimple)

def decideFVillager(gameState):

  # decide on the next gather type for F villagers
  return "sheep"

# ===== main functions =====

def findGatherer(res, gameState):

  minIndex = -1
  minRes = 10000

  for i,v in enumerate(gameState.villager_states):
    if v.gatherType != res: continue
    if v.state != "gather": continue
    if v.carry < minRes:
      minRes = v.carry
      minIndex = i

  return minIndex

def reassign(fromm, too, gameState):

  i = findGatherer(fromm, gameState)
  if i == -1: return
  v = gameState.villager_states[i]
  v.state = "reassign"
  v.time = 0
  v.maxTime = gameState.penalties[v.gatherType][too]
  v.gatherType = too


lureCount = 0

def switchFVillagers(gameState):

  global lureCount
  remaining = { x:gameState.avaliable_res[x] - gameState.stockpilesGathered[x] for x in fullResources }
  villCount = gameState.done_units["villager"]

  counts = initDict(fullResources, 0)
  counts2 = initDict(fullResources, 0)
  for v in gameState.villager_states:
    counts[v.gatherType] += 1
    if v.state != "gather": continue
    counts2[v.gatherType] += 1

  # if any idle farms then populate them

  if gameState.free_farms > 0:

    for v in gameState.villager_states:
      if v.state != "gather": continue
      if v.gatherType in ["sheep", "boar", "deer", "berries", "fish"]:
        v.state = "reassign"
        v.maxTime = gameState.penalties[v.gatherType]["farms"]
        v.gatherType = "farms"
        v.time = 0
        gameState.free_farms -= 1
        break

  # add lurers
  if villCount >= 7 and lureCount == 0 or villCount >= 13 and lureCount == 1:
    i = findGatherer("sheep", gameState)
    if i == -1: i = findGatherer("boar", gameState)
    if i != -1:
      v = gameState.villager_states[i]
      v.time = 0
      v.maxTime = 2*gameState.boarDist/gameState.villSpeed
      v.state = "lure"
      lureCount += 1

  # 6 sheep -> boar when 7 vills
  if villCount >= 7 and counts["boar"] < 7 and counts["sheep"] > 0 and remaining["boar"] > 50:
    reassign("sheep", "boar", gameState)
    return

  # 8-11 go on berries
  if counts["boar"] + counts["sheep"] > 8 and counts["sheep"] > 0 and counts["berries"] < 4 and remaining["berries"] > 50:
    reassign("sheep", "berries", gameState)
    return

  # (low-res) sheep -> boar
  if remaining["sheep"] <= 0 and remaining["boar"] > 50 and counts2["sheep"] > 0:
    reassign("sheep", "boar", gameState)
    return

  # (low-res) boar -> sheep
  if remaining["sheep"] > 50 and remaining["boar"] <= 0 and counts2["boar"] > 0:
    reassign("boar", "sheep", gameState)
    return

  # (low-res) boar,sheep -> deer
  if remaining["sheep"] <= 0 and remaining["boar"] <= 0 and remaining["deer"] > 50 and counts2["sheep"] > 0:
    reassign("sheep", "deer", gameState)
    return

  # (low-res) boar,sheep -> deer
  if remaining["sheep"] <= 0 and remaining["boar"] <= 0 and remaining["deer"] > 50 and counts2["boar"] > 0:
    reassign("boar", "deer", gameState)
    return

  # (low-res) boar,sheep,deer -> berries
  if remaining["sheep"] <= 0 and remaining["boar"] <= 0 and remaining["deer"] <= 0 and remaining["berries"] > 50 and counts2["sheep"] > 0:
    reassign("sheep", "berries", gameState)
    return

  # (low-res) boar,sheep,deer -> berries
  if remaining["sheep"] <= 0 and remaining["boar"] <= 0 and remaining["deer"] <= 0 and remaining["berries"] > 50 and counts2["boar"] > 0:
    reassign("boar", "berries", gameState)
    return

  # (low-res) boar,sheep,deer -> berries
  if remaining["sheep"] <= 0 and remaining["boar"] <= 0 and remaining["deer"] <= 0 and remaining["berries"] > 50 and counts2["deer"] > 0:
    reassign("deer", "berries", gameState)
    return

  # berries -> farms
  # todo...


def reassignVillagers(gameState):

  # alias of vill list
  vills = gameState.villager_states

  # get number of vills
  villCount = gameState.done_units["villager"]

  # add new vills to the list
  while len(vills) < villCount:
    vills.append(VillData())

  # get actual res numbers
  (_,act_numbers) = getActVillNumbers(gameState)

  # get desired res numbers
  des_numbers = getFinalVillNumbers(gameState)

  # assign new vills
  while True:
    if sum(act_numbers.values()) >= villCount: break
    delta = { k : act_numbers[k] - des_numbers[k] for k in act_numbers }
    minRes = argMinValue(delta, lambda x:x)
    act_numbers[minRes] += 1

    for v in vills:
      if v.state == "idle": break
    if v.state != "idle": raise Exception("invalid")

    v.time = 0
    v.state = "reassign"
    v.gatherType = minRes
    if minRes == "food": v.gatherType = decideFVillager(gameState)
    v.maxTime = gameState.penalties["none"][v.gatherType]

  # get biggest error
  delta = { k : act_numbers[k] - des_numbers[k] for k in act_numbers }
  mainRes = argMinValue(delta, lambda x:-abs(x))
  mainDelta = delta[mainRes]
  secondRes = argMinValue(delta, lambda x:math.copysign(1.,mainDelta)*x)

  # reassign vill

  pendingVills = 0
  for x in gameState.pending_units:
    if x[0] == "villager":
      pendingVills += 1

  # no reassignments when researching loom, wheelbarrow, hand-cart, etc
  for x in gameState.pending_techs:
    if x[0] in ["loom", "wheelbarrow", "hand-cart"]:
      return

  if abs(mainDelta) > 1.5 or pendingVills == 0 and abs(mainDelta) > 0.9:

    fromm = mainRes
    too = secondRes

    if mainDelta < 0.0:
      fromm = secondRes
      too = mainRes

    i = getVillIndex(fromm,vills)
    if i == -1: return

    act_numbers[fromm] -= 1
    act_numbers[too] += 1

    # (instant drop off)
    gameState.stockpiles[vills[i].gatherTypeSimple()] += vills[i].carry
    vills[i].carry = 0
    
    vills[i].state = "reassign"
    vills[i].time = 0
    if too == "food": too = decideFVillager(gameState)
    vills[i].maxTime = gameState.penalties[vills[i].gatherType][too]
    vills[i].gatherType = too

def updateVillagerStates(gameState):

  # alias of vill list
  vills = gameState.villager_states
  speed = getVillagerSpeed(gameState)

  for v in vills:

    # gather -> drop
    if v.state == "gather" and v.carry >= v.maxCarry:
      v.state = "drop"
      v.time = 0
      v.maxTime = gameState.drop_off[v.gatherType] / speed

    # drop -> return
    if v.state == "drop" and v.time >= v.maxTime:
      v.state = "return"
      v.time = 0
      v.maxTime = gameState.drop_off[v.gatherType] / speed
      gameState.stockpiles[v.gatherTypeSimple()] += v.carry
      v.carry = 0

    # return -> gather
    if v.state == "return" and v.time >= v.maxTime:
      v.state = "gather"
      v.time = 0
      v.maxCarry = getMaxCarry(v.gatherType, gameState)

    # gather -> reseed
    if v.state == "gather" and v.farmFood <= 0 and v.gatherType == "farms":
      v.state = "reseed"
      v.time = 0
      v.maxTime = getBuildingTime("farm", gameState)
      gameState.buyBuilding("farm")
      # Note: reseeds don't go into the pending list!

    # reseed -> gather
    if v.state == "reseed" and v.time >= v.maxTime:
      v.state = "gather"
      v.time = 0
      v.farmFood = getFarmFood(gameState)
      gameState.stockpiles["food"] += v.carry
      v.carry = 0

    # gather -> toBuilding
    # (done elsewhere)

    # toBuilding -> build
    if v.state == "toBuilding" and v.time >= v.maxTime:
      v.state = "build"
      v.time = 0
      v.maxTime = getBuildingTime(v.building, gameState)
      try:
        i = gameState.walking_buildings.find(v.building)
        del i
      except Exception as e:
        pass

      gameState.pending_buildings.append([v.building, 0, v.maxTime])
      
    # build -> fromBuilding, gather
    if v.state == "build" and v.time >= v.maxTime:
      v.time = 0
      
      if v.building in ["farm", "lumber-camp", "mining-camp", "mill", "town-center"]:
        gameState.stockpiles[v.gatherTypeSimple()] += v.carry
        v.carry = 0
      
      if v.building == "farm":
        v.state = "gather"
        v.gatherType = "farms"
        v.farmFood = getFarmFood(gameState)
        v.maxCarry = getMaxCarry(v.gatherType, gameState)

      else:
        v.state = "fromBuilding"
        v.maxTime = getBuildingTime(v.building, gameState)

    # fromBuilding -> gather
    if v.state == "fromBuilding" and v.time >= v.maxTime:
      v.state = "gather"
      v.time = 0
      v.maxCarry = getMaxCarry(v.gatherType, gameState)

    # gather -> lure
    # (done elsewhere)

    # lure -> gather
    if v.state == "lure" and v.time >= v.maxTime:
      v.state = "gather"
      v.time = 0
      v.maxCarry = getMaxCarry(v.gatherType, gameState)

    # gather,idle -> reassign
    # (done elsewhere)

    # reassign -> gather
    if v.state == "reassign" and v.time >= v.maxTime:
      v.state = "gather"
      v.time = 0
      v.maxCarry = getMaxCarry(v.gatherType, gameState)

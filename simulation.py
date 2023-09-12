from buildOrder import *
from gameData import *
from gameStart import *
from utils import *
from villData import *
from villNumbers import *
import copy

class GameState:

  # ===== setup state =====

  def __init__(self):

    # ======== simulation info ========

    # stat record time; format: MM.SS
    self.dt_stats = convertToSecs(0.25)
    # time step; format: MM.SS
    self.dt = convertToSecs(0.01)
    # end simulation time; format: MM.SS
    # self.endTime = convertToSecs(22.00)
    self.endTime = convertToSecs(16.00)
    # walking-distances (note that villagers gather/drop from 1/4 tiles away)
    self.drop_off = {

      "sheep":0.5,
      "boar":0.5,
      "deer":1.5,
      "berries":2.5,
      "farms":1.5,
      "stone":1.5,
      "gold":1.5,
      "wood":1.5 }
    # reassignment penalties
    self.penalties = {

      "none"   :{ "sheep":3, "boar":3, "deer":5, "berries":14, "farms":9, "stone":20, "gold":17, "wood":16 },
      "sheep"  :{ "sheep":0, "boar":0.5, "deer":3, "berries":14, "farms":7, "stone":20, "gold":17, "wood":6 },
      "boar"   :{ "sheep":0.5, "boar":0, "deer":3, "berries":14, "farms":7, "stone":20, "gold":17, "wood":16 },
      "deer"   :{ "sheep":3, "boar":3, "deer":0, "berries":14, "farms":6, "stone":20, "gold":17, "wood":16 },
      "berries":{ "sheep":10, "boar":10, "deer":10, "berries":0, "farms":6, "stone":20, "gold":17, "wood":16 },
      "farms"  :{ "sheep":3, "boar":3, "deer":3, "berries":7, "farms":0, "stone":20, "gold":17, "wood":16 },
      "stone"  :{ "sheep":20, "boar":20, "deer":20, "berries":20, "farms":15, "stone":0, "gold":17, "wood":16 },
      "gold"   :{ "sheep":17, "boar":17, "deer":17, "berries":17, "farms":15, "stone":20, "gold":0, "wood":16 },
      "wood"   :{ "sheep":19, "boar":19, "deer":19, "berries":19, "farms":15, "stone":20, "gold":17, "wood":0 } }

    self.boarDist = 23
    # the build order
    self.bo = copy.deepcopy(activeBuildOrder)
    # building distances
    self.buildingDistances = initDict(buildings, 8)
    self.buildingDistances["farm"] = 5
    self.buildingDistances["barracks"] = 13
    self.buildingDistances["archery-range"] = 13
    self.buildingDistances["stable"] = 13
    self.buildingDistances["blacksmith"] = 13
    self.buildingDistances["market"] = 13

    # ======== game-state ========
    
    # current game time in seconds
    self.gameTime = 0
    # current population
    self.population = 0
    # current civ
    self.civ = ""
    # instantaneous resources gathered; includes specific food types
    self.stockpilesGathered = initDict(fullResources, 0)
    # resources gathered + starting resources - resources spent
    self.stockpiles = initDict(resources, 0)
    # housing limit
    self.housing_cap = 0
    # population limit
    self.pop_cap = 0
    # total farms
    self.farm_count = 0

    # these are objects that we will create when resources become available
    # format: { name:number-of-overwatches }

    self.overwatch_techs = initDict(techs, 0)
    self.overwatch_units = initDict(units, 0)
    self.overwatch_buildings = initDict(buildings, 0)

    # these are buildings that we will create once the builder has arrived
    # format: [ [name, assigned-count] ]

    self.walking_buildings = [ ]

    # these are objects that are in progress
    # format: [ [name, progress-time, max-time] ]

    self.pending_techs = [ ]
    self.pending_units = [ ]
    self.pending_buildings = [ ]

    # these are the current counts of each object
    # format { name:count }

    self.done_techs = initDict(techs, 0)
    self.done_units = initDict(units, 0)
    self.done_buildings = initDict(buildings, 0)

    # the state of each villager, Format: [ VillData ]
    self.villager_states = [ ]

    # avaliable resources at map start
    self.avaliable_res = initDict(fullResources, 0)

    # ======== saved-stats ========

    self.villager_distribution = initDict(fullResources, 0)
    self.villSpeed = 0
    self.gatherRates = { }
    self.housing_headroom = 0
    self.remaining_res = { }
    self.free_farms = 0
    self.ready_buildings = { }


    # ======== recorded-stats ========

    tmp = { "build*":0., "gather":0., "drop*":0., "reassign":0., "reseed":0., "lure":0. }

    self.villagerTimes = { x:copy.deepcopy(tmp) for x in fullResources }
    self.rec_res_collected = [ ]
    self.rec_stockpiles = [ ]
    self.rec_civilian_pop = [ ]
    self.rec_military_pop = [ ]

    self.useTime = initDict(buildings, 0.0)
    self.idleTime = initDict(buildings, 0.0)

  def applyGameStart(self):

    self.civ = starting_civ
    self.pop_cap = starting_pop_cap
    self.avaliable_res |= starting_avail_res
    self.stockpiles |= starting_stockpiles
    self.done_techs |= starting_techs
    self.done_units |= starting_units
    self.done_buildings |= starting_buildings

  # ===== general helpers =====

  def buyBuilding(self, obj):
    price = getBuildingCost(obj, self)
    self.stockpiles["food"] -= price["food"]
    self.stockpiles["wood"] -= price["wood"]
    self.stockpiles["stone"] -= price["stone"]
    self.stockpiles["gold"] -= price["gold"]

  def buyUnit(self, obj):
    price = getUnitCost(obj, self)
    self.stockpiles["food"] -= price["food"]
    self.stockpiles["wood"] -= price["wood"]
    self.stockpiles["stone"] -= price["stone"]
    self.stockpiles["gold"] -= price["gold"]

  def buyTech(self, obj):
    price = getTechCost(obj, self)
    self.stockpiles["food"] -= price["food"]
    self.stockpiles["wood"] -= price["wood"]
    self.stockpiles["stone"] -= price["stone"]
    self.stockpiles["gold"] -= price["gold"]

  # ===== simulation helpers =====

  def updateStats(self):

    self.villager_distribution = initDict(fullResources, 0)
    for v in gameState.villager_states:
      self.villager_distribution[v.gatherType] += 1

    self.villager_distribution["food"] = sum([v for k,v in self.villager_distribution.items() if k not in ["wood", "stone", "gold"]])

    self.stockpilesGathered["food"] = sum([self.stockpilesGathered[k] for k in self.stockpilesGathered if k not in ["wood", "stone", "gold"]])
    self.population = sum(self.done_units.values())
    self.housing_cap = getHousingCap(self)
    self.farm_count = self.done_buildings["farm"]
    self.villSpeed = getVillagerSpeed(self)
    self.gatherRates = getGatherRates(gameState)
    self.housing_headroom = self.housing_cap-self.population
    self.remaining_res = { k:self.avaliable_res[k] - self.stockpilesGathered[k] for k in fullResources }

    self.free_farms = self.farm_count
    for v in self.villager_states:
      if v.gatherType == "farms":
        self.free_farms -= 1

    self.ready_buildings = copy.deepcopy(self.done_buildings)
    for x in self.pending_units:
      self.ready_buildings[unitSite[x[0]]] -= 1
    for x in self.pending_techs:
      self.ready_buildings[techSite[x[0]]] -= 1

  def updateLists(self):

    # - check if pending list items are ready -> add to final list

    for x in self.pending_techs:
      if x[1] >= x[2]: 
        self.done_techs[x[0]] += 1
        site = techSite[x[0]]
        self.ready_buildings[site] = min(self.done_buildings[site],self.ready_buildings[site]+1)
    for x in self.pending_units:
      if x[1] >= x[2]: 
        self.done_units[x[0]] += 1
        site = unitSite[x[0]]
        self.ready_buildings[site] = min(self.done_buildings[site],self.ready_buildings[site]+1)
    for x in self.pending_buildings:
      if x[1] >= x[2]: 
        self.done_buildings[x[0]] += 1
    
    self.pending_techs[:] = filter(lambda x: x[1] < x[2], self.pending_techs)
    self.pending_units[:] = filter(lambda x: x[1] < x[2], self.pending_units)
    self.pending_buildings[:] = filter(lambda x: x[1] < x[2], self.pending_buildings)

    # - check if overwatch items are avaliable

    overwatch_techs_delta = copy.deepcopy(self.overwatch_techs)
    overwatch_units_delta = copy.deepcopy(self.overwatch_units)
    overwatch_buildings_delta = copy.deepcopy(self.overwatch_buildings)

    for x in self.pending_techs:
      overwatch_techs_delta[x[0]] -= 1
    for x in self.pending_units:
      overwatch_units_delta[x[0]] -= 1
    for x in self.pending_buildings:
      overwatch_buildings_delta[x[0]] -= 1

    for k,v in overwatch_techs_delta.items():
      if v <= 0: continue
      if self.ready_buildings[techSite[k]] <= 0: continue
      if not canAffordTech(k,self): continue
      if not checkTechAvaliable(k,self.ready_buildings,self): continue
      # TODO: only do this when done
      self.overwatch_techs[k] -= 1
      self.pending_techs.append([k, 0.0, getTechTime(k, self)])
      self.buyTech(k)
      self.ready_buildings[techSite[k]] -= 1

    for k,v in overwatch_buildings_delta.items():
      if v <= 0: continue
      if not canAffordBuilding(k,self): continue
      if not checkBuildingAvaliable(k,self.ready_buildings,self): continue
      # TODO: only do this when done
      self.overwatch_buildings[k] -= 1
      self.pending_buildings.append([k, 0.0, getBuildingTime(k, self)])
      self.buyBuilding(k)

    for k,v in overwatch_units_delta.items():
      if v <= 0: continue
      if self.ready_buildings[unitSite[k]] <= 0: continue
      if not canAffordUnit(k,self): continue
      if not checkUnitAvaliable(k,self.ready_buildings,self): continue
      self.pending_units.append([k, 0.0, getUnitTime(k, self)])
      self.buyUnit(k)
      self.ready_buildings[unitSite[k]] -= 1

  def checkBuildOrder(self):

    if self.gameTime >= 350:
      pass

    i = -1

    while True:

      i += 1

      # check if loop should quit
      if len(self.bo) <= i: break
      if self.bo[i][0] > self.gameTime: break

      # next BO item is activated!
      nextItem = self.bo[i]

      # figure out what type it is
      name = nextItem[1]
      request = nextItem[2]

      typee = "unit"
      if name in buildings:
        typee = "building"
      elif name in techs:
        typee = "tech"

      if request == "done":

        if typee == "unit": self.buyUnit(name)
        if typee == "building": self.buyBuilding(name)
        if typee == "tech": self.buyTech(name)

        if typee == "unit": self.done_units[name] += 1
        if typee == "building": self.done_buildings[name] += 1
        if typee == "tech": self.done_techs[name] += 1

        del self.bo[i]
        i -= 1

      elif request == "place":

        if typee != "building": raise Exception("invalid")
        if not checkBuildingAvaliable(name,self.ready_buildings,self): continue
        self.buyBuilding(name)
        self.walking_buildings.append([name, 0])

        del self.bo[i]
        i -= 1

      elif request == "pending":

        if typee == "building":
          if not checkBuildingAvaliable(name,self.ready_buildings,self): continue
          self.buyBuilding(name)
          self.pending_buildings.append([name, 0.0, getBuildingTime(name, self)])
          del self.bo[i]
          i -= 1

        elif typee == "unit":
          if not checkUnitAvaliable(name,self.ready_buildings,self): continue
          if ready_buildings(unitSite[name]) <= 0: continue
          ready_buildings[unitSite[name]] -= 1
          self.buyUnit(name)
          self.pending_units.append([name, 0.0, getUnitTime(name, self)])
          del self.bo[i]
          i -= 1

        else:
          if not checkTechAvaliable(name,self.ready_buildings,self): continue
          if self.ready_buildings[techSite[name]] <= 0: continue
          self.ready_buildings[techSite[name]] -= 1
          self.buyTech(name)
          self.pending_techs.append([name, 0.0, getTechTime(name, self)])
          del self.bo[i]
          i -= 1

      elif request == "on":

        if typee == "building": self.overwatch_buildings[name] += 1
        if typee == "unit": self.overwatch_units[name] += 1
        if typee == "tech": self.overwatch_techs[name] += 1
        del self.bo[i]
        i -= 1

      elif request == "off":

        if typee == "building": self.overwatch_buildings[name] = max(0,self.overwatch_buildings[name]-1)
        if typee == "unit": self.overwatch_units[name] = max(0,self.overwatch_units[name]-1)
        if typee == "tech": self.overwatch_techs[name] = max(0,self.overwatch_techs[name]-1)
        del self.bo[i]
        i -= 1

      else: raise Exception("unknown request")

  def updateVillagers(self):

    # --- reassign villagers

    reassignVillagers(self)

    # --- assign free vills to walk to foundations

    for x in self.walking_buildings:

      # check if there are no assigned villagers, and assign a villager
      if x[1] == 0:
        index = builderSelection(x[0], self)
        if index == -1: break
        self.villager_states[index].state = "toBuilding"
        self.villager_states[index].building = x[0]
        self.villager_states[index].time = 0
        self.villager_states[index].maxTime = self.buildingDistances[x[0]]/self.villSpeed
        x[1] += 1

    # Note: walking -> pending transition done automatically

    # --- switch food villagers to other food

    switchFVillagers(self)

    # --- update villager states

    updateVillagerStates(self)

  def timeStep(self):

    # --- increment villager carry, and farm capacity

    for v in self.villager_states:
      if v.state == "gather":
        amount = self.gatherRates[v.gatherType] * self.dt
        v.carry += amount
        if v.gatherType == "farms":
          v.farmFood -= amount
        self.stockpilesGathered[v.gatherType] += amount

    # --- increment action time of villagers

    for v in self.villager_states:
      v.time += self.dt

    # --- record time on each action

    for k,v in self.done_buildings.items():

      used = v - self.ready_buildings[k]
      idle = v - used
      self.useTime[k] += used*self.dt
      self.idleTime[k] += idle*self.dt

    for v in self.villager_states:

      if v.state in ["build", "toBuilding", "fromBuilding"]:
        self.villagerTimes[v.gatherType]["build*"] += self.dt
      elif v.state == "gather":
        self.villagerTimes[v.gatherType]["gather"] += self.dt
      elif v.state == "drop" or v.state == "return":
        self.villagerTimes[v.gatherType]["drop*"] += self.dt
      elif v.state == "reassign":
        self.villagerTimes[v.gatherType]["reassign"] += self.dt
      elif v.state == "lure":
        self.villagerTimes[v.gatherType]["lure"] += self.dt
      elif v.state == "reseed":
        self.villagerTimes[v.gatherType]["reseed"] += self.dt
      else:
        raise(Exception("invalid state: " + v.state))

    # --- increment progress of pending objects

    for p in self.pending_buildings: p[1] += self.dt
    for p in self.pending_techs: p[1] += self.dt
    for p in self.pending_units: p[1] += self.dt

    # --- increment game time

    self.gameTime += self.dt

  def record(self):

    if self.gameTime % self.dt_stats == 0:

      civ_pop = sum([v for k,v in self.done_units.items() if k == "villager"])
      mil_pop = sum([v for k,v in self.done_units.items() if k != "villager"])
      remaining = { x:gameState.avaliable_res[x] - gameState.stockpilesGathered[x] for x in fullResources }
      # full vill distribution
      dist = initDict(fullResources, 0)
      for v in self.villager_states:
        if v.gatherType == "none": continue
        dist[v.gatherType] += 1

      print("--------------------", civ_pop)
      print("time: ", str(int(self.gameTime // 60)).rjust(2,'0') + ":" + str(int(self.gameTime % 60)).rjust(2,'0'), " civ: ", civ_pop, " mil: ", mil_pop,
            "   F: ", int(self.stockpiles["food"]), " W: ", int(self.stockpiles["wood"]), " S: " , int(self.stockpiles["stone"]), " G: ", int(self.stockpiles["gold"]))
      print("         techs: ", "  ".join([k for k,v in self.done_techs.items() if v > 0]))
      print("         units: ", "  ".join([k+":"+str(v) for k,v in self.done_units.items() if v > 0]))
      print("     buildings: ", "  ".join([k+":"+str(v) for k,v in self.done_buildings.items() if v > 0]))
      print("idle-buildings: ", "  ".join([k+": "+str(self.idleTime[k])+" ("+str(int(100.*self.idleTime[k]/(self.idleTime[k]+self.useTime[k])))+")" for k in self.idleTime if self.useTime[k] > 0]))
      print("  distribution: ", "  ".join([k+": "+str(v) for k,v in self.villager_distribution.items() if v != 0]))
      print(" remaining-res: ", "  ".join([k+": "+str(int(v)) for k,v in remaining.items() if k in ["sheep", "boar", "deer", "berries"]]))

      print("villager activities (percent):")
      for x in self.villagerTimes:
        if self.villagerTimes[x]["gather"] == 0.: continue
        total = sum(self.villagerTimes[x].values())
        print((x+": ").rjust(10), "  ".join([k+": "+str(int(100.*v/total)).ljust(4) for k,v in self.villagerTimes[x].items()]))

      # villager times
      # gather-time, drop-time, building-time, reassignment-time, reseed-time

      # number of reseeds
      # reassignments
      # reassignment times, gather times, drop times, building times

      # self.rec_stockpiles.append([self.stockpiles["food"], self.stockpiles["wood"], self.stockpiles["stone"], self.stockpiles["gold"]])
      # self.rec_civilian_pop.append(civ_pop)
      # self.rec_military_pop.append(mil_pop)

# ===== main simulation function =====

  def simulate(self):

    while self.gameTime < self.endTime:
      
      for i in range(2):
        self.updateStats()
        self.updateLists()
        self.checkBuildOrder()
        self.updateVillagers()
      self.record()
      self.timeStep()

# ===== stats =====

# villager_idle_time = 0
# building_idle_times = { }

# ===== actual program =====

gameState = GameState()
gameState.applyGameStart()
gameState.simulate()


pass
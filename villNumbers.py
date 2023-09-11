villNumbers = { }

# ----- add vill numbers for each BO here -----

# Format: [ [vills,age,F,W,G,S] ]

villNumbers["FF-SCOUT-FLUSH"] = [

  [ 0,0.0, 0,0,0,0],
  [ 7,0.0, 7,0,0,0],
  [11,0.0, 7,4,0,0],
  [20,0.0, 16,4,0,0],
  [21,0.0, 16,5,0,0],
  [21,0.1, 8,13,0,0],
  [21,1.0, 8,13,0,0],
  [22,1.0, 9,13,0,0],
  [25,1.0, 13,12,0,0],
  [28,1.0, 16,12,0,0],
  [29,1.0, 17,11,1,0],
  [30,1.0, 17,11,2,0],
  [36,1.0, 18,12,6,0],
  [36,1.1, 17,12,7,0],
  [36,2.0, 14,13,9,0],
  [41,2.0, 15,14,12,0],

]

# ----------------------------------------------

# select active villager numbers
activeVillNumbers =  villNumbers["FF-SCOUT-FLUSH"]
if len(activeVillNumbers) < 2: raise Exception("villNumbers lists must have a length of at least 2")
if activeVillNumbers[0][0] != 0: raise Exception("villNumbers lists must start at time 0")

# age-up times (in units of villagers)
feudalTime = 5.2
castleTime = 6.4
imperialTime = 7.6

# convert first column to time
for i,r in enumerate(activeVillNumbers):

  if r[1] < 1.0:
    r[0] += (r[1] % 1.0) * feudalTime
  elif r[1] < 2.0:
    r[0] += (r[1] % 1.0) * castleTime + feudalTime
  elif r[1] < 3.0:
    r[0] += (r[1] % 1.0) * imperialTime + feudalTime + castleTime
  else:
    r[0] += feudalTime + castleTime + imperialTime

  r[0] *= 25.
  del r[1]

def getFinalVillNumbers(gameState):

  gameTime = gameState.gameTime+3*25
  villCount = gameState.done_units["villager"]

  if gameState.done_techs["loom"] > 0:
    gameTime -= 25

  if gameState.done_techs["wheelbarrow"] > 0:
    gameTime -= 75

  # get gameTime just above current
  i2 = 0
  while i2 < len(activeVillNumbers) and activeVillNumbers[i2][0] <= gameTime:
    i2 += 1
  if i2 == len(activeVillNumbers): i2 -= 1
  x2 = activeVillNumbers[i2][0]

  # get gameTime below/equal to current
  i1 = i2-1
  x1 = activeVillNumbers[i1][0]

  # get portion of each
  p = (gameTime-x1) / (x2-x1) # =1 when at larger time
  q = 1 - p # =1 when at lower time

  # linear interpolation
  result = { }

  result["food"] = activeVillNumbers[i1][1]*q + activeVillNumbers[i2][1]*p
  result["wood"] = activeVillNumbers[i1][2]*q + activeVillNumbers[i2][2]*p
  result["gold"] = activeVillNumbers[i1][3]*q + activeVillNumbers[i2][3]*p
  result["stone"] = activeVillNumbers[i1][4]*q + activeVillNumbers[i2][4]*p

  total = max(1,result["food"] + result["wood"] + result["stone"] + result["gold"])

  # rescale to give correct vill count
  result["food"] *= villCount / total
  result["wood"] *= villCount / total
  result["stone"] *= villCount / total
  result["gold"] *= villCount / total

  # Note: may be fractional at this stage
  return result

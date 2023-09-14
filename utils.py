import copy

def convertToSecs(time):

  return (time // 1)*60 + 100*(time % 1.0)

def initDict(listt, value):

  return { x:value for x in listt }

# TODO: delete later?
def argMinValue(dictt, func):

  if type(dictt) is dict:
    minValue = 1e50
    minKey = None

    for k,v in dictt.items():
      if func(v) < minValue:
        minValue = func(v)
        minKey = k

  else:
    minValue = 1e50
    minKey = -1

    for i,v in enumerate(dictt):
      if func(v) < minValue:
        minValue = func(v)
        minKey = i

  return minKey

def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z
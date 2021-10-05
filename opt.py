#Terminology: https://docs.google.com/document/d/1QFggZ8KRd4AHGsprd1xjd7-F5-7ZqMykGbkkwU6dMSY/edit?usp=sharing
from itertools import product
import numpy as np
import numpy as geek
import pandas as pd
from scipy.optimize import linprog
from pandas.io.stata import StataMissingValue
 
#PART 1: MENDEFINISIKAN INPUT
#1.1 INVENTORY   
def parseInputInventory(ingredientList, supplyList, priceList):
 supplyList = list(map(int, supplyList))
 priceList = list(map(int, priceList))
 data_inventory = {
   'Bahan': ingredientList,
   'Ai': supplyList,
   'Pi': np.divide(priceList, supplyList),
 }
 df_inventory = pd.DataFrame(data_inventory, columns=['Bahan', 'Pi', 'Ai'])
 return df_inventory
 
 
#1.2 RECIPE
def parseInputRecipe(productPerIngredientList, unitPerIngredientList, totalIngredientRows):
 data_recipe = {}
 for i in range(len(productPerIngredientList)):
   for j in range(len(productPerIngredientList[i])):
     productName = productPerIngredientList[i][j];
     if productName not in data_recipe:
       data_recipe[productName] = [0] * (totalIngredientRows - 1 )
     data_recipe[productName][i] = int(unitPerIngredientList[i][j])
 df_recipe = pd.DataFrame(data_recipe, columns=data_recipe.keys())
 return df_recipe


#1.3 SCORE REQUIREMENT
def parseScoreInput(productScoreList, demandScoreList, minSalesList, maxSalesList):
 minSalesList = list(map(int, minSalesList))
 demandScoreList = list(map(int, demandScoreList))
 maxSalesList = list(map(int, maxSalesList)) 
 data_score = {
   'Product': productScoreList,
   'Demand': demandScoreList, 
   'Smin': minSalesList, 
   'Smax': maxSalesList
 }
 df_score = pd.DataFrame(data_score, columns=['Product', 'Demand', 'Smin', 'Smax'])
 return df_score 


#1.5 PRODUCT COST 
def calculate(df_recipe, df_inventory, df_score):
  # Iterate over column names; c
  allProductCost = []
  for column in df_recipe:
      costColumns = df_recipe[column]
      Pi = df_inventory['Pi']
      cost = sum(costColumns.values * Pi)
      allProductCost.append(cost)
  
  #PART 2: DEFINING THE OBJECTIVE FUNCTION
  #2.2 AVAILABILITY FUNCTION
  #2.2.1 Total Usage Function per Row
  allProductUsage =[]
  for i in range(len(df_recipe.index)):
    row_values = []
    for j in range(len(df_recipe.columns)):
      cell_values = df_recipe.iloc[i,j]
      row_values.append(cell_values)
    allProductUsage.append(row_values)
  
  #2.2.2 Total Supply
  allIngredientSupply = np.array(df_inventory['Ai'])
  
  #2.3 SCORE REQUIREMENT FUNCTION
  #membagi semua score min jadi persentase
  score_min = []
  for i in range(len(df_score.index)):
    score_values = df_score.iloc[i, 2]
    score_min.append(score_values / 100)
  
  #membagi semua score max jadi persentase
  score_max = []
  for i in range(len(df_score.index)):
    score_values = df_score.iloc[i, 3]
    score_max.append(score_values / 100)


  #Minimum score requirement
  scoreRequire_min = []  
  for i in range(len(df_score.index)):
    #array anomali ada -1 nya
    #scoreReqA untuk array sebelum array anomali,
    #scoreReqB = array anomali
    #scoreReqC untuk array setelah anomali
    scoreReqA = []
    scoreReqB = []
    scoreReqC = []
    appendMinScore = score_min[i]
  
    scoreReqA.append(appendMinScore)
    tempA = np.array(np.repeat(scoreReqA, i))
    scoreRequire_min += [tempA]
  
    tempB = np.array(appendMinScore-1)
    scoreRequire_min += [tempB]
  
    scoreReqC.append(appendMinScore)
    tempC = np.array(np.repeat(scoreReqC, len(df_score.index) - i - 1))
    scoreRequire_min += [tempC]
  grand_min_array = np.array(scoreRequire_min, dtype=object)
  
  final_min_array = []
  for i in range(len(df_score.index) * 3):
    tempFinalArrayMin = grand_min_array[i].tolist()
    final_min_array.append(tempFinalArrayMin)
    

  #flatten function
  def flatten(list_of_lists):
    if len(list_of_lists) == 0:
        return list_of_lists
    if isinstance(list_of_lists[0], list):
        return flatten(list_of_lists[0]) + flatten(list_of_lists[1:])
    return list_of_lists[:1] + flatten(list_of_lists[1:])
  
  score_min_array = np.array(flatten(final_min_array))
  score_min_array = score_min_array.reshape(len(df_score.index), len(df_score.index))

  
  #Maximum score requirement
  scoreRequire_max = []  
  for i in range(len(df_score.index)):
    #array anomali ada -1 nya
    #scoreReqA untuk array sebelum array anomali,
    #scoreReqB = array anomali
    #scoreReqC untuk array setelah anomali
    scoreMaxReqA = []
    scoreMaxReqB = []
    scoreMaxReqC = []
    appendMaxScore = score_max[i]
  
    scoreMaxReqA.append(appendMaxScore)
    tempMaxA = np.array(np.repeat(scoreMaxReqA, i))
    scoreRequire_max += [tempMaxA]
  
    tempMaxB = np.array(1-appendMaxScore)
    scoreRequire_max += [tempMaxB]
  
    scoreMaxReqC.append(appendMaxScore)
    tempMaxC = np.array(np.repeat(scoreMaxReqC, len(df_score.index) - i - 1))
    scoreRequire_max += [tempMaxC]
    grand_max_array = np.array(scoreRequire_max, dtype=object)
  
  final_max_array = []
  for i in range(len(df_score.index) * 3):
    tempFinalArrayMax = grand_max_array[i].tolist()
    final_max_array.append(tempFinalArrayMax)

  score_max_array = np.array(flatten(final_max_array))
  score_max_array = score_max_array.reshape(len(df_score.index), len(df_score.index))

  #DEFINING THE CONSTRAINT INEQUALITIES - COMBINING ALL THE INEQUALITY ARRAYS
  #Getting left inequality
  left_ineq = []
  left_ineq.append(allProductUsage)
  left_ineq.append(score_min_array)
  left_ineq.append(score_max_array)

  final_left_ineq = np.array(left_ineq)
  final_left_ineq = final_left_ineq.reshape(len(score_max_array) + len(score_min_array) + len(allProductUsage), len(df_score.index))

  #Getting right inequality
  right_ineq = [allIngredientSupply, np.array([0] * len(df_score.index)*2)]
  final_right_ineq=[]
  for sublist in right_ineq:
    for element in sublist:
        final_right_ineq.append(element)

  #2.4 DEMAND FUNCTION (BOUNDS)
  demand_array = []
  for i in range(len(df_score.index)):
    demand_array += [[df_score.iloc[i, 1], float("inf")]]

  # 2.5 OBJECTIVE FUNCTION
  res = linprog(c = allProductCost, A_ub = final_left_ineq, b_ub = final_right_ineq, bounds = demand_array)

  final = [res['message'],res['x']]
  
  # final1 = tempFinal.reshape(1, (len(df_recipe.columns)))
  print(final)
  return final
  

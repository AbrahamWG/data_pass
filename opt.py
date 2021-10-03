#Terminology: https://docs.google.com/document/d/1QFggZ8KRd4AHGsprd1xjd7-F5-7ZqMykGbkkwU6dMSY/edit?usp=sharing
from itertools import product
import numpy as np
import pandas as pd
from pandas.io.stata import StataMissingValue

#PART 1: DEFINING THE TABLES/DATASET

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
  print(productPerIngredientList)
  for i in range(len(productPerIngredientList)):
    print(len(productPerIngredientList[i]))
    for j in range(len(productPerIngredientList[i])):
      productName = productPerIngredientList[i][j];
      if productName not in data_recipe:
        data_recipe[productName] = [0] * (totalIngredientRows - 1 )
      print(productName, i,j)
      print(data_recipe[productName])
      data_recipe[productName][i] = int(unitPerIngredientList[i][j])
  df_recipe = pd.DataFrame(data_recipe, columns=data_recipe.keys())
  return df_recipe

def parseScoreInput(productScoreList, demandScoreList, minSalesList, maxSalesList):
  print(productScoreList, demandScoreList, minSalesList, maxSalesList)
  minSalesList = list(map(int, minSalesList))
  demandScoreList = list(map(int, demandScoreList))
  maxSalesList = list(map(int, maxSalesList))


  print(productScoreList, demandScoreList, minSalesList, maxSalesList)
  data_score = {
    'Product': productScoreList,
    'Demand': demandScoreList,  
    'Smin': minSalesList,  
    'Smax': maxSalesList
  }
  df_score = pd.DataFrame(data_score, columns=['Product', 'Demand', 'Smin', 'Smax'])
  return df_score  
# #1.3 SCORE & DEMAND REQUIREMENT

#TODO: df_sq & df_dmd yg perlu di adjust
def calculate(df_recipe, df_inventory, df_sq):

  #1.5 CALCULATING THE COST OF EACH PRODUCT
  a1 = np.array(df_recipe['a1(Milk Tea)'])
  a2 = np.array(df_recipe['a2(Strawberry Tea)'])
  a3 = np.array(df_recipe['a3(Mango Tea)'])
  a4 = np.array(df_recipe['a4(Apple Tea)'])
  Pi = np.array(df_inventory['Pi'])

  cost1 = sum(a1*Pi)
  cost2 = sum(a2*Pi)
  cost3 = sum(a3*Pi)
  cost4 = sum(a4*Pi)

  #PART 2: DEFINING THE OBJECTIVE FUNCTION
  from scipy.optimize import linprog

  #2.1 COEFFICIENT FOR THE DECISION VARIABLES
  c =  [cost1, cost2, cost3, cost4]

  #2.2 AVAILABILITY FUNCTION
  #2.2.1 Total Usage Function
  sig_a1 = np.array(df_recipe.iloc[0,:4])
  sig_a2 = np.array(df_recipe.iloc[1,:4])
  sig_a3 = np.array(df_recipe.iloc[2,:4])
  sig_a4 = np.array(df_recipe.iloc[3,:4])
  sig_a5 = np.array(df_recipe.iloc[4,:4])
  sig_a6 = np.array(df_recipe.iloc[5,:4])
  sig_a7 = np.array(df_recipe.iloc[6,:4])
  sig_a8 = np.array(df_recipe.iloc[7,:4])
  sig_a9 = np.array(df_recipe.iloc[8,:4])
  sig_a10 = np.array(df_recipe.iloc[9,:4])
  sig = [sig_a1, sig_a2, sig_a3, sig_a4, sig_a5, sig_a6, sig_a7, sig_a8, sig_a9, sig_a10]

  #2.2.2 Total Stock Function
  s1 = df_inventory.iloc[0,2]
  s2 = df_inventory.iloc[1,2]
  s3 = df_inventory.iloc[2,2]
  s4 = df_inventory.iloc[3,2]
  s5 = df_inventory.iloc[4,2]
  s6 = df_inventory.iloc[5,2]
  s7 = df_inventory.iloc[6,2]
  s8 = df_inventory.iloc[7,2]
  s9 = df_inventory.iloc[8,2]
  s10 = df_inventory.iloc[9,2]

  #2.3 SCORE REQUIREMENT FUNCTION
  #2.3.1 Parameters
  smin1 = df_sq.iloc[0,1]
  smin2 = df_sq.iloc[1,1]
  smin3 = df_sq.iloc[2,1]
  smin4 = df_sq.iloc[3,1]
  smax1 = df_sq.iloc[0,2]
  smax2 = df_sq.iloc[1,2]
  smax3 = df_sq.iloc[2,2]
  smax4 = df_sq.iloc[3,2]

  #2.3.2 Coefficients for SQ Inequalities 
  sqmin1 = [smin1-1, smin1, smin1, smin1]
  sqmin2 = [smin2, smin2-1, smin2, smin2]
  sqmin3 = [smin3, smin3, smin3-1, smin3]
  sqmin4 = [smin4, smin4, smin4, smin4-1]
  sqmax1 = [smax1-1, smax1, smax1, smax1]
  sqmax2 = [smax2, smax2-1, smax2, smax2]
  sqmax3 = [smax3, smax3, smax3-1, smax3]
  sqmax4 = [smax4, smax4, smax4, smax4-1]

  #2.3.3 Defining the Constraint Inequalities
  lhs_ineq = [sig_a1.tolist(), 
  sig_a2.tolist(), 
  sig_a3.tolist(), 
  sig_a4.tolist(), 
  sig_a5.tolist(), 
  sig_a6.tolist(), 
  sig_a7.tolist(), 
  sig_a8.tolist(), 
  sig_a9.tolist(), 
  sig_a10.tolist(), 
  sqmin1, sqmin2, sqmin3, sqmin4, 
  sqmax1, sqmax2, sqmax3, sqmax4]

  rhs_ineq =  [s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, 0, 0, 0, 0, 0, 0, 0, 0
  ]

  #2.4 DEMAND FUNCTION (BOUNDS)
  dmd1 = [float(df_dmd.iloc[0,1]), float("inf")]
  dmd2 = [float(df_dmd.iloc[1,1]), float("inf")]
  dmd3 = [float(df_dmd.iloc[2,1]), float("inf")]
  dmd4 = [float(df_dmd.iloc[3,1]), float("inf")]
  bounds_final = [dmd1, dmd2, dmd3, dmd4]

  #2.5 OBJECTIVE FUNCTION
  res = linprog(c, A_ub = lhs_ineq, b_ub = rhs_ineq, bounds = bounds_final)
  return res







import numpy as np
import pandas as pd
from pandas.io.stata import StataMissingValue

#PART 1: DEFINING THE TABLES/DATASET
#1.1 INVENTORY
data_inventory = {'Bahan': ['Ice', 'Water', 'Tea', 'Milk', 'Gula Merah', 'Gula Putih', 'Syrup', 'Strawberry', 'Mango', 'Apple'],
'Pi': [125, 2, 1500, 20, 16, 13, 40, 20, 20, 20],
'Ai': [10000, 500000, 2000, 400000, 50000, 50000, 100000, 50000, 50000, 50000]
} 
df_inventory = pd.DataFrame(data_inventory, columns=['Bahan', 'Pi', 'Ai']) 

#1.2 RECIPE
data_recipe = {'⍺1(Milk Tea)': [2, 300, 1, 200, 150, 30, 25, 0, 0, 0],
'⍺2(Strawberry Tea)': [8, 300, 1, 100, 100, 40, 50, 20, 0, 0],
'⍺3(Mango Tea)': [8, 300, 1, 0, 100, 40, 50, 0, 20, 0],
'⍺4(Apple Tea)': [8, 300, 1, 100, 150, 35, 50, 0, 0, 20]
}
df_recipe = pd.DataFrame(data_recipe, columns=['⍺1(Milk Tea)', '⍺2(Strawberry Tea)', '⍺3(Mango Tea)', '⍺4(Apple Tea)'])

#1.3 SCORE REQUIREMENT
data_sq = {'Product': ['Milk Tea', 'Strawberry Tea', 'Mango Tea', 'Apple Tea'],
'Smin': [20, 20, 20, 10],  
'Smax': [60, 70, 60, 30]
}
df_sq = pd.DataFrame(data_sq, columns=['Product', 'Smin', 'Smax'])

#1.4 DEMAND FUNCTION
data_dmd = {'Product': ['Milk Tea', 'Strawberry Tea', 'Mango Tea', 'Apple Tea'],
'Min Order/Week': [10, 20, 30, 40],  
}
df_dmd = pd.DataFrame(data_dmd, columns=['Product', 'Min Order/Week'])

#1.5 CALCULATING THE COST OF EACH PRODUCT
a1 = np.array(df_recipe['⍺1(Milk Tea)'])
a2 = np.array(df_recipe['⍺2(Strawberry Tea)'])
a3 = np.array(df_recipe['⍺3(Mango Tea)'])
a4 = np.array(df_recipe['⍺4(Apple Tea)'])
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
print(res)






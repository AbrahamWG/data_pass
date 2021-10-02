import numpy as np
import pandas as pd
from scipy.optimize import linprog
from pandas.io.stata import StataMissingValue
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_value():
    #ambil data ingredient, unit cost dan supply
    #Pi = unit cost -> total price dibagi supply yang ada, Ai = total supply
    data_inventory = {
        'Bahan': request.form.getlist['ingredient[]'],
        'Ai': request.form.getlist['supply[]'],
        'Pi': request.form.getlist['price[] // supply[]']
        } 
    
    #assign tiap option value dari product recipe list pada satu variable
    data_recipe = {

    }

    #assign tiap product pada score min dan max nya masing-masing
    data_score_requirement = {
        'Minimum' : request.form.getlist['minimum[]'],
        'Maximum' : request.form.getlist['maximum[]'],
    }


    return '''<h1>The data value is: {}</h1>'''.format(data_inventory)

if __name__ == "__main__":
    app.run()

 
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_value():
    Ingredients = request.form['Ingredients']
    Quantity = request.form['Quantity']
    Price = request.form['Price']
    return render_template('pass.html', i=Ingredients, q=Quantity, p=Price)

app.run()
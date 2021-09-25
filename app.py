from flask import Flask, render_template, request

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_value():
    Ingredients = request.form['Ingredients']
    Quantity = request.form['Quantity']
    Price = request.form['Price']
    return render_template('pass.html', i=Ingredients, q=Quantity, p=Price)

if __name__ == "__main__":
    app.run()
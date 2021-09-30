from flask import Flask, render_template, request

app = Flask(__name__, template_folder='template')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def get_value():
    print('listnya', request.form.getlist('ingredient[]'))
    print('value pertamanya', request.form.getlist('ingredient[]')[0])
    return render_template('pass.html')

if __name__ == "__main__":
    app.run()
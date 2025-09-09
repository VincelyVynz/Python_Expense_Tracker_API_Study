from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def working():
    return "Expense Tracker API is working."



if __name__ == '__main__':
    app.run(debug=True, port=5000)

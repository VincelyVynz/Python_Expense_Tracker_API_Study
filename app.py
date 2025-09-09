from flask import Flask, jsonify
import sqlite3
app = Flask(__name__)
@app.route('/')
def working():
    return "Expense Tracker API is working."

#new route for expenses
@app.route('/expenses')
def expenses():
    conn = sqlite3.connect('expense_tracker.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    all_expenses = cursor.fetchall()
    expense_json = []
    for row in all_expenses:
        expense_json.append({"id": row[0], "item": row[1], "amount": row[2], "category": row[3], "date": row[4]})
    conn.close()
    return jsonify(expense_json)




if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, jsonify, request
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

@app.route('/expenses', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        # #validation
        if 'item' not in data or not isinstance(data['item'], str) or data['item'].strip() == "":
            return jsonify({'error': "Invalid or missing 'item'"}), 400

        if 'amount' not in data or not (isinstance(data['amount'], int) or isinstance(data['amount'], float)) or data[
            'amount'] <= 0:
            return jsonify({'error': "Invalid or missing 'amount'"}), 400

        if 'category' not in data or not isinstance(data['category'], str) or data['category'].strip() == "":
            return jsonify({'error': "Invalid or missing 'category'"}), 400

        if 'date' not in data or not isinstance(data['date'], str) or data['date'].strip() == "":
            return jsonify({'error': "Invalid or missing 'date'"}), 400

        item = data['item']
        amount = data['amount']
        category = data['category']
        date = data['date']
        conn = sqlite3.connect('expense_tracker.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO expenses (item, amount, category, date) VALUES (?,?,?,?)", (item, amount, category, date))
        conn.commit()
        conn.close()
        return jsonify({"message": "Expense added successfully"}), 201

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': "Something went wrong"}), 500

@app.route('/expenses/<int:id>', methods=['PUT'])
def update_expenses(id):
    data = request.get_json()
    if not data:
        return jsonify({'error': "Invalid or missing request."}), 400

    try:
        item = data['item']
        amount = data['amount']
        category = data['category']
        date = data['date']

    except KeyError as e:
        return jsonify({'error': f"Invalid or missing: {e}"}), 400

    conn = None

    try:
        conn = sqlite3.connect('expense_tracker.db')
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE expenses
        SET item= ?, amount = ?, category = ?, date = ?
        WHERE id = ?
        """, (item, amount, category, date, id))

        if cursor.rowcount == 0:
            return jsonify({'error': "Expense not found"}), 404
        else:
            conn.commit()
            return jsonify({"message": "Expense updated successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({'error': f"Something went wrong: {e}"}), 500

    finally:
        if conn:
            conn.close()


@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expenses(id):
    conn = None
    try:
        conn = sqlite3.connect('expense_tracker.db')
        cursor = conn.cursor()
        cursor.execute("""
        DELETE FROM expenses
        WHERE id = ?
        """, (id,))
        if cursor.rowcount == 0:
            return jsonify({'error': "Expense not found"}), 404
        else:
            conn.commit()
            return jsonify({"message": "Expense deleted successfully"}), 200

    except sqlite3.Error as e:
        return jsonify({'error': f"Something went wrong: {e}"}), 500
    finally:
        if conn:
            conn.close()



if __name__ == '__main__':
    app.run(debug=True, port=5000)

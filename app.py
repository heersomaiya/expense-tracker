from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
from bson.objectid import ObjectId


#loading environment variables from .env file
load_dotenv(override=True)

app = Flask(__name__)

#MongoDB connection
client = MongoClient(
    os.getenv("MONGO_URI"),
    tls=True,
    tlsCAFile=certifi.where()
)

#selecting the database
db = client["expense_tracker"]

#selecting the collection
expenses = db['expenses']

@app.route('/')
def home():
    all_expenses = expenses.find().sort("date", -1) # Sort expenses by date in descending order

    return render_template('index.html', expenses=all_expenses)

@app.route("/add", methods=['POST'])
def add_expense():
    amount = request.form['amount']
    category = request.form['category']
    description = request.form['description']
    date = request.form['date']

    expense = {
        "amount" : float(amount),
        "category" : category,
        "description" : description,
        "date" : date
    }

    expenses.insert_one(expense)

    return redirect('/')

@app.route("/delete/<id>")
def delete_expense(id):

    expenses.delete_one(
        {"_id" : ObjectId(id)}
    )

    return redirect('/')

@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit_expense(id):

    if request.method == 'POST':
        
        amount = request.form['amount']
        category = request.form['category']
        description = request.form['description']
        date = request.form['date']

        expenses.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "amount": float(amount),
                "category": category,
                "description": description,
                "date": date
            }}
        )

        return redirect('/')

    expense = expenses.find_one({"_id": ObjectId(id)})

    return render_template('edit.html', expense=expense)

if __name__ == '__main__':
    app.run(debug=True)
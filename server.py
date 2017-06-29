from flask import Flask, render_template, redirect, request, session, flash
import re
from mysqlconnection import MySQLConnector

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
app = Flask(__name__)
app.secret_key = "MermaidsAreReal"
mysql = MySQLConnector(app, 'fullFriends')

@app.route('/')
def indext():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', friends = friends)

@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/edit', methods=['POST'])
def edit(id):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {
        'id': id
    }
    friend = mysql.query_db(query, data)
    return render_template('edit.html', friend = friend[0])

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id"
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/friends/<id>/delete', methods=['POST'])
def delete(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {
        'id': id
    }
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)

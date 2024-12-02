from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB connection
client = MongoClient(os.getenv('MONGODB_URI'))
db = client.movie_catalog

# Collections
movies = db.movies
ratings = db.ratings
users = db.users

@app.route('/')
def index():
    return render_template('index.html')

# Movies CRUD
@app.route('/movies')
def list_movies():
    all_movies = list(movies.find())
    return render_template('movies/list.html', movies=all_movies)

@app.route('/movies/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        movie = {
            'title': request.form['title'],
            'genre': request.form['genre'],
            'release_year': int(request.form['release_year']),
            'description': request.form['description']
        }
        movies.insert_one(movie)
        return redirect(url_for('list_movies'))
    return render_template('movies/add.html')

@app.route('/movies/edit/<id>', methods=['GET', 'POST'])
def edit_movie(id):
    if request.method == 'POST':
        movies.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'title': request.form['title'],
                'genre': request.form['genre'],
                'release_year': int(request.form['release_year']),
                'description': request.form['description']
            }}
        )
        return redirect(url_for('list_movies'))
    movie = movies.find_one({'_id': ObjectId(id)})
    return render_template('movies/edit.html', movie=movie)

@app.route('/movies/delete/<id>')
def delete_movie(id):
    movies.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('list_movies'))

# Ratings CRUD
@app.route('/ratings')
def list_ratings():
    all_ratings = list(ratings.find())
    
    # Додаємо імена фільмів та користувачів до рейтингів
    for rating in all_ratings:
        movie = movies.find_one({'_id': rating['movie_id']})
        user = users.find_one({'_id': rating['user_id']})
        rating['movie_title'] = movie['title'] if movie else 'Не знайдено'
        rating['user_name'] = user['name'] if user else 'Анонім'
    
    return render_template('ratings/list.html', ratings=all_ratings)

@app.route('/ratings/add', methods=['GET', 'POST'])
def add_rating():
    if request.method == 'POST':
        rating = {
            'movie_id': ObjectId(request.form['movie_id']),
            'user_id': ObjectId(request.form['user_id']),
            'rating': int(request.form['rating']),
            'comment': request.form['comment'],
            'date': datetime.utcnow()
        }
        ratings.insert_one(rating)
        return redirect(url_for('list_ratings'))
    all_movies = list(movies.find())
    all_users = list(users.find())
    return render_template('ratings/add.html', movies=all_movies, users=all_users)
@app.route('/ratings/edit/<id>', methods=['GET', 'POST'])
def edit_rating(id):
    if request.method == 'POST':
        ratings.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'movie_id': ObjectId(request.form['movie_id']),
                'user_id': ObjectId(request.form['user_id']),
                'rating': int(request.form['rating']),
                'comment': request.form['comment'],
                'date': datetime.utcnow()  # дата оновлення рейтингу
            }}
        )
        return redirect(url_for('list_ratings'))

    # Отримуємо рейтинг за його id
    rating = ratings.find_one({'_id': ObjectId(id)})
    
    # Отримуємо список фільмів і користувачів для заповнення форм
    all_movies = list(movies.find())
    all_users = list(users.find())

    return render_template('ratings/edit.html', rating=rating, movies=all_movies, users=all_users)

@app.route('/ratings/delete/<id>')
def delete_rating(id):
    ratings.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('list_ratings'))


# Users CRUD
@app.route('/users')
def list_users():
    all_users = list(users.find())
    return render_template('users/list.html', users=all_users)

@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password']
        }
        users.insert_one(user)
        return redirect(url_for('list_users'))
    return render_template('users/add.html')

@app.route('/users/edit/<id>', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        users.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'name': request.form['name'],
                'email': request.form['email'],
                'password': request.form['password']
            }}
        )
        return redirect(url_for('list_users'))
    user = users.find_one({'_id': ObjectId(id)})
    return render_template('users/edit.html', user=user)

@app.route('/users/delete/<id>')
def delete_user(id):
    users.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('list_users'))

if __name__ == '__main__':
    app.run(debug=True)

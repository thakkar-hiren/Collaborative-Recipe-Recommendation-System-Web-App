from flask import Flask, render_template, request, redirect, url_for
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np


app = Flask(__name__)

final_ratings = pd.read_csv('/Users/drashti/Documents/Mtech[Sem2]/Item_Item_Flask_App/final_ratings.csv')
train_data,test_data = train_test_split(final_ratings, test_size=0.2)
train_pt = train_data.pivot_table(index='name', columns='user_id', values='rating')
similarity_scores = cosine_similarity(train_pt.fillna(0))

def get_top_k_recommendations(user_id, k, rated_items=[]):
    """
    Get top k recommendations for a given user ID.

    Arguments:
        user_id (int): ID of the user for whom to make recommendations.
        k (int): Number of top recommendations to return.
        rated_items (list): List of tuples of (recipe_name, rating) for recipes
            rated by the user in previous rounds. Default is an empty list.

    Returns:
        list: List of top k recommended recipe names for the user.
    """
    if user_id not in train_pt.columns:
        return []
    print(user_id)
    # update user's ratings with rated items from previous rounds
    for recipe_name, rating in rated_items:
        if recipe_name in train_pt.index:
            train_pt[user_id][recipe_name] = rating

    rated_recipes = train_pt[user_id]
    print(rated_recipes)
    rated_recipes = rated_recipes[rated_recipes.notna()]
    unrated_recipes = train_pt.index.difference(rated_recipes.index)
    predicted_ratings = []

    for recipe_name in unrated_recipes:
        similarity_scores_for_recipe = similarity_scores[train_pt.index.get_loc(recipe_name)]
        user_ratings = train_pt[user_id].fillna(0)
        numerator = (user_ratings * similarity_scores_for_recipe).sum()
        denominator = similarity_scores_for_recipe.sum()

        if denominator == 0:
            predicted_rating = 0
        else:
            predicted_rating = numerator / denominator

        predicted_ratings.append((recipe_name, predicted_rating))
        
    top_recipe_names = [recipe_name for recipe_name, predicted_rating in sorted(predicted_ratings, key=lambda x: x[1], reverse=True)[:k]]
    return top_recipe_names

# define route for login page
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # check if user_id and password match
        user_id = request.form['user_id']
        password = request.form['password']
        if user_id == password:
            return redirect(url_for('recommendations', user_id=int(user_id)))
        else:
            error = 'Invalid credentials'
    return render_template('login.html', error=error)


# define route for recommendation page
@app.route('/recommendations/<user_id>', methods=['GET', 'POST'])
def recommendations(user_id):
    # define parameters for recommendation system
    k = 5
    rated_items = []

    if request.method == 'POST':
        # get selected item and rating from form
        selected_item = request.form['selected_item']
        rating = float(request.form['rating'])
        rated_items.append((selected_item, rating))
        
        # check if user is satisfied
        if request.form['satisfied'] == 'yes':
            # get ingredients of selected item and display to user
            ingredients = final_ratings[final_ratings['name'] == selected_item]['ingredients'].values[0]
            print(ingredients)
            return render_template('ingredients.html', recipe=selected_item, ingredients=ingredients)

    # get top k recommendations for user
    user_id = int(user_id)
    recommendations = get_top_k_recommendations(user_id, k, rated_items)
    print(recommendations)
    # render template for recommendation page
    return render_template('recommendations.html', user_id=user_id, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
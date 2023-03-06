# Collaborative-Recipe-Recommendation-System-Web-App
This is a Flask application that provides recipe recommendations to users based on their previous ratings. The recommendations are generated using item-item collaborative filtering technique. The application requires a dataset of recipes with user ratings and ingredients to provide recommendations.

## Prerequisites
* Python
* Flask
* Pandas
* NumPy
* scikit-learn

## Installation
1. Clone the repository to your local machine.
```
git clone https://github.com/thakkar-hiren/Collaborative-Recipe-Recommendation-System-Web-App.git
```

2. Install the required packages using pip.
```python
pip install flask
pip install pandas
pip install numpy
pip install scikit-learn
```

## Usage
1. Navigate to the cloned repository on your local machine.
```
cd Collaborative-Recipe-Recommendation-System-Web-App
```
2. Run the Flask application.
```Python
python app.py
```
3. Open a web browser and go to http://localhost:5000.
4. Login with your user ID and password.
5. Rate the recommended recipes and indicate whether you are satisfied with the recommendations.
6. If you are satisfied with the recommendations, the ingredients of the selected recipe will be displayed.
7. The application will provide more recommendations based on your ratings.

## File Structure
* `app.py`: This file contains the Flask application and the recommendation system.
* `final_ratings.csv`: This file contains the dataset of recipes with user ratings and ingredients.
* `templates`: This folder contains the HTML templates for the web pages.

## References
* <a href="https://flask.palletsprojects.com/en/2.2.x/">Flask</a>
* <a href="https://pandas.pydata.org/">Pandas</a>
* <a href="https://numpy.org/">NumPy</a>
* <a href="https://scikit-learn.org/">scikit-learn</a>

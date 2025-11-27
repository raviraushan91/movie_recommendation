from flask import Flask, request, jsonify
from flask_cors import CORS      # ADD THIS
import pickle

app = Flask(__name__)
CORS(app)                        # ADD THIS (allow all origins)

# Load files
movies = pickle.load(open("movie_list.pkl", "rb"))
cv = pickle.load(open("vectorizer.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.json['movie']

    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]

    movie_list = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]

    recommended = []
    for i in movie_list:
        recommended.append(movies.iloc[i[0]].title)

    return jsonify({"recommendations": recommended})

if __name__ == '__main__':
    app.run(debug=True)

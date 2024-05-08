from flask import Flask,request,render_template,jsonify
import pandas as pd
import pickle
import requests


application = Flask(__name__)
app = application

## arjun singh 
movies  = pickle.load(open(r'E:\Movie Recommendation System\artifacts\movie.pkl','rb'))
similarity = pickle.load(open(r'E:\Movie Recommendation System\artifacts\similarity.pkl','rb'))

def fetch_poster(movie_id):
    responce = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = responce.json()
    return  "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(selected_movie_namse):

    index = movies[movies['title'] == selected_movie_namse].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])

    recommend_movie = []
    recommend_movie_poster = []
    for i in distances[1:10]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movie_poster.append(fetch_poster(movie_id))
        recommend_movie.append(movies.iloc[i[0]].title)
    
    return recommend_movie,recommend_movie_poster


@app.route('/')
def homepage():
    return render_template('homepage.html')

if __name__=='__main__':
    app.run(host='0.0.0.0',debug=True)



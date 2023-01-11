import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import base64
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('movies_hp.csv')
df_movies_nlp = pd.read_csv('df_movies_nlp.csv')

# replace nan values with empty string from df_movies_nlp
df_movies_nlp = df_movies_nlp.fillna('')

filtered_df = df
random_movie = None
selected_genres = []
liked_movies = pd.DataFrame(columns=["Title"])
disliked_movies = pd.DataFrame(columns=["Title"])

# Create the app object with bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

# Action
with open('icons/action.jpg', 'rb') as f:
    image_action = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Adventure
with open('icons/adventure.png', 'rb') as f:
    image_adventure = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Animation
with open('icons/animation2.png', 'rb') as f:
    image_animation = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))
 
# Comedy
with open('icons/comedy.jpg', 'rb') as f:
    image_comedy = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Crime
with open('icons/crime.jpg', 'rb') as f:
    image_crime = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Documentary
with open('icons/documentary.jpg', 'rb') as f:
    image_documentary = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Drama
with open('icons/drama.jpg', 'rb') as f:
    image_drama = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Family
with open('icons/family2.png', 'rb') as f:
    image_family = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Fantasy
with open('icons/fantasy.jpg', 'rb') as f:
    image_fantasy = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# History
with open('icons/history.jpg', 'rb') as f:
    image_history = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Horror
with open('icons/horror.jpg', 'rb') as f:
    image_horror = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Music
with open('icons/music.jpg', 'rb') as f:
    image_music = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Mystery
with open('icons/mystery.jpg', 'rb') as f:
    image_mystery = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Romance
with open('icons/romance.jpg', 'rb') as f:
    image_romance = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Scifi
with open('icons/scifi.jpg', 'rb') as f:
    image_scifi = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# thriller
with open('icons/thriller.jpg', 'rb') as f:
    image_thriller = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# TV Movie
with open('icons/tv_movie.png', 'rb') as f:
    image_tvmovie = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# War
with open('icons/war.jpg', 'rb') as f:
    image_war = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Western
with open('icons/western.jpg', 'rb') as f:
    image_western = 'data:image/png;base64,{}'.format(base64.b64encode(f.read()).decode('utf-8'))

# Navigation
nav_menu = dbc.Navbar(
    children = [
        dbc.Nav([
                dbc.NavItem(dbc.NavLink('Instructions', href='/instructions')),
                dbc.NavItem(dbc.NavLink('Select Genres', href='/select-genres')),
                dbc.NavItem(dbc.NavLink('Tinder', href='/tinder')),
                dbc.NavItem(dbc.NavLink('Recommendations', href='/recommendations')),
            ],
            vertical = False,
        ),
    ],
    color = 'primary',
    dark = True,
    className = 'mb-5 justify-content-center',
)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content', style = {'textAlign': 'center', 'font-family': 'Arial'}),
])

# Create Layout for page 1
page_1_layout = html.Div(
    children = [
        nav_menu,
        html.H1('Select your favorite genres', style = {'margin-bottom': 15}),
        html.H4('Select as many as you want', style = {'margin-bottom': 15}),
        dcc.Checklist(
            style = {'max-height': 400, 'max-width': 400, 'overflow': 'auto', 'margin-left': 'auto', 'margin-right': 'auto', 'background-color': '#f8f9fa'},
            id = 'checklist',   
            labelStyle = {'display': 'block'},
            options = [
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_action, style = {'height': 50, 'width': 50}),
                            html.Div('Action', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ], style = {'display': 'inline-block', 'margin-bottom': 15}
                    ),
                    'value': 'Action'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_adventure, style = {'height': 50, 'width': 50}),
                            html.Div('Adventure', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ], style = {'display': 'inline-block', 'margin-bottom': 15}
                    ),
                    'value': 'Adventure'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_animation, style = {'height': 50, 'width': 50}),
                            html.Div('Animation', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ], style = {'display': 'inline-block', 'margin-bottom': 15}
                    ),
                    'value': 'Animation'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_comedy, style = {'height': 50, 'width': 50}),
                            html.Div('Comedy', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ),
                    'value': 'Comedy'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_crime, style = {'height': 50, 'width': 50}),
                            html.Div('Crime', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Crime'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_documentary, style = {'height': 50, 'width': 50}),
                            html.Div('Documentary', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Documentary'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_drama, style = {'height': 50, 'width': 50}),
                            html.Div('Drama', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Drama'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_fantasy, style = {'height': 50, 'width': 50}),
                            html.Div('Fantasy', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Fantasy'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_family, style = {'height': 50, 'width': 50}),
                            html.Div('Family', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Family'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_history, style = {'height': 50, 'width': 50}),
                            html.Div('History', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'History'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_horror, style = {'height': 50, 'width': 50}),
                            html.Div('Horror', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Horror'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_music, style = {'height': 50, 'width': 50}),
                            html.Div('Music', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Music'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_mystery, style = {'height': 50, 'width': 50}),
                            html.Div('Mystery', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Mystery'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_romance, style = {'height': 50, 'width': 50}),
                            html.Div('Romance', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Romance'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_scifi, style = {'height': 50, 'width': 50}),
                            html.Div('Science Fiction', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Science Fiction'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_tvmovie, style = {'height': 50, 'width': 50}),
                            html.Div('TV Movie', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'TV Movie'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_thriller, style = {'height': 50, 'width': 50}),
                            html.Div('Thriller', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Thriller'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_war, style = {'height': 50, 'width': 50}),
                            html.Div('War', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'War'
                },
                {
                    'label': html.Div(
                        [
                            html.Img(src = image_western, style = {'height': 50, 'width': 50}),
                            html.Div('Western', style = {'font-size': 18, 'display': 'inline-block', 'margin-left': 5}),
                        ],  style = {'display': 'inline-block', 'margin-bottom': 15}
                    ), 
                    'value': 'Western'
                },
            ],
            value = []
        ),
        html.Div(
            id = 'selected_genres', 
            style = {'margin-top': '20px'}
        ),
        dcc.Link(dbc.Button(
            'Start',
            id = 'start-button',
            n_clicks = 0, 
            style = {'margin-top': '20px'}),
            href = "/tinder"),
    ]
)

@app.callback(
    Output('selected_genres', 'children'),
    [Input('checklist', 'value')])
def update_output(value):
    global selected_genres
    global filtered_df
    selected_genres = value
    text = 'You have selected {}'.format(value)
    filtered_df = df[df['genres'].str.contains('|'.join(selected_genres),na=False)]
    return text

# Page for Tinder - Like or dislike movies
page_2_layout = html.Div(
    children = [
        nav_menu,
        html.Img(id='movie-poster', style = {'margin-top': '20px'}, height = '300px'),
        html.Div([
            html.H2(id='movie-title', style = {'margin-top': '20px'}),
            html.P(id='movie-overview', style = {'margin-top': '20px', 'margin-left': '15%', 'margin-right': '15%'}),
            dbc.Button('Like', id='like-button', style = {'margin-right': '10px'}, color = 'success'),
            dbc.Button('Have-not seen', id='not_seen-button', color = 'secondary'),
            dbc.Button('Dislike', id = 'dislike-button', style = {'margin-left': '10px'}, color = 'danger')            
        ]),
        dcc.Link(dbc.Button(
            'Go to Recommendations',
            id = 'recommendations-button',
            n_clicks = 0, 
            style = {'margin-top': '40px', 'display': 'none'}),
            href = "/recommendations"),
])

@app.callback(
    [Output(component_id='movie-poster', component_property='src'),
     Output(component_id='movie-title', component_property='children'),
     Output(component_id='movie-overview', component_property='children')],
    [Input('like-button', 'n_clicks_timestamp'),
     Input('dislike-button', 'n_clicks_timestamp'),
     Input('not_seen-button', 'n_clicks_timestamp')]
)
def update_image(like_clicks, dislike_clicks, not_seen_clicks):
    global filtered_df
    global random_movie

    if random_movie is not None:
        title = random_movie['title'].values[0]

        if not_seen_clicks is None:
            not_seen_clicks = -1

        if like_clicks is None:
            like_clicks = -1

        if dislike_clicks is None:
            dislike_clicks = -1

        if not_seen_clicks > like_clicks and not_seen_clicks > dislike_clicks:
            pass

        elif like_clicks > dislike_clicks:
            global liked_movies
            liked_movies = liked_movies.append({"Title": title}, ignore_index=True)

        elif dislike_clicks > like_clicks:
            global disliked_movies
            disliked_movies = disliked_movies.append({"Title": title}, ignore_index=True)
    
    random_movie = filtered_df.sample(1) 
    poster_url = random_movie['backdrop_path'].values[0]

    if type(poster_url) != str:
        poster_url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'

    else:
        poster_url = 'https://www.themoviedb.org/t/p/original'+ poster_url
        
    title = random_movie['title'].values[0]
    overview = random_movie['overview'].values[0]

    return poster_url, title, overview

@app.callback(
    Output('like-button', 'children'),
    [Input('like-button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks is None:
        return 'Like'
    else:
        return 'Like ({})'.format(n_clicks)

@app.callback(
    Output('dislike-button', 'children'),
    [Input('dislike-button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks is None:
        return 'Dislike'
    else:
        return 'Dislike ({})'.format(n_clicks)

@app.callback(
  Output('recommendations-button', 'style'),
    [Input('like-button', 'n_clicks')])
def update_output(n_clicks):
    if n_clicks is None:
        return {'margin-top': '40px', 'display': 'none'}
    elif n_clicks < 5:
        return {'margin-top': '40px', 'display': 'none'}
    else:
        return {'align-self': 'center', 'justify-content': 'center', 'margin-top': '20px'}
        

@app.callback(
    [Output('movie-poster-rec-1', 'src'),
     Output('movie-title-rec-1', 'children'),
     Output('movie-overview-rec-1', 'children'),
     Output('movie-poster-rec-2', 'src'),
     Output('movie-title-rec-2', 'children'),
     Output('movie-overview-rec-2', 'children'),
     Output('movie-poster-rec-3', 'src'),
     Output('movie-title-rec-3', 'children'),
     Output('movie-overview-rec-3', 'children'),
     Output('movie-poster-rec-4', 'src'),
     Output('movie-title-rec-4', 'children'),
     Output('movie-overview-rec-4', 'children'),
     Output('movie-poster-rec-5', 'src'),
     Output('movie-title-rec-5', 'children'),
     Output('movie-overview-rec-5', 'children'),
     Output('rec-button', 'style'),],
    [Input('rec-button', 'n_clicks')]
)
def update_output(n_clicks):
    global df_movies_nlp
    global liked_movies
    global disliked_movies

    if n_clicks is None:
        return {'display': 'none'}
    else:
        liked_movies_list = liked_movies['Title'].tolist()
        disliked_movies_list = disliked_movies['Title'].tolist()
        print("liked list: ", liked_movies_list)
        print("disliked_list: ", disliked_movies_list)

        print(len(df_movies_nlp))

        # remove disliked movies from df_movies_nlp
        for i in range(len(disliked_movies_list)):
            df_movies_nlp = df_movies_nlp[df_movies_nlp['title'] != disliked_movies_list[i]]

        # print row of disliked movie
        print(len(df_movies_nlp))
        
        recommended_movies = tfidf_final(liked_movies_list, df_movies_nlp)
        print("recommended movies: ", recommended_movies)

        poster_urls = []
        titles = []
        overviews = []

        for i in range(5):
            # get row of recommended movie title
            recommended_movie = df[df['title'] == recommended_movies[i]]

            # get backdrop path
            poster_url = recommended_movie['backdrop_path'].values[0]

            # filter backdrop path if its not a string
            if type(poster_url) != str:
                poster_url = 'https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg'
            else:
                poster_url = 'https://www.themoviedb.org/t/p/original' + poster_url

            # get title and overview
            title = recommended_movie['title'].values[0]
            overview = recommended_movie['overview'].values[0]

            # append to lists
            poster_urls.append(poster_url)
            titles.append(title)
            overviews.append(overview)

        return poster_urls[0], titles[0], overviews[0], poster_urls[1], titles[1], overviews[1], poster_urls[2], titles[2], overviews[2], poster_urls[3], titles[3], overviews[3], poster_urls[4], titles[4], overviews[4], {'display': 'none'}


# Page for instructions
page_4_layout = html.Div(
    children = [
        nav_menu,
        html.Div(
            children = [
                html.H1('Welcome to Movie Tinder', style = {'margin-bottom': 15}),
                html.P('This app will help you find new movies to watch. You can select your favourite genres and then swipe through movies and click the like button if you enjoy this movie. After you have liked at least 5 movies, you can see your specialized movie recommendations.', style = {'margin-bottom': 15}),

                html.H2('How does this all work?', style = {'margin-bottom': 15}),
                html.P('The app uses a machine learning algorithm called tf-idf to find similar movies. Tf-idf stands for term frequency-inverse document frequency. Tf-idf is a numerical statistic that is intended to reflect how important a word is to a document in a collection or corpus. The tf-idf value increases proportionally to the number of times a word appears in the document and is offset by the number of documents in the corpus that contain the word, which helps to adjust for the fact that some words appear more frequently in general. Tf-idf is one of the most popular term-weighting schemes today; 83 percent of text-based recommender systems in digital libraries use tf-idf.', style = {'margin-bottom': 15}),

                html.H2('Which data is used?', style = {'margin-bottom': 15}),
                html.P('The data is from the Movie Database (TMDB). The data contains roughly 19,000 movies and 2.6 million ratings that have been released after the year 2000. The data contains information about the movies, such as the title, overview, genres, release date, production companies, production countries and spoken languages.', style = {'margin-bottom': 30}),

                html.H1('Instructions', style = {'margin-bottom': 15}),

                html.H3('Step 1 - Selecting Genres', style = {'margin-bottom': 15}),
                html.P('Go to the page "Select Genres" and select your favourite genres from the list. You can choose as many genres as you like. Once you are satisfied with your choices, you can click the start button and you will be redirected to the Tinder page.', style = {'margin-bottom': 15}),
                
                html.H3('Step 2 - Tinder Swiping', style = {'margin-bottom': 15}),
                html.P('On the Tinder page, you will see the movie poster, title and the description of the movie. You can click the like button if you like the movie, the dislike button if you dislike the movie or the have-not seen button if you have not seen the movie. \nOnce you have reached at least 5 liked you can click the start button to start the movie recommendations.', style = {'margin-bottom': 15}),
            
                html.H3('Step 3 - Recommendations', style = {'margin-bottom': 15}),
                html.P('On the recommendations page, you will see the movies you previously liked on the tinder page. Click on the "Start" button to start the recommendation process. This process usually takes 15 seconds, but could take longer depending on the amount of liked movies. After the calculations have been made, you will see the top 5 recommended movies for you based on your previous genre and movie choices. Here you can see the information about the movie; movie poster, title and overview.', style = {'margin-bottom': 15}),

                html.H3('Step 4 - Watch the movie', style = {'margin-bottom': 15}),
                html.P('Enjoy the movie!', style = {'margin-bottom': 15}),
            ],
            style = {'margin-left': '15%', 'margin-right': '15%'}
        ),
])

# Create the callback for the page content based on the url
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/select-genres':
        return page_1_layout
    elif pathname == '/tinder':
        return page_2_layout
    elif pathname == '/recommendations':
        return html.Div(
                    children = [
                        nav_menu,
                            html.Div(
                                children = [
                                    html.H1('Your Recommended Movies'),
                                    html.H4('Based on your selected movies: {}'.format(', '.join(liked_movies['Title'].values)), id = 'selected-movies', style = {'margin-top': '20px', 'margin-left': '15%', 'margin-right': '15%'}),
                                    dbc.Button('Start', id = 'rec-button', style = {'margin-top': '50px'})
                                ]
                            ),
                            # recommended movie 1
                            html.Div(
                                children = [
                                    html.Img(id='movie-poster-rec-1', style = {'margin-top': '20px'}, height = '300px'),
                                    html.H2(id='movie-title-rec-1', style = {'margin-top': '20px'}),
                                    html.P(id='movie-overview-rec-1', style = {'margin-top': '20px', 'margin-left': '15%', 'margin-right': '15%'}),     
                                ]
                            ),
                            # recommended movie 2
                            html.Div(
                                children = [
                                    html.Img(id='movie-poster-rec-2', style = {'margin-top': '20px'}, height = '300px'),
                                    html.H2(id='movie-title-rec-2', style = {'margin-top': '20px'}),
                                    html.P(id='movie-overview-rec-2', style = {'margin-top': '20px', 'margin-left': '15%', 'margin-right': '15%'}),     
                                ], style = {'margin-top': '20px'}
                            ),
                            # recommended movie 3
                            html.Div(
                                children = [
                                    html.Img(id='movie-poster-rec-3', style = {'margin-top': '20px'}, height = '300px'),
                                    html.H2(id='movie-title-rec-3', style = {'margin-top': '20px'}),
                                    html.P(id='movie-overview-rec-3', style = {'margin-top': '20px', 'margin-left': '15%', 'margin-right': '15%'}),     
                                ], style = {'margin-top': '20px'}
                            ),
                            # recommended movie 4
                            html.Div(
                                children = [
                                    html.Img(id='movie-poster-rec-4', style = {'margin-top': '20px'}, height = '300px'),
                                    html.H2(id='movie-title-rec-4', style = {'margin-top': '20px'}),
                                    html.P(id='movie-overview-rec-4', style = {'margin-top': '20px', 'margin-left': '15%', 'margin-right': '15%'}),     
                                ], style = {'margin-top': '20px'}
                            ),
                            # recommended movie 5
                            html.Div(
                                children = [
                                    html.Img(id='movie-poster-rec-5', style = {'margin-top': '20px'}, height = '300px'),
                                    html.H2(id='movie-title-rec-5', style = {'margin-top': '20px'}),
                                    html.P(id='movie-overview-rec-5', style = {'margin-top': '20px', 'margin-left': '15%', 'margin-right': '15%'}),     
                                ], style = {'margin-top': '20px'}
                            ),
                        ]
                    )
    elif pathname == '/instructions':
        return page_4_layout
    else:
        return page_4_layout


def create_cosine(data):
    # create tfidf vectorizer
    tfidf_vectorizer = TfidfVectorizer(ngram_range=(1, 2))

    # transform data to tfidf matrix (sparse matrix)
    tfidf = tfidf_vectorizer.fit_transform(data)

    # calculate cosine similarity
    cosine_sim = cosine_similarity(tfidf)
  
    return cosine_sim


def recommend_movies(df, movie_title, cosine_sim, n):
   
    # get the index of the movie that matches the title
    idx = df[df["title"] == movie_title].index[0]

    # create a Series with the similarity scores in descending order
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

    lst = []

    # add 5 most similar movies to the list
    for i in list(score_series.iloc[1:n].index):
        lst.append([df.iloc[i]["title"], score_series[i]])

    return lst


def tfidf_final(movie_lst, df):
    cols = ['new_title', 'overview', 'spoken_languages', 'original_language', 'production_companies', 'production_countries', 'new_title', 'new_title', 'overview', 'spoken_languages', 'spoken_languages', 'spoken_languages', 'spoken_languages', 'original_language', 'original_language', 'original_language', 'original_language', 'original_language', 'original_language', 'original_language', 'production_companies', 'production_companies', 'production_companies', 'production_companies', 'production_companies', 'production_companies', 'production_companies', 'production_companies', 'production_companies', 'production_companies', 'production_countries', 'production_countries', 'production_countries', 'production_countries', 'production_countries', 'production_countries', 'production_countries', 'production_countries']

    lst = []

    # create tfidf column with column combination
    df["tfidf"] = df[cols].apply(" ".join, axis=1)

    # create cosine similarity matrix
    cosine_sim = create_cosine(df["tfidf"])

    # loop over all movies
    for movie in movie_lst:
        # get 10  movie recommendations for each movie based on cosine similarity matrix
        recommended_movies = recommend_movies(df, movie, cosine_sim, 6)
        lst.append(recommended_movies)

    # if movie_lst is longer than 1, get first 2 recommendations for each movie
    if len(movie_lst) > 1:
        # get first 2 recommendations for each movie
        lst = [item[:2] for item in lst]

    # flatten lst
    lst = [item for sublist in lst for item in sublist]

    # sort lst based on score
    lst = sorted(lst, key=lambda x: x[1], reverse=True)

    # remove score from lst but keep the order
    lst = [item[0] for item in lst]

    return lst[:5]


if __name__ == '__main__':
    app.run_server(debug = False)

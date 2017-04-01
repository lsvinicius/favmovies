from flask_testing import TestCase
from src import restful_app
from src.password import hash_password
from src import database
from src.model.user import User
from src.model.movie import Movie
from src.api.favmovies import USER_NOT_FOUND, MOVIE_NOT_FOUND

def create_database():
    user = User(name='Vinicius Silva', email='vinicius@gmail.com', password=hash_password('admin'))
    movie = Movie(imdbID='imdbid',
                  title='300',
                  plot='greeks and persians fighting',
                  type='movie',
                  poster="N/A",
                  user_id=1,
                  year=2008) #possibly wrong year
    user.movies.append(movie)
    database.db.create_all()
    database.db.session.add(user)
    database.db.session.commit()

def destroy_database():
    database.db.session.remove()
    database.db.drop_all()

class TestSetup(TestCase):
    TESTING = True
    movie_json = {
        'imdbID': 'imdbid',
        'Title':'300',
        'Plot': 'greeks and persians fighting',
        'Type': 'movie',
        'Poster': 'N/A',
        'user_id': 1,
        'Comment': None,
        'Year': 2008 #possibly wrong year
    }

    def create_app(self):
        #using the same application database, this is not a problem,
        #since the application database is destroyed every time it starts up
        app = restful_app.create_app()
        database.db.init_app(app)
        return app

    def setUp(self):
        create_database()

    def tearDown(self):
        destroy_database()

class RestfulTest(TestSetup):
    def call_get(self, user_id, imdb_id=None):
        address = '/restful/favmovies/'+user_id
        if imdb_id:
            address = address+'/'+imdb_id
        return self.client.get(address)

    #test all scenarios for favmovies_get
    def test_get_all_movies_from_valid_user(self):
        response = self.call_get('1')
        assert response.json == {'favmovies':[self.movie_json]}

    def test_get_all_movies_from_invalid_user(self):
        response = self.call_get('2')
        assert response.json == USER_NOT_FOUND

    #test all scenarios for favmovies_get_single
    def test_get_single_valid_movie_from_valid_user(self):
        response = self.call_get('1', 'imdbid')
        assert response.json == self.movie_json

    def test_get_single_valid_movie_from_invalid_user(self):
        response = self.call_get('2', 'imdbid')
        assert response.json == USER_NOT_FOUND

    def test_get_single_invalid_movie_from_valid_user(self):
        response = self.call_get('1', '1')
        assert response.json == MOVIE_NOT_FOUND

    #test all scenarios for favmovies_post
    imdb_id1 = 'tt0133093'
    imdb_id2 = 'tt0234215'
    def call_post(self, user_id, data=None):
        if data is None:
            data = [self.imdb_id1, self.imdb_id2]
        return self.client.post('/restful/favmovies/'+user_id, data={'movies':data})

    def test_valid_post_with_valid_user(self):
        response = self.call_post('1')
        m1 = Movie.query.filter_by(imdbID = self.imdb_id1).first()
        m2 = Movie.query.filter_by(imdbID = self.imdb_id2).first()
        assert len(response.json['added_movies']) == 2 and m1 is not None and m2 is not None

    def test_valid_post_with_valid_user_twice(self):
        response = self.call_post('1')
        response = self.call_post('1')
        m1 = Movie.query.filter_by(imdbID = self.imdb_id1).all()
        m2 = Movie.query.filter_by(imdbID = self.imdb_id2).all()
        assert len(response.json['added_movies']) == 0 and len(m1) == 1 and len(m2) == 1

    def test_valid_post_with_invalid_user(self):
        response = self.call_post('2')
        m1 = Movie.query.filter_by(imdbID = self.imdb_id1).first()
        m2 = Movie.query.filter_by(imdbID = self.imdb_id2).first()
        assert response.json == USER_NOT_FOUND and m1 is None and m2 is None

    def test_invalid_post_with_valid_user(self):
        invalid_id = 'invalid'
        response = self.call_post('1', [invalid_id])
        m1 = Movie.query.filter_by(imdbID = invalid_id).first()
        assert len(response.json['added_movies']) == 0 and m1 is None

    #test all scenarios for favmovies_put
    def call_put(self, user_id, imdb_id, data={'comment':'nice movie'}):
        return self.client.put('/restful/favmovies/'+user_id+'/'+imdb_id, data=data)

    def test_update_comment_of_valid_movie_of_valid_user(self):
        response = self.call_put('1', 'imdbid')
        movie = Movie.query.get(1)
        assert (response.json == {'Response':'Updated successfully'} and movie.comment == 'nice movie')

    def test_update_comment_of_invalid_movie_of_valid_user(self):
        response = self.call_put('1', '1')
        movie = Movie.query.get(1)
        assert response.json == MOVIE_NOT_FOUND and movie.comment is None

    def test_update_comment_of_valid_movie_of_invalid_user(self):
        response = self.call_put('2', 'imdbid')
        movie = Movie.query.get(1)
        assert response.json == USER_NOT_FOUND and movie.comment is None

    #test all scenarios for favmovies_delete
    def call_delete(self, user_id, imdb_id):
        return self.client.delete('/restful/favmovies/'+user_id+'/'+imdb_id)

    def test_delete_valid_movie_from_valid_user(self):
        response = self.call_delete('1', 'imdbid')
        movie = Movie.query.get(1)
        assert movie is None

    def test_delete_invalid_movie_from_valid_user(self):
        response = self.call_delete('1', '1')
        movie = Movie.query.get(1)
        assert movie is not None

    def test_delete_valid_movie_from_invalid_user(self):
        response = self.call_delete('2', 'imdbid')
        movie = Movie.query.get(1)
        assert movie is not None

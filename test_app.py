import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movie, Actor, db, Gender
from random import randint
from datetime import datetime

executive_producer_jwt = os.environ["EXECUTIVE_PRODUCER_JWT"]
casting_director_jwt = os.environ["CASTING_DIRECTOR_JWT"]
casting_assistant_jwt = os.environ["CASTING_ASSISTANT_JWT"]
expired_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjZiYi1EX2pSVjk3UWdyUWhUX2x0MiJ9.eyJpc3MiOiJodHRwczovL21hbGkxMjM0LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWM1NjYyN2Y5NzkzNDBjNzNlNGVlYTMiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTU4OTk5NTE1MywiZXhwIjoxNTg5OTk1NDUzLCJhenAiOiJYaXNGNFNQSHBObXBYdkxuVDd3UloxN1YwUENUZnNHTyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.KFOexGTnTlJFvYOG1sb8mNgN72d_GkBgIzq4WtYi8YqiWBYVSuf8VHHh_8GjZZO2XVRRt2BZnv_mug09gZvdP1lUsJlSE0_eAFPHa9C9VihghSkz_UUqvqAVUNd7heDsGevkawhJY6b9aOghvyDdEx59eyT6JYlJ8eh4r_vUTECo9I7vNSU8rp3YRKcfH6VGXir4jUJMECctIn5gWyy6iPVa5hRFUCBB96YlXqFX19_lv3k4C5gvSUw7OFTzAHp0NZJtDx6oAaIyAmOpQd51drke7M0syiN08ePVTNkHG4MlFVDQMbfpcRIWVuz9FRrxdYPmPbNkhPNGStdON-BDRQ'

new_actor = {
    'name': 'ali',
    'age': 25,
    'gender': 'male'
    }

new_movie = {
            'title': 'movie',
            'release_date': '03/05/2020 23:00 UTC+01'
            }

expired_token_message = {
                'error': 'token_expired',
                'description': 'Token expired.'
                }

no_permission_message = {
            'error': 'unauthorized',
            'description': 'Permission not found.'
            }

class Casting_agency(unittest.TestCase):
    """This class represents the casting_agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.executive_producer_jwt = executive_producer_jwt
        self.casting_director_jwt = casting_director_jwt
        self.casting_assistant_jwt = casting_assistant_jwt
        self.expired_jwt = expired_jwt
        self.expired_token_message = expired_token_message
        self.no_permission_message = no_permission_message
        self.new_actor = new_actor
        self.new_movie = new_movie
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    Write at least one test for each endpoint for successful operation and for expected errors.
    """
    def test_casting_assistant_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_actors'], len(data['actors']))
        nb_actors = db.session.query(db.func.count(Actor.id)).scalar()
        self.assertEqual(data['total_actors'], nb_actors)
    
    def test_casting_director_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_actors'], len(data['actors']))
        nb_actors = db.session.query(db.func.count(Actor.id)).scalar()
        self.assertEqual(data['total_actors'], nb_actors)
    
    def test_executive_producer_get_actors(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_actors'], len(data['actors']))
        nb_actors = db.session.query(db.func.count(Actor.id)).scalar()
        self.assertEqual(data['total_actors'], nb_actors)
    
    def test_401_expired_jwt(self):
        res = self.client().get(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.expired_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.expired_token_message)
    
    def test_casting_assistant_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], len(data['movies']))
        nb_movies = db.session.query(db.func.count(Movie.id)).scalar()
        self.assertEqual(data['total_movies'], nb_movies)
    
    def test_casting_director_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], len(data['movies']))
        nb_movies = db.session.query(db.func.count(Movie.id)).scalar()
        self.assertEqual(data['total_movies'], nb_movies)
    
    def test_executive_producer_get_movies(self):
        res = self.client().get(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_movies'], len(data['movies']))
        nb_movies = db.session.query(db.func.count(Movie.id)).scalar()
        self.assertEqual(data['total_movies'], nb_movies)
    
    #
    def test_403_casting_assistant_post_actors(self):
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)
    
    def test_403_casting_assistant_delete_actors(self):
        res = self.client().delete(
            '/actors/7',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)
    
    def test_403_casting_assistant_update_actors(self):
        res = self.client().patch(
            '/actors/7',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)
    
    def test_casting_director_post_actors(self):
        self.new_actor['name'] += ' ' + str(randint(1, 10000))
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            },
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    
    def test_casting_director_update_actors(self):
        actor = Actor.query.first()
        formatted_actor = actor.format()
        formatted_actor['age'] += 1
        res = self.client().patch(
            '/actors/{}'.format(actor.id),
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            },
            json=formatted_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], formatted_actor)
    
    def test_casting_director_delete_actors(self):
        actor = Actor.query.first()
        res = self.client().delete(
            '/actors/{}'.format(actor.id),
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], actor.id)
    
    def test_executive_producer_post_actors(self):
        self.new_actor['name'] += ' ' + str(randint(1, 10000))
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            },
            json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    
    def test_executive_producer_update_actors(self):
        actor = Actor.query.first()
        formatted_actor = actor.format()
        formatted_actor['age'] -= 1
        res = self.client().patch(
            '/actors/{}'.format(actor.id),
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            },
            json=formatted_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], formatted_actor)
    
    def test_executive_producer_delete_actors(self):
        actor = Actor.query.first()
        res = self.client().delete(
            '/actors/{}'.format(actor.id),
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], actor.id)
    
    def test_422_post_actors(self):
        actor_no_name={
            'age': 42,
            'gender': 'male'
        }
        res = self.client().post(
            '/actors',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            },
            json=actor_no_name)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        message = {
            'error': 'missing actor informations',
            'description': '`name` is required'
        }
        self.assertEqual(data['message'], message)
    
    def test_404_update_actors(self):
        res = self.client().patch(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_404_delete_actors(self):
        res = self.client().delete(
            '/actors/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_403_casting_assistant_post_movies(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)
    
    def test_403_casting_assistant_delete_movies(self):
        res = self.client().delete(
            '/movies/22',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)
    
    def test_403_casting_assistant_update_movies(self):
        res = self.client().patch(
            '/movies/22',
            headers={
                "Authorization": "Bearer {}".format(self.casting_assistant_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)
    
    def test_403_casting_director_post_movies(self):
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)

    def test_403_casting_director_delete_movies(self):
        res = self.client().delete(
            '/movies/12',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], self.no_permission_message)
    
    def test_casting_director_update_movies(self):
        movie = Movie.query.first()
        formatted_movie = movie.format()
        release_date = formatted_movie['release_date'] + '00'
        release_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M UTC%z')
        release_date = datetime(
            release_date.year+1,
            release_date.month,
            release_date.day,
            tzinfo=release_date.tzinfo)
        formatted_movie['release_date'] = release_date.strftime('%d/%m/%Y %H:%M UTC%z')[0:-2]
        res = self.client().patch(
            '/movies/{}'.format(movie.id),
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            },
            json=formatted_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], formatted_movie)
        
    
    def test_executive_producer_post_movies(self):
        self.new_movie['title'] += ' ' + str(randint(1, 10000))
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            },
            json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
    
    def test_executive_producer_update_movies(self):
        movie = Movie.query.first()
        formatted_movie = movie.format()
        release_date = formatted_movie['release_date'] + '00'
        release_date = datetime.strptime(release_date, '%d/%m/%Y %H:%M UTC%z')
        release_date = datetime(
            release_date.year+1,
            release_date.month,
            release_date.day,
            tzinfo=release_date.tzinfo)
        formatted_movie['release_date'] = release_date.strftime('%d/%m/%Y %H:%M UTC%z')[0:-2]
        res = self.client().patch(
            '/movies/{}'.format(movie.id),
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            },
            json=formatted_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated'], formatted_movie)
    
    def test_executive_producer_delete_movies(self):
        movie = Movie.query.first()
        formatted_movie = movie.format()
        formatted_movie['title'] += ' revolution'
        res = self.client().delete(
            '/movies/{}'.format(movie.id),
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie.id)
    
    def test_422_post_movies(self):
        movie_no_title={
            'release_date': '03/05/2020 00:00 UTC+00'
        }
        res = self.client().post(
            '/movies',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            },
            json=movie_no_title)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        message = {
            'error': 'missing movie informations',
            'description': '`title` is required'
        }
        self.assertEqual(data['message'], message)
    
    def test_404_delete_movies(self):
        res = self.client().delete(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(self.executive_producer_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_404_update_movies(self):
        res = self.client().patch(
            '/movies/1',
            headers={
                "Authorization": "Bearer {}".format(self.casting_director_jwt)
            })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
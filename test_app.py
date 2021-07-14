import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

# database path
database_path = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)

auth0_tokens = {
    "casting_assistant": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlotSmJLVzlGTTJJVHRpb1c2X0hvcSJ9.eyJpc3MiOiJodHRwczovL2pzYXNhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlYjM1NmMxNjFhODIwMDY4ZWE1NjRmIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNjI4MjEyMiwiZXhwIjoxNjI2MzY4NTIyLCJhenAiOiJYQ0gxVGJBbHZ4Y05BQ3IzSmtheTh5ZnRTaVF4cVlmciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.gpSDI_IVvFvzRmBFGB9aHIVcjeXRGzVbfNcZf2jB3HvxIekyjt-PMbG5TX25fcZwO9n13kiUL1OL8ITvI_iXqXBWvNG9bDYck3JPVKdfapNzXrmXLhKrhSyMbs_OQ6deC3ZrzLLtCNczgo58t47PCJltt8P6JvQKszlm6Ppuh7mUePFXZNHfyV-otEcQ66aLg-pLd_NcLdPSmY7qzON9wbodwo7k0eZrMkyBacnozWuuBu0wCyxvg9zoGKvOnmv2DhVUXXMrSK8qqa_I6k49gyfbBy2VBBG6dyGpWEr_gxPv46cRsOxFxmodcNShIsnoIzOLO4AoTRgdYVXUDRvK1g",
    "casting_director": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlotSmJLVzlGTTJJVHRpb1c2X0hvcSJ9.eyJpc3MiOiJodHRwczovL2pzYXNhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlYjM1NGJmYzVlOWIwMDZiYWM1MTljIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNjI4MjAzOCwiZXhwIjoxNjI2MzY4NDM4LCJhenAiOiJYQ0gxVGJBbHZ4Y05BQ3IzSmtheTh5ZnRTaVF4cVlmciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.UhpHbuEthUqsExxhFydCm6epm0ol-Lb-_CQTrr0wWPebao4tdphoGIBjuN0gBKhnDoTfLYXY02TEOU0aobjxfLgYtJrY8pMpSHpSmLmW6wSpp-9IhWytHZcG0vlRxyA7a94EZMqhGQcgSgymm1pB5d5nT0cZr0qF4cAz5-N6Ppr4ZJjH3E67tF5uEHbm6v4XVjlfd6DFbN8_yTzhJddXG-wuEN9oszwlBp5kw1ABa44SED7bHoGYhaHLbnKsBuvkSOx-5qXnMUflGUnYQnH1DmZKnYs_Uxbs8nBCzselRDMQQ7jRrSyDVTpQzbvAvWaGfoB7G9mLVtSjZbDv3P-2yA",
    "executive_producer": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlotSmJLVzlGTTJJVHRpb1c2X0hvcSJ9.eyJpc3MiOiJodHRwczovL2pzYXNhbi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBlYjM1YWFmYzVlOWIwMDZiYWM1MTlmIiwiYXVkIjoiaHR0cHM6Ly9jYXN0aW5nLWFnZW5jeSIsImlhdCI6MTYyNjI4MjE4NSwiZXhwIjoxNjI2MzY4NTg1LCJhenAiOiJYQ0gxVGJBbHZ4Y05BQ3IzSmtheTh5ZnRTaVF4cVlmciIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.tzKDM8_eAEk9KBDgw8LiHlH8dlM_NEwf6GIewKOVabAg9_qPtV5zDHLa-cerzHOXGSYM1nTR2F3OrQ0otwXBOpQLzRUQNTIXCDaNgz-rZE9a9nCi_u2wI4a9UVoUJhA54VKo4qYM5GLAzyVcx-hfJUEs93tiVfS-FFbR6fO1RT4S5LVbw9SHRnbpCb8a7I9goC7QenBo21u0jGIdxs7-Gf4JVtfYiLrpxQTTMLAo-Ehh_nIFAT0TNmULQJSrDxdGD4ttCbCLvxHd7tQhIC_evL4cDDRk7-eqszjmBvPkZvZq-mQpdMXnjp84PshfuZIBHrO_Uadm3bBwBK29ksb2HA"
}


class Casting_Agency_Tests(unittest.TestCase):
    """This class represents the casting agency api test cases"""

    casting_assistant_auth_header = {
        'Authorization': "Bearer " + auth0_tokens["casting_assistant"]
    }

    casting_director_auth_header = {
        'Authorization': "Bearer " + auth0_tokens["casting_director"]
    }

    producer_auth_header = {
        'Authorization': "Bearer " + auth0_tokens["executive_producer"]
    }

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        #db_drop_and_create_all()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # test cases
    # @app.route('/actors', methods=['GET'])
    def test_get_actors(self):
        res = self.client().get('/actors',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # @app.route('/movies', methods=['GET'])
    def test_get_movies(self):
        res = self.client().get('/movies',
                                headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # @app.route('/actors', methods=['POST'])
    def test_post_new_actor(self):
        res = self.client().post('/actors',
                                 json={'name': 'UdacityActor',
                                       'age': '42',
                                       'gender': 'Male'},
                                 headers=self.producer_auth_header)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_new_actor(self):
        res = self.client().post('/actors',
                                 json={},
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # @app.route('/actors', methods=['POST'])
    def test_post_new_movie(self):
        res = self.client().post('/movies',
                                 json={'title': 'UdacityMovie',
                                       'date': '7/11/2021'},
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_new_movie(self):
        res = self.client().post('/movies', json={},
                                 headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    # @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    def test_delete_actor(self):
        res = self.client().delete('/actors/1', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_404_delete_actor(self):
        res = self.client().delete('/actors/200', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    def test_delete_movie(self):
        res = self.client().delete('/movies/1', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 1)

    def test_404_delete_movie(self):
        res = self.client().delete('/movies/200', headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    # @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    def test_update_actor_by_id(self):
        update_actor = {'name': 'Jatin Sasan'}
        res = self.client().patch('/actors/1', json=update_actor,
                                  headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_update_actor_by_id(self):
        update_actor = {}
        res = self.client().patch('/actors/1', json=update_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    def test_update_movie_by_id(self):
        update_movie = {'title': 'SANJOSE_MEMOIRS', 'release_dat': '03/23/2010'
                        }
        res = self.client().patch('/movies/1', json=update_movie,
                                  headers=self.producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_update_movie_by_id(self):
        update_movie = {}
        res = self.client().patch('/movies/1', json=update_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    # Testing Role based access
    # Casting assistant
    def test_get_actors_castassistant(self):
        res = self.client().get('/actors',
                                headers=self.casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_update_movie_castassistant(self):
        update_movie = {'title': 'CASTASSISTANT', 'date': '07/11/2021'
                        }
        res = self.client().patch('/movies/2', json=update_movie,
                                  headers=self.casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_post_new_movie_castassistant(self):
        new_movie = {'title': 'Movie_CASTASSISTANT',
                     'release_date': '01/01/2021'}
        res = self.client().post('/movies', json=new_movie,
                                 headers=self.casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    # Test Role based access for Casting Director
    def test_get_actors_casting_director(self):
        res = self.client().get('/actors',
                                headers=self.casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_post_new_movie_casting_director(self):
        new_movie = {'title': 'Movie_CASTDIRECTOR',
                     'release_date': '01/01/2021'}
        res = self.client().post('/movies', json=new_movie,
                                 headers=self.casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_update_movie_casting_director(self):
        update_movie = {'title': 'CASTDIRECTOR', 'date': '07/11/2021'
                        }
        res = self.client().patch('/movies/5', json=update_movie,
                                  headers=self.casting_assistant_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")

    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/5',
                                   headers=self.casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "Permission not found.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

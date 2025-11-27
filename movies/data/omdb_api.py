import requests
import dotenv
import os

from movies.models import Movie

dotenv.load_dotenv()

class Omdb:
    __URL = f"http://www.omdbapi.com/?apikey={os.getenv("OMDB_API_KEY")}&"

    def __init__(self, title: str, user_id: int):
        self.movie_data = requests.get(self.__URL, {'t': title}).json()

        if self.movie_data.get('Response') == 'False':
            raise Exception(self.movie_data.get('Error'))

        self.movie = Movie(
            title=self.movie_data.get('Title'),
            year=int(self.movie_data.get('Released')[-4:]),
            rating=float(self.movie_data.get('imdbRating')),
            poster=self.movie_data.get('Poster'),
            user_id=user_id
        )

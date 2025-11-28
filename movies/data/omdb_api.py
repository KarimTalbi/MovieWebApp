import requests
import dotenv
import os

from movies.models import Movie

dotenv.load_dotenv()

class Omdb:
    __URL = f"http://www.omdbapi.com/?apikey={os.getenv("OMDB_API_KEY")}&"

    def __init__(self, title: str):
        self.__movie_data = requests.get(self.__URL, {'t': title}).json()

        if self.__movie_data.get('Response') == 'False':
            raise Exception(self.__movie_data.get('Error'))

        self.__movie = Movie(
            title=self.__movie_data.get('Title'),
            year=int(self.__movie_data.get('Released')[-4:]),
            rating=float(self.__movie_data.get('imdbRating')),
            poster=self.__movie_data.get('Poster')
        )

    def movie(self):
        return self.__movie

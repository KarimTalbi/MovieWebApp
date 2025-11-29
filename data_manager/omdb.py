import requests
import dotenv
import os

from models import Movie


class MovieApiError(Exception):
    pass


dotenv.load_dotenv()


class Omdb:
    __URL = f"http://www.omdbapi.com/?apikey={os.getenv("OMDB_API_KEY")}&"

    def __init__(self, title: str):

        self._movie_data = requests.get(
            url=self.__URL,
            params={'t': title}
        ).json()

        self.__response = self._movie_data.get('Response')

        if self._movie_data.get('Response') == 'False':
            raise MovieApiError(f"No movie found with title {title}")

        self.__movie = Movie(
            title=self._movie_data.get('Title'),
            release_year=int(self._movie_data.get('Released')[-4:]),
            rated=self._movie_data.get('Rated'),
            rating=float(self._movie_data.get('imdbRating')),
            runtime=self._movie_data.get('Runtime'),
            genre=self._movie_data.get('Genre'),
            director=self._movie_data.get('Director'),
            actors=self._movie_data.get('Actors'),
            plot=self._movie_data.get('Plot'),
            imdb_id=self._movie_data.get('imdbID'),
            poster=self._movie_data.get('Poster')
        )

    def movie(self):
        return self.__movie

"""
This module provides a client for the OMDB (Open Movie Database) API.

It allows fetching movie details by title and converting the data into a
local Movie model instance.
"""
import requests
import dotenv
import os

from models import Movie


class MovieApiError(Exception):
    """Raised when the OMDB API returns an error or can't find a movie."""
    pass


dotenv.load_dotenv()


class Omdb:
    """A client to fetch movie data from the OMDB API."""
    __URL = f"http://www.omdbapi.com/?apikey={os.getenv('OMDB_API_KEY')}&"

    def __init__(self, title: str):
        """
        Initializes the Omdb client and fetches movie data.

        Args:
            title: The title of the movie to search for.

        Raises:
            MovieApiError: If the movie is not found or the API returns an error.
        """
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

    def movie(self) -> Movie:
        """
        Returns the fetched movie data as a Movie model instance.

        Returns:
            A Movie object populated with data from the OMDB API.
        """
        return self.__movie

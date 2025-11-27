import requests
import dotenv
import os
from typing import Any

dotenv.load_dotenv()


class MovieApi:
    """
    A wrapper for the OMDB (Open Movie Database) API.

    This class fetches movie data based on a title and provides properties
    to access various details of the movie.

    Args:
        title (str): The title of the movie to search for.

    Raises:
        ValueError: If the title is empty.
    """
    __KEY = os.getenv("OMDB_API_KEY")
    __URL = "http://www.omdbapi.com/?apikey=[yourkey]&"

    def __init__(self, title: str):
        self.__url = self.__URL.replace('[yourkey]', self.__KEY)

        if not title:
            raise ValueError("parameter 'title' can't be empty")

        self.__param = {'t': title}
        self.__movie = requests.get(self.__url, self.__param).json()

        if self.__movie.get('Response') == 'False':
            raise IOError

    @property
    def movie(self) -> dict[str, Any]:
        """The raw dictionary response from the OMDB API."""
        return self.__movie

    @property
    def title(self) -> str:
        """The title of the movie."""
        return self.__movie.get('Title')

    @property
    def year(self) -> int:
        """The release year of the movie."""
        year = self.__movie.get('Released')[-4:]
        return int(year)

    @property
    def rating(self) -> float:
        """The IMDb rating of the movie."""
        rating = self.__movie.get('imdbRating')
        return float(rating)

    @property
    def poster(self) -> str:
        """The URL of the movie's poster image."""
        return self.__movie.get('Poster')

    @property
    def imdb_id(self) -> str:
        """The IMDb ID of the movie."""
        return self.__movie.get('imdbID')

    @property
    def country(self) -> str:
        """The primary country of production for the movie."""
        res = self.__movie.get('Country')
        return res.split(',')[0].strip()

    @property
    def info(self) -> dict[str, str | int | float]:
        """A dictionary containing curated information about the movie."""
        info = {
            'title': self.title,
            'year': self.year,
            'rating': self.rating,
            'poster': self.poster,
            'imdb_id': self.imdb_id,
            'country': self.country
        }
        return info
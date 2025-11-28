from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

# TODO third table for usermovies
# TODO delete should remove movie id from usermovie table
# TODO when trying to add a movie check if it is in the database before looking in the api
# TODO info of movie should be updateable for users
# TODO single movie shown, update and delete on page
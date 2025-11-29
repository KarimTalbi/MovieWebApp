# MovieWebApp

This project is a simple movie web application, part of the MSIT curriculum.

## Screenshot

![MovieWebApp Screenshot](docs/images/example.png)

## Features

-   **User Management:** Create, update, delete, and view users.
-   **Movie Management:** Add, update, delete, and view movies for each user.

## Installation

1.  **Clone the repository:**
    
    ```
    git clone 
    ```
    
2.  **Create a virtual environment:**
    
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venvScriptsactivate
    ```
    
3.  **Install the dependencies:**
    
    ```bash
    pip install -r requirements.txt
    ```
    
4.  **Set up the environment variables:** Create a `.env` file in the root directory of the project and add your OMDB API key:
    
    ```
    OMDB_API_KEY=your_api_key
    ```
    
    You can get an API key from [http://www.omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx).
    

## Usage

1.  **Run the application:**
    
    ```bash
    python app.py
    ```
    
2.  Open your web browser and navigate to `http://127.0.0.1:5000`.
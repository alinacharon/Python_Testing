# gudlift-registration

1. About the Project

    This is a proof of concept (POC) project demonstrating a lightweight version of our competition booking platform. The aim is to keep things as simple as possible and use user feedback for iterations.

2. Technologies

    This project uses the following technologies:

    * Python v3.x+
    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

3. Installation

    - Clone the repository and navigate to the project directory
    - Create a virtual environment: `virtualenv .`
    - Activate the virtual environment: `source bin/activate`
    - Install dependencies: `pip install -r requirements.txt`
    - Set the FLASK_APP environment variable: `export FLASK_APP=server.py`
    - Run the application: `flask run` or `python -m flask run`

4. Project Structure

    - `server.py`: Main Flask application file
    - `clubs.json`: JSON file containing club data
    - `competitions.json`: JSON file containing competition data
    - `templates/`: Directory containing HTML templates
    - `tests/`: Directory containing test files
        - `integration/`: Integration tests
        - `unit/`: Unit tests

5. Main Features

    - Club and competition data loaded from JSON files
    - User authentication via email
    - Booking system for competitions
    - Points system for clubs
    - View available points for each club

6. Testing

    The project includes unit and integration tests. To run the tests with coverage:

    ```
    python run_coverage.py
    ```

    This will generate a coverage report.

7. Development

    The application runs in debug mode by default. You can modify this in the `server.py` file.

8. Contributing

    Please update the `requirements.txt` file if you add any new packages:

    ```
    pip freeze > requirements.txt
    ```

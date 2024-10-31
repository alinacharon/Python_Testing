# gudlift-registration

## 1. Overview

This is a proof of concept (POC) project to demonstrate a lightweight version of our competition booking platform. The aim is to keep things as simple as possible and use user feedback for iterations.

## 2. Getting Started

This project uses the following technologies:

* Python v3.x+
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)

    While Django provides many features out of the box, Flask allows us to add only what we need.

* [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

    This ensures you'll be able to install the correct packages without interfering with Python on your machine. Before you begin, please ensure you have this installed globally.

## 3. Installation

- After cloning, change into the directory and type `<code>virtualenv .</code>`. This will set up a virtual Python environment within that directory.
- Next, type `<code>source bin/activate</code>`. You should see that your command prompt has changed to the name of the folder. This means that you can install packages here without affecting files outside. To deactivate, type `<code>deactivate</code>`.
- Rather than hunting around for the packages you need, you can install them in one step. Type `<code>pip install -r requirements.txt</code>`. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the `requirements.txt` file. An easy way to do this is `<code>pip freeze > requirements.txt</code>`.
- Flask requires that you set an environmental variable to the Python file. You will want to set the file to be `<code>server.py</code>`. Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details.
- You should now be ready to test the application. In the directory, type either `<code>flask run</code>` or `<code>python -m flask run</code>`. The app should respond with an address you can visit using your browser.

## 4. Current Setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm) to avoid using a database until necessary. The main files are:

* `competitions.json`: A list of competitions.
* `clubs.json`: A list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

## 5. Application Routes

### `/`
- **Method**: GET
- **Description**: Renders the index page.

### `/showSummary`
- **Method**: POST
- **Description**: Shows the summary of the club based on the provided email. If the email is not found, it redirects to the index page; otherwise, it renders the `welcome.html` template with club and competitions data.

### `/book/<competition>/<club>`
- **Method**: GET
- **Description**: Renders the booking page for a specific competition and club. If the club or competition is not found, it redirects to the index page with an error message.

### `/purchasePlaces`
- **Method**: POST
- **Description**: Handles the purchase of places for a competition. It updates the points and number of places available. If the purchase fails, it redirects to the index page with an error message.

### `/points`
- **Method**: GET
- **Description**: Views the points of clubs. Renders the `points.html` template with clubs and their points, or redirects to the index page if no clubs are found.

### `/logout`
- **Method**: GET
- **Description**: Logs out and redirects to the index page.

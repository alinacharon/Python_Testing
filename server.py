import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    """
    Load clubs from a JSON file.

    Returns:
        list: A list of clubs if the file is found and valid, otherwise an empty list.
    """
    try:
        with open('clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs
    except (FileNotFoundError, json.JSONDecodeError):
        flash("No data of clubs found.")
        return []


def loadCompetitions():
    """
    Load competitions from a JSON file.

    Returns:
        list: A list of competitions if the file is found and valid, otherwise an empty list.
    """
    try:
        with open('competitions.json') as comps:
            listOfCompetitions = json.load(comps)['competitions']
            return listOfCompetitions
    except (FileNotFoundError, json.JSONDecodeError):
        flash("No data of competitions found.")
        return []


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    """
    Render the index page.

    Returns:
        Response: The rendered index.html template.
    """
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    """
    Show the summary of the club based on the provided email.

    Returns:
        Response: Redirects to the index page if the email is not found,
                  otherwise renders the welcome.html template with club and competitions data.
    """
    email = request.form.get('email')
    club = next((club for club in clubs if club['email'] == email), None)
    if club is None:
        flash("Email not found.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
    """
    Render the booking page for a specific competition and club.

    Args:
        competition (str): The name of the competition.
        club (str): The name of the club.

    Returns:
        Response: Renders the booking.html template if the club and competition are found,
                  otherwise redirects to the index page with an error message.
    """
    foundClub = next((c for c in clubs if c['name'] == club), None)
    if not foundClub:
        flash("Club not found.")
        return redirect(url_for('index'))
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    """
    Handle the purchase of places for a competition.

    Returns:
        Response: Renders the welcome.html template with updated club and competition data,
                  or redirects to the index page with an error message if the purchase fails.
    """
    competition = next(
        (c for c in competitions if c['name'] == request.form['competition']), None)
    if not competition:
        flash("Competition not found.")
        return render_template('welcome.html', club=club, competitions=competitions)

    club = next((c for c in clubs if c['name'] == request.form['club']), None)
    if not club:
        flash("Club not found.")
        return render_template('welcome.html', club=club, competitions=competitions)

    placesRequired = int(request.form['places'])
    available_places = int(competition['numberOfPlaces'])
    points = int(club['points'])

    if placesRequired <= 0:
        flash("The number of places for booking is invalid. It cannot be negative or zero. Please choose a different number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > 12:
        flash("You can't book more than 12 places. Please choose a different number of places")
        return render_template('welcome.html', club=club, competitions=competitions)
    if placesRequired > available_places or placesRequired > points:
        flash("There are not enough spaces or points for your booking. Please choose a different number of places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Update points and number of places
    competition['numberOfPlaces'] = available_places - placesRequired
    club['points'] = points - placesRequired

    flash(f'Great-booking complete! You booked {placesRequired} places.')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def points_view():
    """
    View the points of clubs.

    Returns:
        Response: Renders the points.html template with clubs and their points,
                  or redirects to the index page if no clubs are found.
    """
    clubs_with_points = loadClubs()
    if not clubs_with_points:
        flash("No clubs found.")
        return redirect(url_for('index'))

    points_data = [{'name': club['name'], 'points': club.get(
        'points', 0)} for club in clubs_with_points]

    return render_template('points.html', clubs=points_data)


@app.route('/logout')
def logout():
    """
    Log out and redirect to the index page.

    Returns:
        Response: Redirects to the index page.
    """
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

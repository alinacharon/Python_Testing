import json
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    try:
        with open('clubs.json') as c:
            listOfClubs = json.load(c)['clubs']
            return listOfClubs
    except (FileNotFoundError, json.JSONDecodeError):
        flash("No data of clubs found.")
        return []


def loadCompetitions():
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
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    email = request.form.get('email')
    club = next((club for club in clubs if club['email'] == email), None)
    if club is None:
        flash("Email not found.")
        return redirect(url_for('index'))
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition, club):
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
        flash("The purchase quantity is invalid. It cannot be negative or zero.")
        return render_template('welcome.html', club=club, competitions=competitions)

    if placesRequired > available_places or placesRequired > 12 or placesRequired > points:
        flash("There is not enough space or points for your booking. Please note that you can't take more than 12 places.")
        return render_template('welcome.html', club=club, competitions=competitions)

    # Update
    competition['numberOfPlaces'] = available_places - placesRequired
    club['points'] = points - placesRequired

    flash(f'Great-booking complete! You booked {placesRequired} places.')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/points')
def points_view():
    clubs_with_points = loadClubs()
    if not clubs_with_points:
        flash("No clubs found.")
        return redirect(url_for('index'))

    points_data = [{'name': club['name'], 'points': club.get(
        'points', 0)} for club in clubs_with_points]

    return render_template('points.html', clubs=points_data)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

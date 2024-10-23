from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)
    host = "http://127.0.0.1:5001" 

    def on_start(self):
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task(1)
    def index(self):
        self.client.get("/")

    @task(2)
    def view_points(self):
        self.client.get("/points")

    @task(3)
    def book_competition(self):
        competitions = ["Spring Festival", "Fall Classic"]  
        clubs = ["Simply Lift", "Iron Temple", "She Lifts"]
        competition = random.choice(competitions)
        club = random.choice(clubs)
        with self.client.get(f"/book/{competition}/{club}", catch_response=True) as response:
            if response.status_code == 500:
                response.failure(f"Unsuccessful booking for the {competition} of {club}")
            else:
                response.success()

    @task(4)
    def purchase_places(self):
        competitions = ["Spring Festival", "Fall Classic"] 
        clubs = ["Simply Lift", "Iron Temple", "She Lifts"]
        competition = random.choice(competitions)
        club = random.choice(clubs)
        places = random.randint(1, 12)
        with self.client.post("/purchasePlaces", data={
            "competition": competition,
            "club": club,
            "places": places 
        }, catch_response=True) as response:
            if response.status_code == 500:
                response.failure(f"Unsuccessful booking of {places} for {club} on {competition}")
            else:
                response.success()

    @task(1)
    def logout(self):
        self.client.get("/logout")
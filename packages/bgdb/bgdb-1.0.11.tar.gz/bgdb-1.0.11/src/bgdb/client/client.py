import requests
from dotenv import load_dotenv
import os
import getpass
import json

# Class which represents the overall blood group database client
class Client:
    def __init__(self, url):
        """
        Initialise the client with the BGDB API URL
        """
        # URL of the database API
        self.url = url

        # Create a requests session
        self.session = requests.session()

        # Test the connection
        self.test_connection()

    def test_connection(self):
        """
        Function for checking the connection to the database
        """

        # Check the database is alive
        response = self.session.get(self.url + "/")

        # Check the response is valid
        if response.status_code == 200:
            print(f"Server: {self.url} is alive.")
        else:
            raise Exception(f"Server: {self.url} is unresponsive.")

    def login(self, use_env=False):
        """
        Function which logs in a user - if use_env is True, will use the envrionemt variables USER and PASSWORD
        """

        if use_env:
            load_dotenv()
            # Get the email and password from the environment
            self.email = os.environ.get("EMAIL")
            self.password = os.environ.get("PASSWORD")
        else:
            self.email = input("Enter your email: ")
            self.password = getpass.getpass("Enter your password: ")

        # Login to the database
        response = self.session.post(
            self.url + "/auth/login",
            json={"email": self.email, "password": self.password},
            headers={"Content-Type": "application/json"},
        )

        # Check the login was successful
        if response.status_code != 201:

            # load response as json
            response_json = json.loads(response.text)

            # Check if message is an array
            if isinstance(response_json["message"], list):
                error_messages = ", ".join(response_json["message"])
            else:
                error_messages = response_json["message"]

            # Print the errors
            print(f"Login failed: {error_messages}.")

        else:
            # Test that you are logged in
            logged_in_as = self.whoami()

            # Check if self.email matched logged_in_as
            if self.email == logged_in_as:
                print(f"Logged in successfuly as {self.email}")
            else:
                print(f"Login failed.")

    def whoami(self):
        response = self.session.get(self.url + "/auth/whoami")

        # Load response as json
        response_json = json.loads(response.text)

        # Check if response is 404
        if response.status_code == 404:
            return "Not logged in"

        # Check if response is 200
        if response.status_code == 200:
            return response_json["email"]

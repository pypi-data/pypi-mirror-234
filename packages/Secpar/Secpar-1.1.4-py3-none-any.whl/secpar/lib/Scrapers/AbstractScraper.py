import json
import os
from time import sleep

import requests
from abc import ABC, abstractmethod
from github import Github

# Disable SSL/TLS warnings from urllib3
requests.packages.urllib3.disable_warnings()

# Define an abstract base class for scrapers
class AbstractScraper(ABC):
    def __init__(self, platform, username, password, repo_owner, repo_name, access_token, platform_header):
        # Create a Github object using an access token
        git = Github(access_token)

        # Initialize class attributes
        self.platform = platform
        self.username = username
        self.password = password
        self.headers = {
            # Define HTTP headers for requests
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-language": "en-GB,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-US;q=0.6",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-requested-with": "XMLHttpRequest",
            "Referer": self.username,
            "Referrer-Policy": "strict-origin-when-cross-origin",
        }
        self.platform_header = platform_header
        self.current_submissions = {}
        self.extensions = {}
        self.repo = git.get_user(repo_owner).get_repo(repo_name)

    def scrape(self):
        # Perform the scraping workflow by calling various methods
        self.load_extensions()
        self.load_already_added()
        if self.login():
            self.get_submissions()
            self.update_submission_json()
        else:
            print("Login failed, please try again")

    def load_extensions(self):
        # Load extensions from a JSON file
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Resources", "Extensions", f"{self.platform}Extensions.json")
        with open(path, 'r') as json_file:
            self.extensions = json.load(json_file)

    def load_already_added(self):
        # Load previously added submissions from a JSON file in the repository
        submissions_path = f'submissions/{self.platform}Submissions.json'
        try:
            json_string = self.repo.get_contents(submissions_path).decoded_content.decode('utf-8')
            self.current_submissions = json.loads(json_string)['Submissions']
            self.current_submissions = {obj['id']: obj for obj in self.current_submissions}
        except:
            self.current_submissions = {}

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def get_submissions(self):
        pass

    @abstractmethod
    def get_submission_html(self, submission):
        pass

    def check_already_added(self, submission_id):
        # Check if a submission with the given ID is already added
        if str(submission_id) in self.current_submissions:
            return True
        return False

    @abstractmethod
    def update_already_added(self, submission_id):
        pass

    @abstractmethod
    def generate_directory_link(self, submission):
        pass

    @staticmethod
    def print_progress_bar(progress, end):
        # Print a progress bar with percentage
        print("[{0}{1}] {2}%    ".format("█" * int((progress/end)*50), "-" * int(50-(progress/end)*50), int((progress/end)*100)), end="\r")

    def update_submission_json(self):
        # Update the JSON file in the repository with the latest submissions
        submissions = list(self.current_submissions.values())
        submissions = sorted(submissions, key=lambda item: item['date'], reverse=True)

        try:
            # Update the file if it exists
            self.repo.get_contents(f'submissions/{self.platform}Submissions.json')
            self.repo.update_file(f'submissions/{self.platform}Submissions.json', f"Update {self.platform}Submissions.json", json.dumps({'Header': self.platform_header, 'Submissions': submissions}), self.repo.get_contents(f'submissions/{self.platform}Submissions.json').sha)
        except:
            # Create the file if it doesn't exist
            self.repo.create_file(f'submissions/{self.platform}Submissions.json', f"Create {self.platform}Submissions.json", json.dumps({'Header': self.platform_header, 'Submissions': submissions}), 'main')
            sleep(2)

# You can now create subclasses of AbstractScraper and implement the abstract methods for specific scraping tasks.

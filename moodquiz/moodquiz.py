#!/usr/bin/env python
from urllib.parse import urljoin, urlparse
from moodquiz.crawler import MoodleScrapper
from moodquiz.exceptions import *
from moodquiz.utils import valid_url
import os
import json
CONFIG_FILE = '.config.ini'

class Moodle:
    def __init__(self):
        self.check_config()

    def check_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
                self.valid_config = self.check_valid_config()
        else:
            self.valid_config = False

    def check_valid_config(self):
        return self.config.get('username', None) and \
                valid_url(self.config.get('login_url', '')) and \
                valid_url(self.config.get('login_url', ''))

    def save_config(self, data):
        with open(CONFIG_FILE, 'w') as configfile:
            json.dump(data, configfile, indent=4)

    def format_quiz_url(self, quiz_url):
        return '?'.join((urljoin(quiz_url, urlparse(quiz_url).path), 'id={}'))

    def store_config(self, login_url, quiz_url, username):
        data = {'username': username,
                'login_url': login_url,
                'quiz_url': quiz_url}
        self.save_config(data)

    def get_input_value(self, text, validator=None, validator_error=None):
        data = input(text)
        if validator:
            if not validator(data):
                if validator_error:
                    print(validator_error)
                else:
                    print('Invalid Input')
                return self.get_input_value(text, validator=validator, validator_error=validator_error)
        return data

    def start(self):
        print("""Welcome to quizimporter, thank you for supporting us.
There are a couple of settings we need to setup in order to make the experience better.
If you have any questions please check the README on github.""")
        login_url = self.get_input_value('Please input your moodle quiz login URL (usually ends up in login.php): ',
                                         validator=valid_url,
                                         validator_error='Invalid URL')
        quiz_url = self.get_input_value('Please input your moodle quiz page (usually ends up in view.php): ',
                                        validator=valid_url,
                                        validator_error='Invalid URL')
        quiz_url = self.format_quiz_url(quiz_url)
        username = self.get_input_value('PLease input your login username: ')
        self.store_config(login_url, quiz_url, username)
        print('Setup Finished, you can now import quizzes! ENJOY!')

    def import_quiz(self, quiz_id):
        if self.valid_config:
            try:
                scrapper = MoodleScrapper(**self.config)
            except MoodleScrapperInvalidCredentialsException as e:
                print(e)
            except MoodleScrapperBadLoginURLException as e:
                print(e)
            else:
                try:
                    scrapper.get_quiz(quiz_id)
                except MoodleScrapperQuizNotFoundException as e:
                    print(e)
        else:
            print('No valid configuration files available')



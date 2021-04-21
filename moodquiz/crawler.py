from urllib.parse import urlparse, ParseResult, parse_qsl, urlencode
from bs4 import BeautifulSoup
from dashtable import html2rst
from jinja2 import Environment, FileSystemLoader
from moodquiz.utils import parse_test_body
from moodquiz.exceptions import *
import getpass
import mechanize
import os
import sys

sys.path.append(os.path.dirname(__file__))

class MoodleScrapper:
    def __init__(self, username, login_url, quiz_url):
        self.quiz_url = quiz_url
        self.login_url = login_url
        self.username = username
        self.password = getpass.getpass('Password:')
        self.br = mechanize.Browser()
        self.login()

    def is_login(self, title):
        return 'Log in' in title

    def login(self):
        self.br.open(self.login_url)
        if not self.is_login(self.br.title()):
            raise MoodleScrapperBadLoginURLException
        self.br.select_form(nr=0)
        form = self.br.forms()[0]
        form['username'] = self.username
        form['password'] = self.password
        self.br.submit()
        if self.is_login(self.br.title()):
            raise MoodleScrapperInvalidCredentialsException

    def write_template_to_file(self, data, template, file_name, quiz_name):
        env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates/")))
        template = env.get_template(template)
        output_from_parsed_template = template.render(**data)
        with open('/'.join((quiz_name, file_name)), "w") as fh:
            fh.write(output_from_parsed_template)

    def get_question(self, content, info, question_number, quiz_name):
        state = info.find('div', {"class": "state"}).text
        grade = info.find('div', {"class": "grade"}).text
        formulation = content.find('div', {'class': "formulation"})
        answer = content.find('textarea', {"class": "coderunner-answer"}).text
        test_cases = self.has_tests(content)
        if test_cases:
            examples_table = self.get_examples_table(test_cases)
            parsed_table = html2rst(examples_table.__str__().replace('"""', '"'), force_headers=False)

        question_payload = {"question_number": question_number,
                            "mark": grade,
                            "answer": answer,
                            "completed": state,
                            "examples": parsed_table if test_cases else '',
                            "question": formulation.find('p').text}

        self.write_template_to_file(question_payload,
                                    'question.template',
                                    'question{}.py'.format(question_number),
                                    quiz_name)
    def has_tests(self, content):
        test_cases = content.find('div', {"class": "coderunner-examples"})
        return test_cases if test_cases else False

    def get_examples_table(self, test_cases):
        examples_table = test_cases.find('table', {"class": "coderunnerexamples"})
        return examples_table if examples_table else False

    def get_tests(self, content, question_number, quiz_name):

        test_cases = self.has_tests(content)
        if not test_cases:
            return

        examples_table = self.get_examples_table(test_cases)
        if not examples_table:
            return

        examples_table = examples_table.find('tbody')
        tests = {"question_number": question_number, "tests": []}
        counter = 0
        for tr in examples_table.find_all('tr'):
            tds = tr.find_all('td')
            body = parse_test_body(tds[0].text)
            test_payload = {"number": str(counter),
                            "body": body,
                            "result": tds[1].text.strip()}
            tests['tests'].append(test_payload)
            counter += 1

        self.write_template_to_file(tests,
                                    'tests.template',
                                    'test_question{}.py'.format(question_number),
                                    quiz_name)

    def get_page(self, content, quiz_name):
        code_runners = content.find_all("div", {"class": "coderunner"})
        for div in code_runners:
            content = div.find('div', {"class": "content"})
            info = div.find('div', {"class": "info"})
            question_number = info.find('h3').find('span').text
            self.get_question(content, info, question_number, quiz_name)
            self.get_tests(content, question_number, quiz_name)

    def has_next_page(self, soup):
        return soup.find('input', {"name": "nextpage"}).get('value')

    def go_to_page(self, page):
        u = urlparse(self.br.geturl())
        data = dict(parse_qsl(u.query))
        if page == 0:
            del data['page']
        else:
            data['page'] = page
        res = ParseResult(scheme=u.scheme, netloc=u.hostname, path=u.path, params=u.params, query=urlencode(data),
                          fragment=u.fragment)
        self.br.open(res.geturl())

    def get_quiz_name(self):
        page = self.br.response().read()
        soup = BeautifulSoup(page, features='html5lib')
        name = soup.find('div', {"role": "main"}).find('h2').text
        if not os.path.exists(name):
            os.mkdir(name)
        return name

    def get_pages(self, quiz_name):
        page = self.br.response().read()
        soup = BeautifulSoup(page, features='html5lib')
        self.get_page(soup, quiz_name)
        next_page = self.has_next_page(soup)
        if next_page != '-1':
            self.go_to_page(next_page)
            self.get_pages(quiz_name)

    def get_quiz_url(self, id):
        return self.quiz_url.format(id)

    def get_quiz(self, id):
        try:
            self.br.open(self.get_quiz_url(id))
        except mechanize.HTTPError as e:
            raise MoodleScrapperQuizNotFoundException
        quiz_name = self.get_quiz_name()
        print('Getting Quiz {}'.format(quiz_name))
        self.br.select_form(nr=0)
        self.br.submit()
        if 'page' in self.br.geturl():
            self.go_to_page(0)
        self.get_pages(quiz_name)



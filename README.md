## Inspiration:

Inspired by the way coursera manages their quizzes/assignments I wanted to build a tool that supported this feature for courses using Moodle Platform.

My biggest struggle when doing Quizzes/Assignments in Moodle is that I have to create environments to code and tests the questions before submitting them into the platform, this takes a lot of time and also opens the door to unintentional mistakes.

The idea of this project is to give students the opportunity to import Python coding questions into a project, creating test cases for the examples given (if they have examples) all in the comfort of their IDE or console.

## Tech Stack:

* [Mechanize](https://mechanize.readthedocs.io/en/latest/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to navigate and parse the quizzes.
* [unittest](https://docs.python.org/3/library/unittest.html) and [pytest](https://docs.pytest.org/en/6.2.x/) to execute tests.
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) for question templates.
* [dashtable](https://github.com/doakey3/DashTable) to turn HTML tables into ASCII tables.
* Python > 3

## Installation

While we are in beta installation is as follows:

```
pip install git+https://github.com/tagercito/moodquiz.git
```

Mood Quiz project adds a new command to your sys path: **mquiz**

**RECOMMENDATION** : Create a virtualenv for this installation and all your code challenges.

## Supported OS

```
  Linux
  MacOS
  Windows ( haven't been able to test it)
```

## Usage:

```
mquiz [-h] [-s] [-q QUIZ] [-t TEST]
```

### First time command -s --start

```
mquiz -s
```

First time we execute mquiz we have to create a config file, this includes your moodle login page, the quiz page and your username.
**NOTE**: We never store your password, it is asked everytime you import a quiz.
We need this setup in order to make imports as easy and fast for the student as possible.

**LOGIN_URL** : You have to provide the login url to your current moodle provider, this url is the one you use to login to your quiz server, usually endinding in : login.php.

**Example**: https://moodle.com/2021/login.php

**QUIZ_URL**: This is the url of any quiz that you have in your platform, it usually ends in /mod/quiz/view.php.

**Example**: https://moodle.com/mod/quiz/view.php?id=123  (the params in the uri don't matter, the app will take care of this.)

**USERNAME**: The username you use to login to the platform.

This command will create a json configuration file on your current path (**.config.ini**)
In case something was misspelled during configuration you can either edit that file or run the command again. 

### Import QUIZ -q --quiz QUIZ_ID

```
mquiz -q {QUIZ_ID}
mquiz -q 124
```

This command imports a quiz into your current path, the param **QUIZ_ID** is the ID given to the quiz in the quiz page, usually it is after view.php?id=**QUIZ_ID**.

**Example**: If your quiz url is: https://moodle.com/mod/quiz/view.php?id=123 then **123** is your **QUIZ_ID**.

It will ask for password in order to login and will create a folder with the quiz name. 

Once this proccess is finished you should see the a new folder on your path with the name of the quizz and inside of it the questions and tests. 
The command only imports questions that have code challenges.

### Test QUIZ Question -t --test QUESTION_ID

```
mquiz -t {QUESTION_ID}
mquiz -t 1 (for question 1)
```

This command runs pytest for the id of the questions. **NOTE**: You have to be inside the quiz folder for this command to work.


## TODO: 
1) Write tests for the scrapper and wrapper (ironic isn't it?)
2) Allow the user to submit questions after all tests have passed. 
3) Allow script to import further tests if code fails on server side (hidden) tests.
4) Add documentation.
5) Better error management.
6) Test with more quiz examples and possible different quizz outputs (only supports stdout for now)





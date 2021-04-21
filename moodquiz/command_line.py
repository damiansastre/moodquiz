import argparse
import os
from .moodquiz import Moodle

def main():
    p = argparse.ArgumentParser()
    p.add_argument('-s', '--start', action="store_true")
    p.add_argument('-q', '--quiz', type=int)
    p.add_argument('-t', '--test', type=int)

    args = p.parse_args()

    if args.test:
        os.system('pytest test_question{}.py'.format(args.test))
    else:
        handler = Moodle()
        if args.start:
           handler.start()
        if args.quiz:
            handler.import_quiz(args.quiz)


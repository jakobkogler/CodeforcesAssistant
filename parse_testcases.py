#!/usr/bin/env python3
from bs4 import BeautifulSoup, NavigableString
from urllib.request import urlopen
import argparse
import os
import re


def format_testcase(test):
    return '\n'.join(e for e in test.pre.contents if isinstance(e, NavigableString))


def parse_testcases(contest, problem):
    url = 'http://codeforces.com/contest/{contest}/problem/{problem}'
    url = url.format(contest=contest, problem=problem)
    page = urlopen(url).read()
    soup = BeautifulSoup(page, 'lxml')

    find = lambda test_type: soup.find_all('div', class_=test_type)
    test_cases = zip(find('input'), find('output'))
    test_cases_nice = [[format_testcase(part) for part in test_case] for test_case in test_cases]
    return test_cases_nice


def parse_args():
    parser = argparse.ArgumentParser(description='Parse test cases from Codeforce problem')
    parser.add_argument('ids', metavar='id', nargs='+', help='problem id, e.g. 123D')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-d', '--directory', metavar='dir', help='working directory', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    for problem_id in args.ids:
        m = re.match('(\d+)([A-Z]+)', problem_id)
        if m:
            contest, problem = m.groups()
            dir_path = os.path.join(args.directory, contest, problem)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            for idx, test_case in enumerate(parse_testcases(contest, problem), start=1):
                for text_type, text in zip(("input", "output"), test_case):
                    file_path = os.path.join(dir_path, '{}{}'.format(text_type, idx))
                    with open(file_path, 'w') as f:
                        f.write(text)


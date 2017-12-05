# Rango Tests for WAD2 and ITECH

## Introduction

These tests are only valid for the Rango app of the Tango with Django Book (https://leanpub.com/tangowithdjango19/) up to Chapter 10. Each test runs view and model tests. If you are in Chapter 6, tests from previous chapters might fail as the structure of templates/views changes as you develop Rango.

## Requirements:

* Python 3.6.2
* bcrypt 3.1.4
* cffi 1.11.2
* Django 1.11.7
* olefile 0.44
* Pillow 4.3.0 -> On Windows, pip install might fail so download Pillow wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/
* pycparser 2.18
* pytz 2017.3
* six 1.11.0

## How-To

To use these tests, download/clone this repository, open a terminal/command prompt, navigate to this repository directory and run:

`python run_tests.py -u "Your GitHub repository" -s "student name" -d "YYYY-MM-DD"`

without "". Alternatively, you can run each test for each chapter by copying the corresponding chapter's test and, "test_utils.py" and "decorators.py" into the "rango" directory and run (in your app directory):

`python manage.py test rango.tests_chapter3`

`python manage.py test rango.tests_chapter4`

`...`

`python manage.py test rango.tests_chapter10`


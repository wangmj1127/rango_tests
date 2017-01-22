# Rango Tests for WAD2 and ITECH

## Introduction

These tests are only valid for the Rango app of the Tango with Django Book (https://leanpub.com/tangowithdjango19/) up to Chapter 10. Each test runs view and model tests. If you are in Chapter 6, tests from previous chapters might fail as the structure of templates/views changes as you develop Rango.

## Requirements:

* Python 2.7
* Django-1.10
* Pillow-3.3.1

## How-To

To use these tests, download/clone this repository, open a terminal/command prompt, navigate to this repository directory and run:

python run_tests.py -u "Your GitHub repository" -s "student name" -d "YYYY-MM-DD"

without "". Alternatively, you can run each test for each chapter by copying the corresponding chapter's test into trhe "rango" directory and run (in your app directory):

`python manage.py test rango.tests_chapter3`

`python manage.py test rango.tests_chapter4`

`...`

`python manage.py test rango.tests_chapter10`


# Alt-wordPlay

This repo is a web application designed for learning English vocabulary from not only word meanings, but also synonmys, antonmys, quotations, images and videos. Logged in users can also import and export word database for backup and offline learning.

## Table of contents

- [Motivation](#motivation)
- [Project status](#project-status)
- [Screenshots](#screenshots)
- [Tech/framework used](#tech/framework-used)
- [Features](#features)
- [Distinctiveness and complexity](#Distinctiveness-and-complexity)
- [What’s contained in each file](#What’s-contained-in-each-file)
- [How to run the app?](#how-to-run-the-app?)
- [Credits](#credits)
- [Sources](#sources)

## Motivation

As a former linguist, I have always wanted to find a better way to study foreign languages. Words are core components of any languages of the world. Establishing a personal word database helps not only in memorizing, but also improving clarity and vividity through images and videos, expanding vocabulary by providing synonyms and antonyms, and building up sophisticated context through adding quotations.

## Project status

Images/Videos tab will be updated to contain more contents.

It only supports English vocabulary at the moment. But it will be developed and improved for polyglots learning different languages, such as Japanese, French, Chinese, Spanish etc., or even Dothraki! And words with same or similiar definitions can be compared for reinforcing memory and connection.

A separate section for beginners learning English will also be developed.

## Screenshots

Quick look at a word example:

![Word example](https://github.com/michelle2014/wordPlay-website/blob/master/wordPlay/static/word_example.png "Word example")

A bit of competition:

![Leaderboard](https://github.com/michelle2014/wordPlay-website/blob/master/wordPlay/static/leaderboard_example.png "Leaderboard")

## Tech/framework used

Built with

- Frameworks: Django3.0/Bootstrap4.0
- Libraries: jQuery3.2
- Languages: Python3.8/JavaScriptES6/CSS3/HTML5

## Features

Create a word:

![Create a word](https://github.com/michelle2014/wordPlay-website/blob/master/wordPlay/static/create_example.png "Create a word")

Import words from xls, xlsx, csv and ods files:

![Import a word](https://github.com/michelle2014/wordPlay-website/blob/master/wordPlay/static/import_example.png "Import words")

Export all words:

![Export all words](https://github.com/michelle2014/wordPlay-website/blob/master/wordPlay/static/export_example.png "Export all words")

Exported CSV file example:

![Exported CSV file example](https://github.com/michelle2014/wordPlay-website/blob/master/wordPlay/static/csv_open_example.png "Exported CSV file example")

## Distinctiveness and complexity

### Distinctiveness

1. The app can work with kindle vocabulary builder. First of all, export words from kindle using [Kindle Mate](https://findanyanswer.com/goto/453765) into a xlsx file. Modify the file and add information if necessary. Then, import to the app to study.

2.

### Complexity

1. Used [Custom template tags](https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/) for functionality not covered by the core set of template primitives.

2. Applied an import function for quick database building

3. Employed [download](https://docs.djangoproject.com/en/3.1/howto/outputting-csv/) for outputting csv files

4. Wrote [validators](https://docs.djangoproject.com/en/3.1/ref/validators/) for validating emails

5. Created [.gitignore](https://git-scm.com/docs/gitignore) for specifying intentionally untracked file of secret.py to ignore, which contains [SECRET_KEY](https://docs.djangoproject.com/en/3.1/ref/settings/).

6. Limited the number of visible pages in pagination by JavaScript

7. Defined methods in models for getting remote images and videos and embeding them in word descriptions, in addition to directly uploading images and videos to the app

8. Added image field for user's profile image and a form in models for updating the image

9. Adopted [Django messages framework](https://docs.djangoproject.com/en/3.1/ref/contrib/messages/)

10. Made use of [Pandas](https://pandas.pydata.org/) for reading of excel files

11. Each words may have several quotations for the sake of complexity of word context, only the latest one is displayed in word descriptions on account of simplicity and space

12. Tabs have been created for expandable content

13. Bookmarks for sharing database of others.

14. Ability to search for a specific word. Since different user may have different descriptions, word is not unique. Search results could be a list

## What’s contained in each file?

## How to run the app?

1. Install Django.

- Install pip. The easiest is to use the standalone [pip](https://pip.pypa.io/en/latest/installing/#installing-with-get-pip-py) installer. If your distribution already has pip installed, you might need to update it if it’s outdated. If it’s outdated, you’ll know because installation won’t work.

- Take a look at [venv](https://docs.python.org/3/tutorial/venv.html). This tool provides isolated Python environments, which are more practical than installing packages systemwide. It also allows installing packages without administrator privileges.

- After you’ve created and activated a virtual environment, enter the command:

```
$ python -m pip install Django

```

You can tell Django is installed and which version by running the following command in a shell prompt (indicated by the $ prefix):

```
$ python -m django --version

```

If Django is installed, you should see the version of your installation. If it isn’t, you’ll get an error telling “No module named django”.

2. Install [Python](https://www.python.org/getit/)

How to check python version:

```
C:> python -V
Python 3.8.4
```

or

```
C:> python -version
Python 3.8.4
```

3. Install [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)

4. Start a local web server by running the command below:

```
$ python manage.py runserver

```

## Credits

[Limit the number of visible pages in pagination by JavaScript from stackoverflow](https://stackoverflow.com/questions/46382109/limit-the-number-of-visible-pages-in-pagination)

## Sources

This app is inspired by Damien Elmes, the developer of [Anki](https://apps.ankiweb.net/).

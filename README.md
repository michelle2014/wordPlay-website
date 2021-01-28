# Alt-wordPlay

This repo is a web application designed for learning English vocabulary from not only word meanings, but also synonmys, antonmys, quotations, images and videos.

Logged in users can also import and export word database for backup and offline learning.

## Table of contents

- [Motivation](#motivation)
- [Project status](#project-status)
- [Screenshots](#screenshots)
- [Tech/framework used](#tech-/-framework-used)
- [Features](#features)
- [Distinctiveness and complexity](#distinctiveness-and-complexity)
- [What’s contained in each file created?](#what’s-contained-in-each-file-created-?)
- [How to run the app?](#how-to-run-the-app-?)
- [Credits](#credits)
- [Sources](#sources)

## Motivation

As a former linguist, I have always wanted to find a better way to study foreign languages.

Words are core components of any languages of the world.

Establishing a personal word database helps not only in memorizing, but also improving clarity and vividity through images and videos, expanding vocabulary by providing synonyms and antonyms, and building up sophisticated context through adding quotations.

## Project status

Images/Videos tab will be updated to contain more contents.

It only supports English vocabulary at the moment. But it will be developed and improved for polyglots learning different languages, such as Japanese, French, Chinese, Spanish etc., or even Dothraki!

And words with the same or similiar definitions in the same language or of different languages can be compared for reinforcing memory and connection.

A separate section for beginners learning English will also be developed.

Categories have been set up and can be added, based on which new function is planned to be created for group learning.

Download by category is, of course, necessary in the future.

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

1. Applied an upload function for quick word database building. File format supported: tsv, csv, xls, xlsx, ods.

2. Employed [download](https://docs.djangoproject.com/en/3.1/howto/outputting-csv/) for outputting csv files of word data.

3. The app can work with kindle vocabulary builder. First of all, export words from kindle using [Kindle Mate](https://findanyanswer.com/goto/453765) for windows or [Fluent Cards](https://fluentcards.com/) for Linux into a xlsx file or other file formats supported. Modify the file and add information if necessary. Then, import the file to the app to study. If further modification after import is needed, a pre-filled edit form is also available to use.

4. Ability to search for a specific word. Since different user may have different description for the same word and even word of same spelling could have different definitions in different languages, word is not unique. Search result could be a list.

5. Defined methods in models for getting remote images and videos and embeding them in word descriptions, in addition to directly uploading images and videos to the app. In fact, Anki, despite of a good app, does't provide a way for working directly with remote images and videos. Users need to seek to HTML video tag or possiblely canvas tag to make it work. But audio and video elements are quite important in studying languages because they help quickly associate word with context and deeply comprehend word meanings.

### Complexity

1. Used [Custom template tags](https://docs.djangoproject.com/en/3.1/howto/custom-template-tags/) for functionality not covered by the core set of template primitives. With one function, custom template tags of words can be applied to different pages of the app.

2. Wrote [validators](https://docs.djangoproject.com/en/3.1/ref/validators/) for validating emails.

3. Created [.gitignore](https://git-scm.com/docs/gitignore) for specifying intentionally untracked file of secret.py to ignore, which contains [SECRET_KEY](https://docs.djangoproject.com/en/3.1/ref/settings/) for security reason.

4. Limited the number of visible pages in pagination by JavaScript. Extra page number is displayed as '...' in case of pagination size larger than 10.

5. Added image field for user's profile image and a form in models for updating the image.

6. Adopted [Django messages framework](https://docs.djangoproject.com/en/3.1/ref/contrib/messages/).

7. Made use of [Pandas](https://pandas.pydata.org/) for reading excel files.

8. Each word may have several quotations for the sake of complexity of word context, only the latest one is displayed in word descriptions on account of simplicity and space.

9. Tabs have been created for expandable content.

10. Bookmarks for sharing database of others.

## What’s contained in each file created?

- secrets.py in capstone folder for keeping [SECRET_KEY](https://docs.djangoproject.com/en/3.1/ref/settings/) for security reason.

- images, profiles and videos folders for respectively keeping local images, profile images and videos

- urls.py in wordPlay app folder for page routes and API routes

- models.py in wordPlay app folder for creating models and forms

- view.py in wordPlay app folder for getting data from database, providing context for custom template tags and writing API for asychronous response

- play.js in static folder for limiting pagination size, disabling buttons, asynchronous submission of like and bookmark form and asynchronous calculation thereof, changing fontawesome when button is clicked

- styles.css in static folder for styling displayed pages

- html files in templates folder for for displaying pages

- word_extras.py in templatetags folder for creating custom template tags

- requirements.txt in the root directory for runtime requirements

- spec.md in the root directory for project planning

- test.csv, test.ods, test.tsv, test.xls, test.xlsx, test1.xlsx, upload.xls in the root directory for testing import with different file formats

- words.csv in the root directory for an example of downloaded word data file

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

Group learning idea is encouraged by [Free Rice](https://freerice.com/).

======
MyRuns
======

MyRuns was developed as a project for learning Flask. It works only after authorization in Strava and reads data from it.
From all activities, it calculates how many kilometers were covered by runs (only) in the past week (Mon - Sun).
Then the user sees his target (+10% from previous week) and the progress for the current week.

How to install
""""""""""""""
1. install the package: pip install MyRuns
2. update API_KEYS.py in the same directory with MyRuns.py
3. API_KEYS must have these 5 lines:

MY_STRAVA_CLIENT_ID = XXXXX

MY_STRAVA_SECRET = 'XXXXX'

REDIRECT_URI = 'http://XXX.XXX.XXX.XXX:5000/authorize'

SECRET_KEY = 'XXX'

DATABASE = 'sqlite://///path/to/folder/user_token.db'

4. If you haven't already, register on strava.com as a developer.
5. Go to Settings - My Application
6. Here you will find your Client ID and Strava Secret. Also, enter your Authorization Callback Domain and put all these data in settings.py.
7. Create your SECRET_KEY: it's a string required to use by Flask_login.

How to use
""""""""""
1. Run 'MyRuns.py'
2. Click "Connect with Strava' and login.
3. That's it!

======
MyRuns
======

MyRuns was developed as a project for learning Flask. It works only after authorization in Strava and reads data from it.
From all activities, it calculates how many kilometers were covered by runs (only) in the past week (Mon - Sun).
Then the user sees his target (+10% from previous week) and the progress for the current week.

How to install
""""""""""""""
1. install the package: pip install MyRuns
2. If you haven't already, register on strava.com as a developer.
3. Go to Settings - My Application
4. Here you will find your Client ID and Strava Secret. Also, enter your Authorization Callback Domain, it will be needed for configuration.
5. Create your SECRET_KEY: it's a string required to use by Flask_login.
6. Run the following commands:

    MyRuns database

    MyRuns setup

    MyRuns config (NOTE: here you will be required to enter details gained above)

How to use
""""""""""
1. Run command: MyRuns run
2. Click "Connect with Strava' and login.
3. That's it!

# SmartTime #

SmartTime is a Slack bot, built with Python, that aims to deliver some of
[Clockwise](https://www.getclockwise.com/)'s features for free.

## Getting Set Up ##

SmartTime uses the
[Google Calendar API](https://developers.google.com/calendar/api) and Slack's
API, [Bolt](https://api.slack.com/tools/bolt) (Python bindings in both cases) -
both of which require a bit of setup outside of the application's code
environment.


### Google Calendar API ###

In order to use the Google Calendar API, you'll have to setup a Google Cloud
project/ application, enable the Google Calendar API, configure OAuth consent,
and generate authentication credentials. Everything you need to do this can be
found in
[this guide](https://developers.google.com/workspace/guides/get-started), with
the exception of the required API to enable, which is of course the Google
Calendar API (when you get to this step you can either search for it manually
or you can find it
[here](https://console.cloud.google.com/apis/library/calendar-json.googleapis.com?project=meta-coral-351508)
), and the required scope whilst configuring OAuth consent, which is the
`.../auth/calendar` scope for the Google Calendar API. When you come to
create access credentials, you need to opt for OAuth client ID credentials
for a desktop app - be sure the save the credentials JSON file on your
development machine as you'll need it to run the bot.


### Slack App ###

In order for SmartTime to work as a Slack bot, it needs a Slack App setup in
your Slack workspace. You can follow Slack's own
[getting started guide](https://slack.dev/bolt-python/tutorial/getting-started)
guide to get this set up. Be sure to make a note of the bot and app tokens as
you'll need these to run the bot. When you come to setup OAuth and permissions,
you'll need to add the following OAuth scopes:

* `channels:history`
* `chat:write`
* `commands`
* `groups:history`
* `im:history`
* `mpim:history`


### Development Environment ###

At this point you have everything in place for the SmartTime to function as a
Slack bot and use the Google Calendar API. To setup your local development
environment you need to:

* Create a virtual python environment and install the app's dependencies:
  ```shell
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
* Move your Google Cloud app credentials JSON file at the top level of the
  repository as `credentials.json`.
* Create a `slack_tokens.py` file at the top level of the repository, containing
  `APP` as the Slack app's app token and `BOT` as the Slack app's bot token
  (both as strings).
  

## Running The Bot ##
 To run SmartTime, simply invoke `bot.py` via the Python interpreter in your
 venv:
 
 ```shell
 python bot.py
 ```
 
 
 ## Deployment ##
 
 TODO
 

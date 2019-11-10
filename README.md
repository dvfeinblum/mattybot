# mattybot
slackbot for debaucheries

# Local Setup
This is our simple (for now) slackbot.
If you'd like to contribute, here's how you get started.

## Python Stuff
After pulling the repo, you'll want to create a venv.
Once you've done so, activate it a pip install the requirements.

## Secrets
For slack to be able to communicate with mattybot, we need to be able to verify requests.
You'll find `secrets.yml.template` in the route of this project.
Run
```bash
cp conf.d/secrets.yml.template conf.d/secrets.yml
```
and replace the fake values with real ones.
Currently this file is a bit bloated and we're only really using the `signing_secret` but those other values might come in handy later on.

## Running the server
At this point, you're ready to boot up the bot.
This can be done by running
```bash
DEBUG=True python bot.py
```
however, you won't be able to do much.

I highly recommend installing `ngrok`!
It'll allow you to expose the flask port to the open web so that the slack API can hit your python process.
Once you have it installed, run it in a separate terminal window:
```bash
ngrok http 5000
```
You'll get a forwarding URL which you can set in the slack API UI.

# Deploying
For now, I'm using `zappa` to automate the lambda deploys, hence the zappa_settings.json.
Currently, I'll be the only one doing this, so this next bit is mostly for me.
The `zappa_settings.json` currently only has a dev env so `zappa update dev` will get the latest code up into AWS.

# Reading list
I can't get over how easy this was.
Here are some posts I used to get this up in the cloud and running:
1. [Serverless Slash Commands with Python](https://renzo.lucioni.xyz/serverless-slash-commands-with-python/) by Renzo Lucioni
    * This post also clued me into `ngrok` which was super helpful for debugging and testing
1. [Verifying Requests from Slack](https://api.slack.com/docs/verifying-requests-from-slack)
    * [This](https://janikarhunen.fi/verify-slack-requests-in-aws-lambda-and-python) post by Jani Karhunen was crucial as well, because the first resource uses the old verification system that slack encourages you not to use.

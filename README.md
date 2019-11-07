# mattybot
slackbot for debaucheries

# Local Setup
This is our simple (for now) slackbot.
If you'd like to contribute, here's how you get started.

After pulling the repo, you'll want to create a venv.
Once you've done so, activate it a pip install the requirements.

At that point, you're ready to boot up the bot.
This can be done by running
```bash
DEBUG=True python bot.py
```
however, you won't be able to do much.

I highly recommend installing `ngrok`!
It'll allow you to expose the flask port to the open web so that the slack API can hit your python process.

# TODO
I'm gonna deploy this to lambda at some point very soon.
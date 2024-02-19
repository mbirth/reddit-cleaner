#!/usr/bin/env python3

# This script is based on a snippet posted here: https://github.com/j0be/PowerDeleteSuite/issues/55
# It can be used to overwrite the text of all the comments in your account, when you have over 1000 comments. Many tools are limited to the most recent 1000.

# CAUTION:

# I'm releasing this into the wild with ABSOLUTELY NO TECH SUPPORT. Use it at your own risk. If you're running it, it means that you have backups. If you know Python, you can modify it to restore the original text.
# But the original editing behaviour may get you banned from some subs, which may not be reversible. Caveat emptor!
# I tested this on Ubuntu Focal and nowhere else. In theory it should run wherever Python 3 can run.

# SETUP:

# Request your data export here: https://www.reddit.com/settings/data-request and wait for a link.
# Create a new app here: https://www.reddit.com/prefs/apps/ -- select "script". You have to enter a redirect URI; you can use http://localhost:8080
# Register to use the API as described here: https://www.reddit.com/wiki/api -- you need to create the app first (see above), because you need the ID from the app for the registration form. Wait for the confirmation email.
# Install the praw and pandas Python libraries. Save this script in the same directory as your unzipped backup data. Make it executable (or you'll need to execute it explicitly with Python 3).
# Edit the custom parameters in the script below:
#   your plaintext Reddit username and password (there are more secure ways to prompt for this, but you should only need to run this script once, and can then delete it or overwrite the value).
#   the ID and secret from the app you created
#   any plausible browser user agent (there are examples online, and sites that will tell you what your browser is reporting)
#   you can also modify the replacement string to anything you want
# Run the script, and wait for many hours (the free API access tier is rate-limited; the praw library automatically handles this and the script uses the maximum possible timeout limit).
# You can browse the backup file to find sample URLs and watch your comments wink out in real time, if you are that way inclined.
# If for some reason you interrupt the script, it should be safe to restart it. There's a guard which skips comments that already have your replacement text as their body.
# This script will log when an attempt to edit a comment returned an error response, and continue. This seems to happen when a comment in the backup is part of a deleted thread (this results in a 403).

import praw
import pandas as pd

df = pd.read_csv('comments.csv')
reddit = praw.Reddit(
    client_id="XXXXX",
    client_secret="XXXXX"
    password="XXXXX",
    user_agent="XXXXX",
    username="XXXXX",
    ratelimit_seconds=600
)

reddit.validate_on_submit = True

overwrite_string = "So long, and thanks for all the fish."

for commentId in df['id']:
    try:
        comment = reddit.comment(commentId)
        if comment.body != overwrite_string:
            comment.edit(overwrite_string)
    except:
        print(f"Error processing comment with id {commentId}.")
#!/usr/bin/env python3

# Original idea: https://github.com/j0be/PowerDeleteSuite/issues/55
# First draft: https://gist.github.com/confluence/3c9637a679ce4e65cfe9df9acee8796a
# This version: https://github.com/mbirth/reddit-cleaner

INPUT_FILE = "comments.csv"

APP_CLIENT_ID = "XXXXX"
APP_CLIENT_SECRET = "XXXXX"
USERNAME = "XXXXX"

USER_AGENT = "XXXXX"

OVERWRITE_STRING = "[intentionally deleted]"

##################################################################################################

import praw
from prawcore.exceptions import Forbidden
import pandas as pd
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, MofNCompleteColumn, TimeRemainingColumn
from rich.prompt import Prompt, IntPrompt
from rich.traceback import install
import sys

# use Rich Traceback handler, fail in style
install(show_locals=True)

# Query user for login data
skip_amount = IntPrompt.ask("How many CSV rows to skip before starting to process?", default=0)
password   = Prompt.ask(f"Enter password for account [b]{USERNAME}[/b]", password=True)
twofa_code = Prompt.ask("If you're using 2FA, enter your current OTA token otherwise just press [b]ENTER[/b]", password=True)

# If 2FA was specified, add to password
if len(twofa_code) > 0:
    password += ":" + twofa_code

# Become a Redditor!
reddit = praw.Reddit(
    client_id=APP_CLIENT_ID,
    client_secret=APP_CLIENT_SECRET,
    password=password,
    user_agent=USER_AGENT,
    username=USERNAME,
    ratelimit_seconds=600
)
# Praw doc says this is deprecated, praw itself says it's required?!
reddit.validate_on_submit = True

# Open CSV and get total number of records
print(f"Reading [b]{INPUT_FILE}[/b]...")
df = pd.read_csv(INPUT_FILE)
comment_count = len(df)
print(f"[bright_green]{comment_count} comments[/bright_green] found in CSV.")

# Start processing
with Progress(
    SpinnerColumn("point", style="bright_yellow", speed=0.5),
    TextColumn("[progress.description]{task.description}"),
    MofNCompleteColumn(),
    BarColumn(),
    TaskProgressColumn(),
    TimeRemainingColumn()
) as progress:
    ptask = progress.add_task("Processing comments...", total=comment_count)

    for i, row in df.iterrows():
        commentId = row['id']
        commentUrl = row['permalink']
        try:
            # Skip number of records as specified
            if i < skip_amount:
                continue
            progress.update(ptask, description=f"Processing comment {commentId}...")
            comment = reddit.comment(commentId)
            if not comment.body:
                # Praw doc defines this for deleted comments, but I've only encountered
                # HTTP 403 / Forbidden during my runs. However, left this here just in case.
                print(f"[orange1]Comment [bright_cyan][link={commentUrl}]{commentId}[/link][/bright_cyan] already deleted.[/orange1]")
                progress.update(ptask, completed=i+1)
                continue
            elif comment.body != OVERWRITE_STRING:
                # Edit the comment to our OVERWRITE_STRING
                comment.edit(OVERWRITE_STRING)
                print(f"[green1]Comment [bright_cyan][link={commentUrl}]{commentId}[/link][/bright_cyan] edited successfully.[/green1]")
            # Delete comment
            comment.delete()
            progress.update(ptask, completed=i+1)
            print(f"[green1]Comment [bright_cyan][link={commentUrl}]{commentId}[/link][/bright_cyan] deleted successfully.[/green1]")
        except Forbidden:
            # Praw returns this for deleted comments
            print(f"[orange1]Comment [bright_cyan][link={commentUrl}]{commentId}[/link][/bright_cyan] already deleted or otherwise not accessible.[/orange1]")
            progress.update(ptask, completed=i+1)
        except Exception as e:
            # Generic exception handler, e.g. for when a comment is in a locked sub
            print(f"Error processing [link={commentUrl}]comment with id {commentId}[/link].")
            print(repr(e))
            progress.update(ptask, completed=i+1)
            #sys.exit(1)

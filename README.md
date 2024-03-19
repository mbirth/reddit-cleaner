reddit-cleaner
==============

History
-------

With Reddit starting to sell their user's content to AI companies and also shutting down their API for 3rd party apps, I wanted to clean out my Reddit account and make my contributions over the past 10 years unusable for AI training.

From a [Reddit data export](https://www.reddit.com/settings/data-request) I knew that Reddit retains the last version of a comment - regardless of whether you've deleted it or not. So that's why I needed to overwrite every single comment before deleting it.

Also, Reddit only associates the latest 1,000 posts and comments with your profile. So everything older is not easily accessible from within Reddit. Some browser-based tools try to find more by trying the various different filters available in your Reddit profile, but in my case, this still left 7k+ of my 9k comments intact.

I was able to find many more comments to delete by using a Google query like `site:reddit.com "mbirth avatar"` (the `avatar` appears in your profile image, so this only shows comments you've actually made, not where you were mentioned). But when I cleaned out everything Google returned, too, a fresh data export still showed over 7k comments still intact.

As it's Spring cleaning time, I started looking for some tool that's still working. I got lucky in the comments of [this PowerDeleteSuite issue](https://github.com/j0be/PowerDeleteSuite/issues/55).

User [@confluence](https://github.com/confluence) turned the snippet mentioned there into a working bare-bones script and published it in [this GIST](https://gist.github.com/confluence/3c9637a679ce4e65cfe9df9acee8796a).



My version
----------

While the script from the GIST already works great for editing all your comments, I've added the deletion and also added a bit of logging and status output so you don't get bored while it's running. It also shows the expected time remaining so you know what to expect.

I've also added inputs for security critical data like the Reddit account password and OTA token. As well as a feature to skip a number of records if the script aborted mid-run and you don't want to wait for it to advance to the current position again.



CAUTION
=======

<div style="background-color: #fcc; padding: 1em;">

I'm releasing this into the wild with ABSOLUTELY NO TECH SUPPORT. Use it at your own risk. If you're running it, it means you're willing to delete your Reddit comments.

Also be aware that this kind of behaviour **may get you banned from some subs**, which may not be reversible. Caveat emptor!

</div>


Setup
-----

### Dependencies

* poetry
* praw
* pandas
* rich

After installing poetry, the remaining dependencies can be setup using: `poetry install`


### Reddit setup

Request your [Reddit data export](https://www.reddit.com/settings/data-request).

While waiting for it, [go here](https://www.reddit.com/prefs/apps/) and create a new "Reddit App". Give it a name, select *Script* as the type and enter `http://localhost:8080` as the *redirect uri* (as that's a required field).

After submitting, you'll see your new "app" with its **Client ID** (shown below the *personal use script* besides the icon) and - after expanding the box by clicking the *edit* link - your app's **secret**. You'll need both of these later.

Now [go here](https://www.reddit.com/wiki/api) and register to use the Reddit API. In the contact form select *I want to register to use the free tier of the Reddit API*. As purpose I've put *Other*. And into the mandatory field asking about the subreddits I plan to use this for, I've put *"all I've participated in"*. The remaining fields should be self-explanatory.

Wait for the mail from support to arrive, confirming you're allowed to use the API. Also, once your data export is ready, download it and unpack the `comments.csv` into the same directory where this script resides.


### Script setup

Edit the file `kill_comments.py`.

Change `APP_CLIENT_ID` to the **Client ID** of your Reddit App. Change the `APP_CLIENT_SECRET` to its **secret** (see above).

Set your Reddit username in `USERNAME`.

Now, [find your browser's user agent](https://explore.whatismybrowser.com/useragents/parse/?analyse-my-user-agent=yes#parse-useragent) and put it into the `USER_AGENT` variable.

And, finally, feel free to modify the `OVERWRITE_STRING` to your liking.



Running the script
------------------

If everything is set up, you can run the script using: **`poetry run ./kill_comments.py`**

It'll ask you for how many records to skip, your Reddit account password and OTA token.

![Screenshot showing example output of this script](/screenshot.png)

Thanks to the Rich library, the comment ids shown in the output are clickable links in supported terminal apps. So you can easily verify that your comments are gone.

If you see output like this:

    Error processing comment with id abcdefg.
    ClientException('No data returned for comment t1_abcdefg')

This means that comment was made in a sub that's now quarantined or locked and thus not accessible. There doesn't seem to be a way to properly delete it apart from legal action as per GDPR or similar.

Also be aware that you'll get lots of messages to your Reddit inbox from several sub's bots that complain about your edited comments as they catch the edit before the deletion. Just ignore/delete those messages.

Happy Spring cleaning!

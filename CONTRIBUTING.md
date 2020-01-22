# Contributing to CodeClassroom

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

## Guidelines

Make sure you follow below guidelines before contributing.

1. Raise an issue before sending any PR.
2. Try to solve issues which have a [**priority**](https://github.com/codeclassroom/codeclassroom/issues?q=is%3Aopen+is%3Aissue+label%3Apriority) label for quick acceptance of PR.
3. Make you changes to `feature` branch.
4. See if there is already an open PR for the same issue.
5. Send a Pull Request to the **`dev`** branch (not master).
6. Wait for the checks to Pass on the Pull Request (if anything fails try to fix it, or comment on the PR).
7. Wait for the team to review it.

> Raise an issue, if you have any doubts :)


## Environment Keys Setup

Here is how a sample `.env` file looks like

```
SECRET_KEY = 'the-secret-key'
DEBUG = 'any valid character for setting DEBUG=False'
MOSS_ID = "moss_user_id"
user_email = "your-gmail-address"
user_pass = "your-gmail-password"
```

### Getting `MOSS_ID`

- To obtain a Moss account, send a mail message to [moss@moss.stanford.edu](moss@moss.stanford.edu). The body of the message should appear exactly as follows:

```
registeruser
mail username@domain
```

where _username@domain_ is your email address. Make sure to NOT add any styling to the message (NO signature, NO bold text etc.)
- You will recieve an email in a minute or to containig the Shell Script, look for `$userid` in the script.

### Getting `SECRET_KEY`

You can use one of the following services to generate SECRET_KEY.

- [Django Secret Key Generator](https://www.miniwebtool.com/django-secret-key-generator/)
- [Djecrety](https://djecrety.ir/)

### Setting Gmail

- Make sure to Turn ON low security apps in your Google account.
- Login and go to [this](https://myaccount.google.com/lesssecureapps) link.